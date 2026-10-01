#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
locate_knowledge.py — 跨文件定位知识点（仅标准库）。

扫描 content/Reflect/** 下的知识点 md（讲解 / 摘要 / 专有名词），按关键字命中行
回溯最近的 <a id="..."> 锚点与标题，输出「文件路径#锚点」可点击链接。

用法：
  python3 scripts/locate_knowledge.py <关键字>
"""

import glob
import os
import re
import sys

_ANCHOR_RE = re.compile(r'<a id="([^"]+)"></a>')
_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$')


def scan(query, root=os.path.join("content", "Reflect")):
    results = []
    q = query.lower()
    for path in sorted(glob.glob(os.path.join(root, "**", "*.md"), recursive=True)):
        base = os.path.basename(path)
        if "知识点" not in base and not base.endswith("-专有名词.md"):
            continue
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        anchor = None
        heading = None
        for line in lines:
            mh = _HEADING_RE.match(line)
            if mh:
                heading = mh.group(2).strip()
                # 进入新的顶层/二级章节（#/##）时重置锚点，避免「知识点联系」等无锚点节误挂上一节的 kp-N
                if len(mh.group(1)) <= 2:
                    anchor = None
            m = _ANCHOR_RE.search(line)
            if m:
                anchor = m.group(1)
            if q in line.lower():
                results.append((path, anchor, heading, line.strip()))
    return results


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)
    query = argv[1]
    results = scan(query)
    if not results:
        print("未找到匹配：%s" % query)
        return
    print("找到 %d 处匹配：\n" % len(results))
    for path, anchor, heading, line in results:
        link = path + ("#" + anchor if anchor else "")
        label = (heading or line)[:40]
        snippet = line[:80]
        print("- [%s](%s) — %s" % (label, link, snippet))


if __name__ == "__main__":
    main(sys.argv)
