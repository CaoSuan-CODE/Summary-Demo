#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""locate_knowledge.py 最小测试：锚点跨节重置。"""

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import locate_knowledge as lk  # noqa: E402


def main():
    d = tempfile.mkdtemp()
    sub = os.path.join(d, "sub")
    os.makedirs(sub)
    md = os.path.join(sub, "foo-知识点讲解.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(
            "# foo 知识点讲解\n\n"
            "## 一、知识点讲解\n\n"
            '<a id="kp-01"></a>\n'
            "### 1. 概念（Concept）\n\n"
            "**讲解**：这是概念。\n\n"
            "## 二、知识点联系\n\n"
            "- 概念 → 应用：这里提到了汇聚。\n"
        )

    # 只出现在「知识点联系」节的词，链接应为文件级（无旧 kp-N 锚点）
    hits = lk.scan("汇聚", root=d)
    assert hits and hits[0][1] is None, "知识点联系节不应误挂 kp-N 锚点：%r" % hits

    # 出现在讲解节的词应命中 kp-01 锚点
    hits2 = lk.scan("概念", root=d)
    assert any(h[1] == "kp-01" for h in hits2), "讲解节命中应带 kp-01：%r" % hits2

    print("PASS  locate_knowledge 全部检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
