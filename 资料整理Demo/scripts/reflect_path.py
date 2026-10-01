#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
reflect_path.py — 计算 content/Raw → content/Reflect 的输出路径映射（仅标准库）。

输入：content/Raw/<子目录>/<文件名>.<扩展名>
输出（相同结构映射到 content/Reflect/<子目录>/<文件名>/ 文件夹）：
  全文.txt / <文件名>-专有名词.md / <文件名>-知识点讲解.md / <文件名>-知识点摘要.md

课程目录（content/Reflect/<子目录>/）下另有：
  讲解原则.md   课程级讲解要求（首次映射该课程时由 --mkdir 创建）

用法：
  python3 scripts/reflect_path.py "content/Raw/GEC3407/Chapter 3.pptx"
  python3 scripts/reflect_path.py --mkdir "content/Raw/..."   # 同时创建输出文件夹
"""

import os
import sys

_RAW = "content" + os.sep + "Raw"

# 课程级讲解原则模板（首次映射课程时创建，优先级介于 CLAUDE.md 与全局讲解原则之间）
_COURSE_PRINCIPLES_TMPL = (
    "# 讲解原则（%s）\n\n"
    "> 本文件记录仅针对本课程的讲解要求，优先级高于 "
    "`.claude/skills/summarize-knowledge/知识点讲解原则.md`，低于 `CLAUDE.md`。"
    "未列出的项默认遵循全局规则。\n\n"
    "## 课程特定要求\n\n"
    "（在此记录本课程的特殊讲解要求；无则留空。）\n"
)


def reflect_paths(raw_path):
    p = raw_path.replace("\\", os.sep)
    p = os.path.normpath(p)
    if not p.startswith(_RAW + os.sep):
        raise SystemExit("输入路径须在 content/Raw/ 下：%s" % raw_path)
    rel = p[len(_RAW) + 1:]  # 去掉 content/Raw/ 前缀
    dirs, fname = os.path.split(rel)
    stem, ext = os.path.splitext(fname)
    base = os.path.join("content", "Reflect", dirs, stem)
    return {
        "dir": base,
        "dump": os.path.join(base, "全文.txt"),
        "proper_nouns": os.path.join(base, stem + "-专有名词.md"),
        "knowledge_detail": os.path.join(base, stem + "-知识点讲解.md"),
        "knowledge_summary": os.path.join(base, stem + "-知识点摘要.md"),
        "course_explain_principles": os.path.join(os.path.dirname(base), "讲解原则.md"),
    }


def main(argv):
    mkdir = False
    args = argv[1:]
    if args and args[0] == "--mkdir":
        mkdir = True
        args = args[1:]
    if len(args) < 1:
        print(__doc__)
        sys.exit(1)
    paths = reflect_paths(args[0])
    if mkdir:
        os.makedirs(paths["dir"], exist_ok=True)
        print("已创建文件夹：%s" % paths["dir"])
        # 首次映射该课程时，在课程目录下创建课程级讲解原则.md
        cpp = paths["course_explain_principles"]
        if not os.path.exists(cpp):
            course_name = os.path.basename(os.path.dirname(paths["dir"]))
            with open(cpp, "w", encoding="utf-8") as f:
                f.write(_COURSE_PRINCIPLES_TMPL % course_name)
            print("已创建课程级讲解原则：%s" % cpp)
    for k, v in paths.items():
        print("%-12s %s" % (k, v))


if __name__ == "__main__":
    main(sys.argv)
