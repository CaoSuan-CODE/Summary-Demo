#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md_to_docx.py — 把 Markdown 转为高可读性的 .docx（仅标准库）。

支持：# / ## / ### 标题、- 或 • 无序列表、**加粗**、[文字](链接) 行内链接、
> 引用（斜体）、行内代码 `` `x` ``（剥反引号）、`| a | b |` 表格、普通段落；
跳过 <a id="..."> 锚点与 --- 分隔线。

用法：
  python3 scripts/md_to_docx.py 输入.md [输出.docx]   # 缺省输出同名 .docx
"""

import html
import os
import re
import sys
import zipfile

_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_BOLD_RE = re.compile(r"(\*\*[^*]+\*\*)")


def _esc(text):
    return html.escape(text, quote=False)


def _inline(text, rpr=""):
    """处理 **加粗**、[文字](链接)、行内代码 `x`、![图片]，返回一串 <w:r>。rpr 为应用于全部 run 的基础格式。"""
    text = text.replace("![", "[")
    text = _LINK_RE.sub(r"\1", text)
    text = text.replace("`", "")
    out = []
    for tok in _BOLD_RE.split(text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**"):
            out.append(
                '<w:r><w:rPr>%s<w:b/></w:rPr>'
                '<w:t xml:space="preserve">%s</w:t></w:r>' % (rpr, _esc(tok[2:-2]))
            )
        else:
            r = "<w:rPr>%s</w:rPr>" % rpr if rpr else ""
            out.append('<w:r>%s<w:t xml:space="preserve">%s</w:t></w:r>' % (r, _esc(tok)))
    return "".join(out)


def _p(text, size=22, bold=False, italic=False, bullet=False):
    rpr = []
    if bold:
        rpr.append("<w:b/>")
    if italic:
        rpr.append("<w:i/>")
    rpr.append('<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (size, size))
    rpr_xml = "".join(rpr)

    runs = _inline(text, rpr_xml) if text else '<w:r><w:t></w:t></w:r>'
    if bullet:
        runs = '<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">• </w:t></w:r>' % rpr_xml + runs

    ppr = '<w:pPr><w:ind w:left="360" w:hanging="360"/></w:pPr>' if bullet else ""
    return "<w:p>%s%s</w:p>" % (ppr, runs)


_TBL_BORDERS = (
    '<w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
    '</w:tblBorders>'
)


def _tbl(rows):
    """把二维单元格列表渲染为 w:tbl（首行为表头，加粗）。"""
    ncols = max(len(r) for r in rows)
    grid = "<w:tblGrid>%s</w:tblGrid>" % "".join(
        '<w:gridCol w:w="%d"/>' % (9000 // ncols) for _ in range(ncols))
    trs = []
    for ri, row in enumerate(rows):
        tcs = []
        for ci in range(ncols):
            cell = row[ci] if ci < len(row) else ""
            runs = _inline(cell, "<w:b/>" if ri == 0 else "")
            tcs.append(
                '<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/></w:tcPr>'
                '<w:p>%s</w:p></w:tc>' % runs)
        trs.append("<w:tr>%s</w:tr>" % "".join(tcs))
    return '<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/>%s</w:tblPr>%s%s</w:tbl>' % (
        _TBL_BORDERS, grid, "".join(trs))


def markdown_to_docx(md_text):
    body = []
    lines = md_text.split("\n")
    i = 0
    while i < len(lines):
        st = lines[i].rstrip().strip()
        if st.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                # 跳过 | --- | --- | 分隔行
                if not all(re.fullmatch(r"[-: ]*", c) for c in cells):
                    rows.append(cells)
                i += 1
            if rows:
                body.append(_tbl(rows))
            continue
        if not st or st == "---" or st.startswith("<a id="):
            i += 1
            continue
        if st.startswith("### "):
            body.append(_p(st[4:], size=26, bold=True))
        elif st.startswith("## "):
            body.append(_p(st[3:], size=30, bold=True))
        elif st.startswith("# "):
            body.append(_p(st[2:], size=36, bold=True))
        elif st.startswith("> "):
            body.append(_p(st[2:], size=22, italic=True))
        elif st.startswith("- ") or st.startswith("• ") or st.startswith("* "):
            body.append(_p(st[2:], size=22, bullet=True))
        else:
            body.append(_p(st, size=22))
        i += 1
    return "\n".join(body)


_CONTENT_TYPES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
"""

_RELS = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""


def build_docx(body_xml):
    doc = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:body>%s<w:sectPr/></w:body></w:document>' % body_xml
    )
    out = {}
    out["[Content_Types].xml"] = _CONTENT_TYPES
    out["_rels/.rels"] = _RELS
    out["word/document.xml"] = doc
    return out


def convert(md_path, out_docx=None):
    with open(md_path, encoding="utf-8") as f:
        md_text = f.read()
    body = markdown_to_docx(md_text)
    entries = build_docx(body)
    out_docx = out_docx or (os.path.splitext(md_path)[0] + ".docx")
    with zipfile.ZipFile(out_docx, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in entries.items():
            z.writestr(name, data)
    return out_docx


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)
    md_path = argv[1]
    out_docx = argv[2] if len(argv) >= 3 else None
    out = convert(md_path, out_docx)
    print("已生成 -> %s" % out)


if __name__ == "__main__":
    main(sys.argv)
