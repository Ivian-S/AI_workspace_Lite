# AI Workspace Lite

AI Workspace Lite 是一个从零开始、逐步演进的 Python 后端工程学习项目。项目从 CLI 项目管理器起步，后续依次引入 Web API、数据库分层、Docker、LLM、Tool Calling、Workflow 和 RAG，最终形成可演示、可部署的 AI 项目助手。

## 当前进度

项目当前处于 **M1｜Python 工程化地基**：

- 已完成：M1-T01 ～ M1-T04；
- 当前成果：`Project` 数据模型、Service / Storage 最小分层、内存存储、查询能力及 19 个测试；
- 下一任务：**M1-T05｜模块、包与 Import 排错**；
- 当前入口只输出应用名称和版本，完整 CLI CRUD 与 JSON 持久化尚未实现。

详细的最新快照见 [`learning_records/summary.md`](learning_records/summary.md)，完整路线见 [`StudyPLAN.md`](StudyPLAN.md)。

## 已实现内容

- 使用 `dataclass` 定义 `Project`，包含名称、描述、标签和成员；
- 通过 `ProjectService` 创建、列出和按名称查询项目；
- 使用 `InMemoryProjectStorage` 保存运行期数据；
- 隔离调用方输入列表和 Storage 内部列表，降低意外共享可变状态的风险；
- 使用 pytest 覆盖应用冒烟、对象引用、复制、状态隔离和 Service / Storage 行为。

当前核心数据流：

```text
调用方 → ProjectService → Project + InMemoryProjectStorage
```

## 项目结构

```text
project/
├── app/
│   ├── __init__.py          # 应用名称
│   ├── info.py              # 应用版本
│   ├── main.py              # 当前入口
│   ├── models.py            # Project 数据模型
│   ├── project_state.py     # 对象引用与复制学习实验
│   ├── services.py          # 业务动作
│   └── storage.py           # 内存存储
├── tests/
│   ├── test_smoke.py
│   ├── test_project_state.py
│   └── test_services.py
├── learning_records/        # 原子任务验收记录和进度摘要
├── AGENTS.md                # 仓库协作指南
├── StudyPLAN.md             # M1～M8 学习计划
├── pyproject.toml           # 项目与依赖配置
└── README.md
```

`exceptions.py`、JSON Storage、API 路由和数据库等文件会在对应任务引入，目前不属于已实现结构。

## 环境与运行

要求 Python 3.11 或更高版本。在仓库根目录执行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"

python -m app.main
python -m pytest -q
```

当前入口预期输出：

```text
AI Workspace Lite started. 0.1.0
```

截至 2026-08-25，仓库虚拟环境中的全量测试结果为：

```text
19 passed
```

如果系统没有 `python` 命令，可激活项目虚拟环境，或直接使用 `.venv/bin/python` 执行上述模块。

## M1 任务状态

| 任务 | 状态 | 产出 |
| --- | --- | --- |
| M1-T01 工程骨架 | 已完成 | 包结构、项目配置、入口和冒烟测试 |
| M1-T02 对象引用与可变对象 | 已完成 | 引用、复制和状态隔离实验 |
| M1-T03 函数、类型注解与数据模型 | 已完成 | `Project` dataclass 与类型化函数 |
| M1-T04 类、组合与模块职责 | 已完成 | Model / Service / Storage 最小拆分 |
| M1-T05 模块、包与 Import 排错 | 下一步 | 绝对导入、搜索路径和循环导入 |
| M1-T06 异常处理与业务异常 | 待开始 | 具体异常与自定义业务异常 |
| M1-T07 JSON 持久化项目管理器 | 待开始 | CLI CRUD 与 JSON 读写 |
| M1-T08 pytest + Debugger + Git 基线 | 待开始 | M1 综合验收 |

## 总体路线

| 周期 | 里程碑 | 目标形态 |
| --- | --- | --- |
| Week 1–2 | M1 Python 工程化地基 | CLI 项目管理器 |
| Week 3–4 | M2 HTTP + FastAPI | Web API |
| Week 5–8 | M3 数据库、分层与权限 | Workspace 后端 |
| Week 9–12 | M4 Linux + Docker | 可部署 Workspace |
| Week 13–15 | M5 LLM 服务集成 | AI Workspace |
| Week 16 | M6 Tool Calling | 可安全操作 Workspace 的 AI |
| Week 17–19 | M7 Workflow + RAG | AI 项目助手 |
| Week 20 | M8 工程收口 | 可演示、可部署、可面试项目 |

## 学习与记录约定

- 按 `StudyPLAN.md` 中的原子任务顺序推进，不提前堆叠后续技术；
- 功能变更同时覆盖成功路径和预期失败路径；
- 每完成一个 `Mx-Txx`，先写入 `learning_records/`，再更新进度摘要；
- 每次提交保持聚焦，并采用 `feat:`、`fix:`、`test:`、`docs:`、`chore:` 等 Conventional Commit 前缀。

## 许可

仅供个人学习使用。
