from __future__ import annotations

import copy
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

from lxml import etree


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "新模板.docx"
SOURCE = ROOT / "AI伪造图像识别论文_终稿_按意见补充版.docx"
OUTPUT = ROOT / "AI伪造图像识别论文_终稿_按新模板格式_最终版.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

NS = {"w": W_NS, "r": R_NS, "rel": PKG_REL_NS, "ct": CT_NS}


def unzip_docx(path: Path, target: Path) -> None:
    with zipfile.ZipFile(path, "r") as zf:
        zf.extractall(target)


def zip_dir(src_dir: Path, out_path: Path) -> None:
    if out_path.exists():
        out_path.unlink()
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(src_dir.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(src_dir).as_posix())


def parse_xml(path: Path) -> etree._ElementTree:
    return etree.parse(str(path))


def style_name_map(styles_path: Path) -> dict[str, str]:
    """返回 style 名称到 styleId 的映射，便于把源文档样式映射到模板样式。"""
    tree = parse_xml(styles_path)
    mapping: dict[str, str] = {}
    for style in tree.xpath("//w:style", namespaces=NS):
        style_id = style.get(f"{{{W_NS}}}styleId")
        name_el = style.find("w:name", namespaces=NS)
        if style_id and name_el is not None:
            name = name_el.get(f"{{{W_NS}}}val")
            if name:
                mapping[name] = style_id
    return mapping


def rels_by_id(rels_path: Path) -> dict[str, etree._Element]:
    if not rels_path.exists():
        return {}
    tree = parse_xml(rels_path)
    result = {}
    for rel in tree.getroot().findall(f"{{{PKG_REL_NS}}}Relationship"):
        rid = rel.get("Id")
        if rid:
            result[rid] = rel
    return result


def next_rid(existing_ids: set[str]) -> str:
    nums = []
    for rid in existing_ids:
        m = re.fullmatch(r"rId(\d+)", rid or "")
        if m:
            nums.append(int(m.group(1)))
    n = max(nums, default=0) + 1
    while f"rId{n}" in existing_ids:
        n += 1
    existing_ids.add(f"rId{n}")
    return f"rId{n}"


def collect_relation_ids(root: etree._Element) -> set[str]:
    """收集文档正文中实际引用到的 rId，避免复制未使用关系。"""
    used = set()
    for el in root.iter():
        for attr_name, attr_val in el.attrib.items():
            if attr_name in {
                f"{{{R_NS}}}id",
                f"{{{R_NS}}}embed",
                f"{{{R_NS}}}link",
            }:
                used.add(attr_val)
    return used


def add_default_content_type(content_types_path: Path, extension: str, content_type: str) -> None:
    tree = parse_xml(content_types_path)
    root = tree.getroot()
    for default in root.findall(f"{{{CT_NS}}}Default"):
        if (default.get("Extension") or "").lower() == extension.lower():
            return
    el = etree.Element(f"{{{CT_NS}}}Default")
    el.set("Extension", extension)
    el.set("ContentType", content_type)
    root.append(el)
    tree.write(str(content_types_path), encoding="UTF-8", xml_declaration=True, standalone=True)


def media_content_type(ext: str) -> str | None:
    ext = ext.lower().lstrip(".")
    return {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "bmp": "image/bmp",
        "emf": "image/x-emf",
        "wmf": "image/x-wmf",
    }.get(ext)


def text_of_p(p: etree._Element) -> str:
    return "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()


def p_style_el(p: etree._Element) -> etree._Element:
    p_pr = p.find("w:pPr", namespaces=NS)
    if p_pr is None:
        p_pr = etree.Element(f"{{{W_NS}}}pPr")
        p.insert(0, p_pr)
    p_style = p_pr.find("w:pStyle", namespaces=NS)
    if p_style is None:
        p_style = etree.Element(f"{{{W_NS}}}pStyle")
        p_pr.insert(0, p_style)
    return p_style


def set_p_style(p: etree._Element, style_id: str) -> None:
    p_style_el(p).set(f"{{{W_NS}}}val", style_id)


def remove_direct_body_formatting(p: etree._Element) -> None:
    """让正文段落更多继承模板样式，保留内容但减少源文档直接格式干扰。"""
    p_pr = p.find("w:pPr", namespaces=NS)
    if p_pr is None:
        p_pr = etree.Element(f"{{{W_NS}}}pPr")
        p.insert(0, p_pr)
    for tag in ["w:ind", "w:spacing", "w:jc"]:
        el = p_pr.find(tag, namespaces=NS)
        if el is not None:
            p_pr.remove(el)
    # 源稿中部分正文段落存在直接字号/字体设置，套用模板时会覆盖模板样式。
    # 清理普通正文 run 级格式，让它们继承模板的正文样式；文字内容不变。
    for run in p.findall("w:r", namespaces=NS):
        r_pr = run.find("w:rPr", namespaces=NS)
        if r_pr is not None:
            run.remove(r_pr)


def in_table(p: etree._Element) -> bool:
    parent = p.getparent()
    while parent is not None:
        if parent.tag == f"{{{W_NS}}}tc":
            return True
        parent = parent.getparent()
    return False


def remap_paragraph_styles(body: etree._Element, source_styles: dict[str, str], template_styles: dict[str, str]) -> None:
    reverse_source = {v: k for k, v in source_styles.items()}
    source_to_template = {
        source_styles.get("heading 1"): template_styles.get("heading 1"),
        source_styles.get("heading 2"): template_styles.get("heading 2"),
        source_styles.get("heading 3"): template_styles.get("heading 3"),
        source_styles.get("heading 4"): template_styles.get("heading 4"),
        source_styles.get("caption"): template_styles.get("caption"),
        source_styles.get("toc 1"): template_styles.get("toc 1"),
        source_styles.get("toc 2"): template_styles.get("toc 2"),
        source_styles.get("toc 3"): template_styles.get("toc 3"),
        source_styles.get("TOC Heading"): template_styles.get("普通标题"),
        source_styles.get("普通标题"): template_styles.get("普通标题"),
    }
    source_to_template = {k: v for k, v in source_to_template.items() if k and v}

    normal_style = template_styles.get("Normal", template_styles.get("normal", "Normal"))
    body_style = template_styles.get("Body Text First Indent 2", normal_style)

    in_main_body = False
    for p in body.xpath(".//w:p", namespaces=NS):
        style_el = p.find("w:pPr/w:pStyle", namespaces=NS)
        old_style = style_el.get(f"{{{W_NS}}}val") if style_el is not None else None
        para_text = text_of_p(p)

        if old_style in source_to_template:
            set_p_style(p, source_to_template[old_style])
            if reverse_source.get(old_style, "").lower().startswith("heading 1") and para_text == "绪论":
                in_main_body = True
            continue

        style_name = reverse_source.get(old_style, "Normal")
        is_normal = old_style is None or style_name == "Normal"

        if is_normal:
            if in_table(p) or not in_main_body or not para_text:
                set_p_style(p, normal_style)
            else:
                set_p_style(p, body_style)
                remove_direct_body_formatting(p)
        elif old_style and old_style in source_to_template:
            set_p_style(p, source_to_template[old_style])

        if para_text == "绪论":
            in_main_body = True


def update_relation_refs(root: etree._Element, rid_map: dict[str, str]) -> None:
    for el in root.iter():
        for attr_name in list(el.attrib):
            if attr_name in {
                f"{{{R_NS}}}id",
                f"{{{R_NS}}}embed",
                f"{{{R_NS}}}link",
            }:
                old = el.attrib[attr_name]
                if old in rid_map:
                    el.attrib[attr_name] = rid_map[old]


def merge_document_relationships(src_dir: Path, dst_dir: Path, document_root: etree._Element) -> None:
    src_rels_path = src_dir / "word" / "_rels" / "document.xml.rels"
    dst_rels_path = dst_dir / "word" / "_rels" / "document.xml.rels"
    src_rels = rels_by_id(src_rels_path)
    dst_tree = parse_xml(dst_rels_path)
    dst_root = dst_tree.getroot()
    existing_ids = {rel.get("Id") for rel in dst_root.findall(f"{{{PKG_REL_NS}}}Relationship")}
    existing_ids = {rid for rid in existing_ids if rid}

    used_rids = collect_relation_ids(document_root)
    rid_map: dict[str, str] = {}

    for old_rid in sorted(used_rids):
        rel = src_rels.get(old_rid)
        if rel is None:
            continue
        new_rid = next_rid(existing_ids)
        rid_map[old_rid] = new_rid

        new_rel = copy.deepcopy(rel)
        new_rel.set("Id", new_rid)
        target = rel.get("Target") or ""
        mode = rel.get("TargetMode")
        if mode != "External" and target.startswith("media/"):
            src_media = src_dir / "word" / target
            dst_media_dir = dst_dir / "word" / "media"
            dst_media_dir.mkdir(exist_ok=True)
            new_name = f"copied_{old_rid}_{Path(target).name}"
            dst_media = dst_media_dir / new_name
            shutil.copy2(src_media, dst_media)
            new_rel.set("Target", f"media/{new_name}")
            content_type = media_content_type(Path(new_name).suffix)
            if content_type:
                add_default_content_type(dst_dir / "[Content_Types].xml", Path(new_name).suffix.lstrip("."), content_type)
        dst_root.append(new_rel)

    update_relation_refs(document_root, rid_map)
    dst_tree.write(str(dst_rels_path), encoding="UTF-8", xml_declaration=True, standalone=True)


def replace_document_body(src_dir: Path, dst_dir: Path) -> None:
    src_doc_path = src_dir / "word" / "document.xml"
    dst_doc_path = dst_dir / "word" / "document.xml"
    src_tree = parse_xml(src_doc_path)
    dst_tree = parse_xml(dst_doc_path)

    src_body = src_tree.getroot().find("w:body", namespaces=NS)
    dst_body = dst_tree.getroot().find("w:body", namespaces=NS)
    if src_body is None or dst_body is None:
        raise RuntimeError("DOCX document.xml 缺少 body。")

    # 保留模板最终 sectPr，以继承模板页面边距、纸张和页眉页脚设置。
    dst_sect = dst_body.find("w:sectPr", namespaces=NS)
    dst_sect_copy = copy.deepcopy(dst_sect) if dst_sect is not None else None

    for child in list(dst_body):
        dst_body.remove(child)

    copied_children = []
    for child in list(src_body):
        if child.tag == f"{{{W_NS}}}sectPr":
            continue
        copied_children.append(copy.deepcopy(child))
    for child in copied_children:
        dst_body.append(child)

    template_styles = style_name_map(dst_dir / "word" / "styles.xml")
    source_styles = style_name_map(src_dir / "word" / "styles.xml")
    remap_paragraph_styles(dst_body, source_styles, template_styles)
    merge_document_relationships(src_dir, dst_dir, dst_body)

    # 关系合并完成后再恢复模板 sectPr，避免把模板页眉页脚 rId
    # 误当作源文档 rId 复制，造成重复关系或缺失部件。
    if dst_sect_copy is not None:
        dst_body.append(dst_sect_copy)

    dst_tree.write(str(dst_doc_path), encoding="UTF-8", xml_declaration=True, standalone=True)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="paper_template_") as tmp:
        tmp_path = Path(tmp)
        src_dir = tmp_path / "source"
        dst_dir = tmp_path / "template"
        unzip_docx(SOURCE, src_dir)
        unzip_docx(TEMPLATE, dst_dir)
        replace_document_body(src_dir, dst_dir)
        zip_dir(dst_dir, OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()
