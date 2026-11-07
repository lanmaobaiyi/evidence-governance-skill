# Contributing

请保持这个仓库为低维护的通用 Skill 与运行规范知识库。

1. 不提交真实治理数据、凭据、数据库、导出报告或外部服务配置。
2. 新规则先放入 references/，并说明输入、输出、证据定位、失败状态和人工复核点。
3. 确定性文件处理可放入 scripts/，但脚本不得联网、写入外部系统或绕过人工复核。
4. 修改后运行 validate_public_bundle.py、run_examples.py，并重建 ZIP 检查 SHA-256。
5. 提交信息和文档使用清晰、可复现的描述；新版本同步更新 VERSION.json 与 CHANGELOG.md。

