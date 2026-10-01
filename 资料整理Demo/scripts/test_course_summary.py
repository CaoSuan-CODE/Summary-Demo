#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course_summary.py 最小测试：锚点属性/加粗概括/多级标题容错，空主题告警。"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import course_summary as cs  # noqa: E402


def main():
    d = tempfile.mkdtemp()

    good = os.path.join(d, "good.md")
    with open(good, "w", encoding="utf-8") as f:
        f.write(
            "# 好 知识点摘要\n\n"
            "## 一、知识点概述\n\n"
            '<a id="sm-01"></a>\n'
            "### 1. 主题A（Topic A）\n"
            "- **概括**：这是粗体概括。\n\n"
            '<a id="sm-02" name="x"></a>\n'
            "#### 2. 主题B（Topic B）\n"
            "- 概括：普通概括。\n\n"
            "## 二、知识点联系（概览）\n"
            "- 主题A → 主题B（依赖）：联系说明。\n"
        )
    info = cs.parse_summary(good)
    assert info["title"] == "好 知识点摘要"
    assert [(a, t, b) for a, t, b in info["topics"]] == [
        ("sm-01", "1. 主题A（Topic A）", "这是粗体概括。"),
        ("sm-02", "2. 主题B（Topic B）", "普通概括。"),
    ], info["topics"]

    # 无锚点的文件应解析出 0 主题（main 会打印告警）
    bad = os.path.join(d, "bad.md")
    with open(bad, "w", encoding="utf-8") as f:
        f.write("# 坏 知识点摘要\n\n### 1. 主题A\n- 概括：无锚点。\n")
    assert cs.parse_summary(bad)["topics"] == []

    print("PASS  course_summary 全部检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
