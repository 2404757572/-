# 贡献指南

## 提交脚本

1. 选择分类目录：`scripts/automation/`、`scripts/reverse/` 或 `scripts/tools/`
2. 按 `<名称>-v<版本>.<扩展名>` 命名文件
3. 在正文前补齐元数据头，字段说明见 `docs/script-format.md`
4. 复制 `templates/script-template.md` 编写同名 `.md` 说明文件
5. 运行校验并更新索引

```bash
# 校验格式并生成索引
python3 scripts/tools/check-scripts-v1.0.0.py --index
```

## 代码要求

- 参数解析、错误处理、帮助信息齐全
- 危险操作提供确认或 `--force` 开关
- 不硬编码账号、密钥、令牌
- 不提交运行产物与本地配置

## 提交信息

采用 `类型: 简述` 格式，类型取 `feat`、`fix`、`docs`、`refactor`、`chore`。

示例：`feat: 新增 file-hash 脚本`

## 交流

问题反馈与技术讨论可通过 Issue 或邮箱 2404757572@qq.com 联系。
