#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""md_to_docx.py 最小测试：剥反引号、表格、图片感叹号、加粗/字号。"""

import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import md_to_docx as m  # noqa: E402

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def main():
    md = (
        "# 标题\n\n"
        "## 二、测试\n\n"
        "### 3. 知识点（Knowledge）\n\n"
        "**讲解**：这里是 `[32,28,28] -> [32,10]` 的说明。\n\n"
        "| 英文 | 中文 | 备注 |\n"
        "| --- | --- | --- |\n"
        "| token | 词元 | 概念 |\n\n"
        "![图](x.png) 之后普通文本。\n"
    )
    body = m.markdown_to_docx(md)
    doc = m.build_docx(body)["word/document.xml"]
    root = ET.fromstring(doc.encode("utf-8"))
    texts = [t.text or "" for t in root.iter("{%s}t" % W)]

    assert not any("`" in t for t in texts), "行内反引号应被剥离：%r" % texts
    assert "<w:tbl>" in doc, "应渲染表格"
    assert not any("!图" in t for t in texts), "图片感叹号应被去除：%r" % texts
    assert any("[32,28,28] -> [32,10]" in t for t in texts), "行内代码应保留内容"
    assert "<w:b/>" in doc, "标题/表头应加粗"

    print("PASS  md_to_docx 全部检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
