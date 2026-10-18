# 脚本文件格式规范

本仓库所有脚本统一采用「元数据头 + 脚本正文」的格式，便于检索、校验和自动生成索引。

## 1. 目录结构

```text
scripts/
  automation/        自动化、批处理类脚本
  reverse/           逆向分析、二进制分析类脚本
  tools/             通用小工具
templates/
  script-template.md 脚本说明模板
docs/
  script-format.md   本规范
scripts/INDEX.md     自动生成的脚本索引
```

新增分类时，在 `scripts/` 下建立目录，并在分类目录内补充 `README.md`。

## 2. 文件命名

```text
<名称>-<版本>.<扩展名>
```

- 名称：小写字母、数字、连字符，能表达用途，例如 `batch-rename`
- 版本：语义化版本，例如 `v1.0.0`
- 扩展名：与运行时一致，`.sh` `.py` `.js` `.ps1` 等

示例：`scripts/automation/batch-rename-v1.0.0.sh`

## 3. 元数据头

脚本正文之前必须包含元数据块，用与注释符匹配的 `---` 包裹。

Bash：

```bash
#!/usr/bin/env bash
# ---
# name: batch-rename
# version: 1.0.0
# ...
# ---
```

Python 使用 `#`，JavaScript 使用 `//`，PowerShell 使用 `#`，原则是元数据块整体被注释，不影响脚本执行。

### 字段定义

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| name | 是 | 脚本名，与文件名前缀一致 |
| version | 是 | 语义化版本号 |
| description | 是 | 一句话说明用途 |
| author | 是 | 作者名称 |
| email | 是 | 联系方式 |
| created | 是 | 创建日期，格式 YYYY-MM-DD |
| language | 是 | 运行时语言 |
| runtime | 是 | 版本要求，例如 `bash>=5.0` |
| category | 是 | 所属分类，与目录名一致 |
| tags | 否 | 逗号分隔的标签 |
| usage | 是 | 调用方式 |
| dependencies | 否 | 依赖项，逗号分隔，无则填 `none` |
| disclaimer | 否 | 使用范围与风险提示 |

### 完整示例

```bash
#!/usr/bin/env bash
# ---
# name: batch-rename
# version: 1.0.0
# description: 按规则批量重命名指定目录下的文件
# author: 2404757572
# email: 2404757572@qq.com
# created: 2026-10-18
# language: bash
# runtime: bash>=4.0
# category: automation
# tags: rename,batch,filesystem
# usage: ./batch-rename-v1.0.0.sh -d <目录> -p <前缀>
# dependencies: none
# disclaimer: 仅用于自有文件，执行前请先备份
# ---
```

## 4. 正文约定

- 参数解析、错误处理、帮助信息三段结构齐全
- 危险操作（覆盖、删除、写入系统路径）必须二次确认或提供 `--force`
- 输出信息区分正常日志与错误日志
- 不在脚本中硬编码账号、密钥、令牌

## 5. 配套文件

每个脚本可附带一个同名说明文件，内容参考 `templates/script-template.md`：

```text
scripts/automation/batch-rename-v1.0.0.sh
scripts/automation/batch-rename-v1.0.0.md
```

需要外部配置时，提供 `.example` 配置文件，真实配置通过 `.gitignore` 排除。

## 6. 校验与索引

提交前运行校验脚本：

```bash
python3 scripts/tools/check-scripts-v1.0.0.py
```

校验内容包括元数据字段完整性、必填字段格式、分类目录匹配、文件名版本格式。校验通过后运行索引生成脚本，更新 `scripts/INDEX.md`。

## 7. 发布流程

1. 按规范编写脚本，补齐元数据头
2. 附上说明文件与示例配置
3. 本地运行校验脚本
4. 生成并检查索引
5. 提交并推送
