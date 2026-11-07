# Evidence Governance Skill

一个低维护、通用的 Agent Skill 与运行规范知识库：把结构化治理记录和制度 Markdown 转成可追溯、可复核的本地 review packet。它源自“骑行智治”项目的工程经验，但不绑定骑行、城市、Provider、数据库或具体业务系统。

## 它是什么

这是“规范 + 可重复本地执行器”的组合：

- SKILL.md 规定准入、证据快照、确定性分析、引用、风险门禁、人工复核和降级流程；
- references/ 保存可按需读取的任务契约、运行规范和失败边界；
- scripts/run_governance_case.py 接受 CSV 台账与 Markdown 制度，生成带 SHA-256、统计、标题引用、建议和未决事项的 JSON review packet；
- scripts/validate_public_bundle.py、scripts/run_examples.py 和 CI 负责发布前的确定性检查。

它不是在线产品、服务端或自动处置系统。包内不连接数据源，不包含真实数据、API Key、数据库、FastAPI、React 或 MCP 服务。需要实时数据、认证或外部动作时，应由宿主 Agent 的工具/MCP 提供；本 Skill 不得宣称已经派单、关单、收费、授权或完成治理动作。

## 适用范围

- 治理台账统计和记录质量检查；
- 制度条款提取与适用范围分析；
- 记录与制度的证据匹配；
- 风险研判和待核实事项整理；
- 生成带责任人、步骤和验收标准的行动建议。

骑行治理只作为合成示例领域。输入可以是任何具有 event_type、location 字段的 CSV，以及可引用的 Markdown 制度文件；其他字段只在输入表头和来源清单中可见；执行器不复制原始行，也不会擅自解释未知字段。

## 快速运行

在仓库根目录执行：

    python scripts/run_governance_case.py --ledger examples/synthetic-ledger.csv --policy examples/synthetic-policy.md --output review.json

完整且可解析且非空的输入输出 terminal_state: REVIEW；缺少必填字段、空值、额外列、重复表头、空台账、无法读取的文件或无可引用 Markdown 标题输出 REGENERATION_REQUIRED，并以非零状态退出。脚本也拒绝用输出文件覆盖输入文件。REVIEW 表示已生成可供人审的确定性结果，不表示已批准或已完成。

## 目录

- SKILL.md：唯一 Skill 入口；
- references/：按需读取的运行规范和任务契约；
- examples/：不含真实数据的合成示例；
- evals/：触发、拒绝、证据不足和人工复核用例；
- scripts/：无依赖的确定性执行、验证与打包脚本；
- .github/workflows/validate.yml：公开仓库 CI。

## 发布前检查

    python scripts/validate_public_bundle.py .
    python scripts/run_examples.py
    python scripts/run_governance_case.py --ledger examples/synthetic-ledger.csv --policy examples/synthetic-policy.md --output review.json
    python scripts/build_skill_zip.py --output ../evidence-governance-final.zip

review.json 是临时输出，不应提交到仓库。发布时请固定 Git 提交或 Skill 版本，不要依赖 latest。官方 Skill 规范要求唯一的 SKILL.md 与单一顶层 ZIP 目录；本包同时用本地 validator、示例执行、ZIP CRC 和重复构建 SHA-256 做检查。当前环境未安装官方 skills-ref，因此不宣称已经运行它。

## 来源与许可

规范来自已清理的本地治理智能体项目，并经过通用化；骑行示例为合成内容。设计边界参考 PROVENANCE.md 和 LICENSE。


