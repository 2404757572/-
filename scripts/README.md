# 脚本目录

所有脚本按分类存放，格式规范见 `docs/script-format.md`。

| 目录 | 说明 |
| --- | --- |
| `automation/` | 自动化、批处理类脚本 |
| `reverse/` | 逆向分析、二进制分析类脚本 |
| `tools/` | 通用小工具与仓库维护脚本 |

## 新增脚本

1. 复制 `templates/script-template.md` 编写说明文件
2. 按 `<名称>-v<版本>.<扩展名>` 命名脚本
3. 补齐元数据头
4. 运行校验并生成索引

```bash
# 校验脚本格式
python3 scripts/tools/check-scripts-v1.0.0.py

# 校验并更新索引
python3 scripts/tools/check-scripts-v1.0.0.py --index
```
