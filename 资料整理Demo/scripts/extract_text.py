#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_text.py — 从英文 Word/PPT 中抽取全文（仅 Python 标准库）。

讲解流程不做翻译，只需把英文源文件的全部文本导出为纯文本供通读。
按扩展名自动分发：
  .docx -> word/document.xml，按 w:p 聚合其下所有 w:t
  .pptx -> ppt/slides/slideN.xml（幻灯片正文）+ ppt/notesSlides/notesSlideN.xml（演讲者备注），
           按 a:p 聚合其下所有 a:t

用法：
  python3 scripts/extract_text.py dump 输入.<docx|pptx> 全文.txt
"""

import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"

_SLIDE_RE = re.compile(r"^ppt/slides/slide(\d+)\.xml$")
_NOTES_RE = re.compile(r"^ppt/notesSlides/notesSlide(\d+)\.xml$")


def _build_parent_map(root):
    parent = {}
    for el in root.iter():
        for child in list(el):
            parent[child] = el
    return parent


def _collect(root, ns):
    """把 root 下所有文本节点按最近段落聚合，返回 [(pid, text), ...]。"""
    parent = _build_parent_map(root)
    p_tag = "{%s}p" % ns
    t_tag = "{%s}t" % ns
    order = []
    ids = {}
    groups = {}

    def pid_of(p):
        if p not in ids:
            ids[p] = "p%03d" % len(order)
            order.append(p)
        return ids[p]

    for t in root.iter(t_tag):
        cur = parent.get(t)
        p = None
        while cur is not None:
            if cur.tag == p_tag:
                p = cur
                break
            cur = parent.get(cur)
        if p is None:
            continue
        pid = pid_of(p)
        groups.setdefault(pid, []).append(t)

    return [(ids[p], "".join(x.text or "" for x in groups[ids[p]])) for p in order]


def _dump_docx(docx):
    with zipfile.ZipFile(docx) as z:
        if "word/document.xml" not in z.namelist():
            raise SystemExit("未找到 word/document.xml，可能不是有效的 .docx")
        raw = z.read("word/document.xml")
    return _collect(ET.fromstring(raw), W)


def _dump_pptx(pptx):
    with zipfile.ZipFile(pptx) as z:
        entries = {n: z.read(n) for n in z.namelist()}
    slides = [n for n in entries if _SLIDE_RE.match(n)]
    notes = [n for n in entries if _NOTES_RE.match(n)]
    slides.sort(key=lambda n: int(_SLIDE_RE.match(n).group(1)))
    notes.sort(key=lambda n: int(_NOTES_RE.match(n).group(1)))
    out = []
    for name in slides + notes:
        sm = _SLIDE_RE.match(name)
        nm = _NOTES_RE.match(name)
        key = "s" + sm.group(1) if sm else "n" + nm.group(1)
        for pid, text in _collect(ET.fromstring(entries[name]), A):
            out.append(("%s-%s" % (key, pid), text))
    return out


def cmd_dump(src, out_txt):
    ext = os.path.splitext(src)[1].lower()
    if ext == ".docx":
        pairs = _dump_docx(src)
    elif ext == ".pptx":
        pairs = _dump_pptx(src)
    else:
        raise SystemExit("仅支持 .docx / .pptx：%s" % src)
    d = os.path.dirname(out_txt)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out_txt, "w", encoding="utf-8") as f:
        for pid, text in pairs:
            f.write("[%s] %s\n" % (pid, text.replace("\n", " ")))
    print("已导出 %d 个段落 -> %s" % (len(pairs), out_txt))


def main(argv):
    if len(argv) >= 4 and argv[1] == "dump":
        cmd_dump(argv[2], argv[3])
    else:
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv)
