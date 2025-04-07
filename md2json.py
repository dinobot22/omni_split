from mistletoe import Document
from mistletoe.block_token import Heading, Paragraph, BlockCode, List, ListItem, Quote, Table, TableRow, TableCell, ThematicBreak
from mistletoe.span_token import Strong, Emphasis, Link, Image, RawText
import json
import re




def md_to_json_list(md_content):
    # 解析Markdown为AST
    doc = Document(md_content)

    result = []

    # 遍历AST中的每个节点
    for child in doc.children:
        # 处理标题
        if isinstance(child, Heading):
            level = child.level
            content = get_inline_md(child.children) if hasattr(child, "children") and child.children else ""
            result.append({"content": content, "type": f"head{level}"})

        # 处理段落
        elif isinstance(child, Paragraph):
            # 检查是否是独立的图片
            if hasattr(child, "children") and child.children and len(child.children) == 1 and isinstance(child.children[0], Image):
                img = child.children[0]
                result.append({"content": {"src": img.src if hasattr(img, "src") else "", "title": img.title if hasattr(img, "title") else "", "description": img.title if hasattr(img, "title") else ""}, "type": "image"})
            else:
                content = get_inline_md(child.children) if hasattr(child, "children") and child.children else ""
                result.append({"content": content, "type": "paragraph"})

        # 处理代码块
        elif isinstance(child, BlockCode):
            code_content = child.children[0].content if hasattr(child, "children") and child.children and len(child.children) > 0 else ""
            result.append({"content": code_content, "type": "code", "language": child.language if hasattr(child, "language") else ""})

        # 处理列表
        elif isinstance(child, List):
            items = []
            if hasattr(child, "children") and child.children:
                for item in child.children:
                    if isinstance(item, ListItem):
                        item_content = get_inline_md(item.children) if hasattr(item, "children") and item.children else ""
                        items.append(item_content)

            result.append({"content": items, "type": "list", "ordered": child.start is not None if hasattr(child, "start") else False})

        # 处理引用
        elif isinstance(child, Quote):
            content = get_inline_md(child.children) if hasattr(child, "children") and child.children else ""
            result.append({"content": content, "type": "quote"})

        # 处理表格
        elif isinstance(child, Table):

            table_content = ""
            if hasattr(child, "children") and child.children:
                # 重建表格的Markdown表示
                if hasattr(child, "header") and child.header:
                    header_row = child.header
                    if hasattr(header_row, "children") and header_row.children:
                        table_content += "| " + " | ".join(get_inline_md(cell.children) if hasattr(cell, "children") else "" for cell in header_row.children if isinstance(cell, TableCell)) + " |\n"
                        table_content += "| " + " | ".join(["---"] * len(header_row.children)) + " |\n"

                for row in child.children[1:] if hasattr(child, "children") else []:
                    if isinstance(row, TableRow) and hasattr(row, "children") and row.children:
                        table_content += "| " + " | ".join(get_inline_md(cell.children) if hasattr(cell, "children") else "" for cell in row.children if isinstance(cell, TableCell)) + " |\n"

            result.append({"content": table_content.strip(), "type": "table"})
        # 处理分隔线
        elif isinstance(child, ThematicBreak):
            result.append({"content": "---", "type": "thematic_break"})

        # 处理数学公式块
        elif is_math_block(child):
            content = child.children[0].content.strip() if hasattr(child, "children") and child.children and len(child.children) > 0 else ""
            result.append({"content": content, "type": "math_block"})

    return result


def get_inline_md(tokens):
    """获取行内元素的Markdown表示"""
    if not tokens:
        return ""

    md = ""
    for token in tokens:
        if isinstance(token, RawText):
            md += token.content if hasattr(token, "content") else ""
        elif isinstance(token, Strong):
            md += f"**{get_inline_md(token.children) if hasattr(token, 'children') else ''}**"
        elif isinstance(token, Emphasis):
            md += f"*{get_inline_md(token.children) if hasattr(token, 'children') else ''}*"
        elif isinstance(token, Link):
            md += f"[{get_inline_md(token.children) if hasattr(token, 'children') else ''}]({token.target if hasattr(token, 'target') else ''})"
        elif isinstance(token, Image):
            md += f"![{token.title if hasattr(token, 'title') else ''}]({token.src if hasattr(token, 'src') else ''})"
        elif is_math_inline(token):
            content = token.children[0].content if hasattr(token, "children") and token.children and len(token.children) > 0 else ""
            md += f"${content}$"
        elif hasattr(token, "children"):
            md += get_inline_md(token.children) if token.children else ""
    return md


def is_math_block(token):
    """检查是否是数学公式块"""
    if isinstance(token, Paragraph) and hasattr(token, "children") and token.children and len(token.children) == 1:
        content = token.children[0].content.strip() if hasattr(token.children[0], "content") else ""
        return isinstance(token.children[0], RawText) and content.startswith("$$") and content.endswith("$$")
    return False


def is_math_inline(token):
    """检查是否是行内数学公式"""
    if isinstance(token, RawText):
        content = token.content.strip() if hasattr(token, "content") else ""
        return content.startswith("$") and content.endswith("$") and len(content) > 1
    return False


if __name__ == "__main__":
    print("main function invoke")
    with open("/media/disk0/xzzn_data_all/yinyabo/pollux_project_new/omni_split/test/c8d4614affc19ba92d7ba0671fd709803d0488a0c5a68bc237783a8af39fe32e/1c7fbb26-1012-4b03-894c-69ab2257985c_1743677710.4311144.md", "r") as f:
        md_content = f.read()

    json_list = md_to_json_list(md_content)
    print(json.dumps(json_list, indent=4, ensure_ascii=False))
