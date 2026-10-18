#!/usr/bin/env python3
# ---
# name: check-scripts
# version: 1.0.0
# description: 校验脚本元数据头与文件命名，并可生成脚本索引
# author: 2404757572
# email: 2404757572@qq.com
# created: 2026-10-18
# language: python
# runtime: python>=3.8
# category: tools
# tags: validate,index,metadata
# usage: python3 check-scripts-v1.0.0.py [--index]
# dependencies: none
# disclaimer: 无
# ---
import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCAN_DIRS = [ROOT / "scripts"]

REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "author",
    "email",
    "created",
    "language",
    "runtime",
    "category",
    "usage",
]

FILENAME_RE = re.compile(r"^(?P<name>[a-z0-9][a-z0-9-]*)-v(?P<version>\d+\.\d+\.\d+)\.(?P<ext>[a-z0-9]+)$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MARKER_RE = re.compile(r"^\s*(?:#|//)\s*---\s*$")
FIELD_RE = re.compile(r"^\s*(?:#|//)\s*([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.*)$")

SKIP_NAMES = {"README.md", "INDEX.md"}


def parse_metadata(path):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    start = None
    for index, line in enumerate(lines):
        if MARKER_RE.match(line):
            start = index
            break
    if start is None:
        return {}

    meta = {}
    for line in lines[start + 1:]:
        if MARKER_RE.match(line):
            return meta
        field = FIELD_RE.match(line)
        if field:
            meta[field.group(1)] = field.group(2).strip()
    return {}


def validate(path):
    errors = []
    meta = parse_metadata(path)

    if not meta:
        return ["缺少元数据头"], meta

    for field in REQUIRED_FIELDS:
        if not meta.get(field):
            errors.append(f"缺少必填字段: {field}")

    filename = FILENAME_RE.match(path.name)
    if not filename:
        errors.append("文件名不符合 <名称>-v<版本>.<扩展名> 格式")
    else:
        if meta.get("name") and meta["name"] != filename.group("name"):
            errors.append("元数据 name 与文件名不一致")
        if meta.get("version") and meta["version"] != filename.group("version"):
            errors.append("元数据 version 与文件名版本不一致")

    if meta.get("version") and not VERSION_RE.match(meta["version"]):
        errors.append("version 需为 x.y.z 格式")

    created = meta.get("created")
    if created:
        if not DATE_RE.match(created):
            errors.append("created 需为 YYYY-MM-DD 格式")
        else:
            try:
                datetime.date.fromisoformat(created)
            except ValueError:
                errors.append("created 不是有效日期")

    email = meta.get("email")
    if email and not EMAIL_RE.match(email):
        errors.append("email 格式不正确")

    category = meta.get("category")
    if category and category != path.parent.name:
        errors.append(f"category 与所在目录不一致: {path.parent.name}")

    usage = meta.get("usage", "")
    if usage and not (usage.startswith("./") or usage.startswith("python") or usage.startswith("bash") or usage.startswith("node")):
        errors.append("usage 需以可执行命令开头")

    return errors, meta


def collect():
    files = []
    for base in SCAN_DIRS:
        if not base.exists():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            if path.name in SKIP_NAMES or path.name.startswith("."):
                continue
            if path.suffix == ".md":
                continue
            files.append(path)
    return files


def build_index(entries):
    lines = [
        "# 脚本索引",
        "",
        "本文件由 `scripts/tools/check-scripts-v1.0.0.py --index` 自动生成，请勿手工修改。",
        "",
        "| 名称 | 版本 | 分类 | 语言 | 说明 | 作者 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for meta, rel in entries:
        desc = meta.get("description", "").replace("|", "\\|")
        link = Path(rel).relative_to("scripts").as_posix()
        lines.append(
            "| [{name}]({rel}) | {version} | {category} | {language} | {desc} | {author} |".format(
                name=meta.get("name", ""),
                rel=link,
                version=meta.get("version", ""),
                category=meta.get("category", ""),
                language=meta.get("language", ""),
                desc=desc,
                author=meta.get("author", ""),
            )
        )
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="校验脚本格式并生成索引")
    parser.add_argument("--index", action="store_true", help="生成 scripts/INDEX.md")
    args = parser.parse_args()

    files = collect()
    if not files:
        print("未找到待校验的脚本")
        return 1

    total_errors = 0
    entries = []
    for path in files:
        errors, meta = validate(path)
        rel = path.relative_to(ROOT).as_posix()
        if errors:
            total_errors += len(errors)
            print(f"[失败] {rel}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[通过] {rel}")
            entries.append((meta, rel))

    print(f"\n共检查 {len(files)} 个文件，失败 {total_errors} 项")

    if args.index and entries:
        entries.sort(key=lambda item: (item[0].get("category", ""), item[0].get("name", "")))
        index_path = ROOT / "scripts" / "INDEX.md"
        index_path.write_text(build_index(entries), encoding="utf-8")
        print(f"索引已更新: {index_path.relative_to(ROOT)}")

    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
