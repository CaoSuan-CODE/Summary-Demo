#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
course_summary.py — 枚举课程目录下各课件的「知识点摘要.md」，提取标题与 sm-N 主题，
供生成课程级知识体系（仅标准库）。

用法：
  python3 scripts/course_summary.py <课程目录>
  例：python3 scripts/course_summary.py content/Reflect/GEC3407
"""

import glob
import os
import re
import sys

_ANCHOR_RE = re.compile(r'<a[^>]*\bid="([^"]+)"[^>]*></a>')
_SUMMARY_RE = re.compile(r'^[-*•]\s*(?:\*\*)?概括(?:\*\*)?[：:]\s*(.*)$')


def parse_summary(path):
    info = {"title": "", "topics": []}
    anchor = None
    topic = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s.startswith("# "):
                info["title"] = s[2:].strip()
                continue
            m = _ANCHOR_RE.search(s)
            if m:
                anchor = m.group(1)
                continue
            mh = re.match(r"^#{2,6}\s+(.+)$", s)
            if mh and anchor:
                topic = mh.group(1).strip()
                continue
            m = _SUMMARY_RE.match(s)
            if m and anchor and topic:
                info["topics"].append((anchor, topic, m.group(1).strip()))
                anchor = None
    return info


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        sys.exit(1)
    course_dir = argv[1]
    pattern = os.path.join(course_dir, "*", "*-知识点摘要.md")
    files = sorted(glob.glob(pattern))
    if not files:
        print("未找到知识点摘要.md（目录：%s）" % course_dir)
        return
    for path in files:
        info = parse_summary(path)
        rel = os.path.relpath(path, course_dir)
        print("=== %s ===" % rel)
        print("  标题：%s" % info["title"])
        if not info["topics"]:
            print("  ⚠ 未解析到主题（格式可能已变，请检查该摘要 md 的锚点/概括行）")
        for anchor, topic, brief in info["topics"]:
            print("  [%s] %s —— %s" % (anchor, topic, brief))


if __name__ == "__main__":
    main(sys.argv)
