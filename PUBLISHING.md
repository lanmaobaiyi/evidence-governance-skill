# GitHub 发布说明

建议仓库地址：

https://github.com/lanmaobaiyi/evidence-governance-skill

## 仓库定位

这是一个低维护、通用的 Agent Skill，提供证据驱动的治理分析、制度引用、风险门禁和人工复核流程。

它不是在线产品，不连接生产数据库，不包含真实治理数据、API Key、MCP 服务或外部写入逻辑。

## 使用方式

在支持 Agent Skills 的环境中，将仓库根目录作为 Skill 使用，入口文件是 SKILL.md。

如果需要直接运行本地确定性分析：

    python scripts/run_governance_case.py --ledger input.csv --policy policy.md --output review.json

该命令只读取本地 CSV 和 Markdown 文件，输出 JSON review packet：

- 完整且非空的输入：REVIEW；
- 缺少字段、空台账、额外列、重复表头、空值、无标题制度或不可读文件：REGENERATION_REQUIRED；
- REVIEW 不代表批准、结案或已经执行外部动作。

## 发布前检查

    python scripts/validate_public_bundle.py .
    python scripts/run_examples.py
    python scripts/build_skill_zip.py --output dist/evidence-governance-final.zip

同时检查 dist/evidence-governance-final.zip.sha256 是否与 ZIP 一致。

GitHub Actions 会在 Python 3.11 和 3.12 上执行这些检查。

## GitHub 上传内容

仓库包含：

- SKILL.md；
- references/ 运行规范；
- examples/ 合成示例；
- evals/ 评估用例；
- scripts/ 执行、验证和打包脚本；
- VERSION.json、CHANGELOG.md、PROVENANCE.md；
- CONTRIBUTING.md、SECURITY.md、CODE_OF_CONDUCT.md；
- dist/ 最终 Skill ZIP 和 SHA-256 校验文件。

不要提交真实台账、制度原件、数据库、日志、账号、密码、API Key 或生产导出物。

## 版本发布

每次修改同步更新 VERSION.json 和 CHANGELOG.md。发布 ZIP 时固定 Git 提交或版本号，不要使用未固定的 latest。

