#!/usr/bin/env bash
# ---
# name: batch-rename
# version: 1.0.0
# description: 按规则为指定目录下的文件批量添加前缀或替换扩展名
# author: 2404757572
# email: 2404757572@qq.com
# created: 2026-10-18
# language: bash
# runtime: bash>=4.0
# category: automation
# tags: rename,batch,filesystem
# usage: ./batch-rename-v1.0.0.sh -d <目录> [-p <前缀>] [-e <新扩展名>] [--force]
# dependencies: none
# disclaimer: 仅用于自有文件，执行前请先备份
# ---
set -euo pipefail

TARGET_DIR=""
PREFIX=""
NEW_EXT=""
FORCE=0

usage() {
    cat <<'EOF'
用法: batch-rename-v1.0.0.sh -d <目录> [-p <前缀>] [-e <新扩展名>] [--force]

  -d <目录>       要处理的目录，必填
  -p <前缀>       为文件名添加前缀
  -e <新扩展名>   替换文件扩展名，例如 txt
  --force         跳过确认直接执行
  -h              显示帮助
EOF
}

log() {
    printf '[信息] %s\n' "$*"
}

err() {
    printf '[错误] %s\n' "$*" >&2
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        -d)
            TARGET_DIR="${2:-}"
            shift 2
            ;;
        -p)
            PREFIX="${2:-}"
            shift 2
            ;;
        -e)
            NEW_EXT="${2:-}"
            shift 2
            ;;
        --force)
            FORCE=1
            shift
            ;;
        -h)
            usage
            exit 0
            ;;
        *)
            err "未知参数: $1"
            usage
            exit 2
            ;;
    esac
done

if [[ -z "$TARGET_DIR" ]]; then
    err "必须指定目录 -d"
    usage
    exit 2
fi

if [[ ! -d "$TARGET_DIR" ]]; then
    err "目录不存在: $TARGET_DIR"
    exit 2
fi

if [[ -z "$PREFIX" && -z "$NEW_EXT" ]]; then
    err "至少指定 -p 或 -e 其中一项"
    exit 2
fi

if [[ -n "$NEW_EXT" ]]; then
    NEW_EXT="${NEW_EXT#.}"
fi

shopt -s nullglob
files=("$TARGET_DIR"/*)
shopt -u nullglob

if [[ ${#files[@]} -eq 0 ]]; then
    log "目录中没有文件，结束"
    exit 0
fi

plan=()
for src in "${files[@]}"; do
    [[ -f "$src" ]] || continue
    base="$(basename "$src")"
    stem="$base"
    ext=""
    if [[ "$base" == *.* && "$base" != .* ]]; then
        stem="${base%.*}"
        ext="${base##*.}"
    fi
    if [[ -n "$NEW_EXT" ]]; then
        ext="$NEW_EXT"
    fi
    name="${PREFIX}${stem}"
    if [[ -n "$ext" ]]; then
        dst="$TARGET_DIR/${name}.${ext}"
    else
        dst="$TARGET_DIR/${name}"
    fi
    if [[ "$src" == "$dst" ]]; then
        continue
    fi
    if [[ -e "$dst" ]]; then
        err "目标已存在，跳过: $dst"
        continue
    fi
    plan+=("$src|$dst")
done

if [[ ${#plan[@]} -eq 0 ]]; then
    log "没有需要重命名的文件"
    exit 0
fi

log "计划重命名 ${#plan[@]} 个文件"
for item in "${plan[@]}"; do
    printf '  %s -> %s\n' "${item%%|*}" "${item##*|}"
done

if [[ $FORCE -ne 1 ]]; then
    printf '确认执行? [y/N] '
    read -r answer
    case "$answer" in
        y|Y) ;;
        *) log "已取消"; exit 0 ;;
    esac
fi

count=0
for item in "${plan[@]}"; do
    src="${item%%|*}"
    dst="${item##*|}"
    mv -- "$src" "$dst"
    count=$((count + 1))
done

log "完成，共重命名 $count 个文件"
