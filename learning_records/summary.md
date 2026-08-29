# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-08-29
>
> 当前阶段：M1 Python 工程化地基
>
> 正式进度：M1-T01 ～ M1-T07 已完成，下一任务为 M1-T08

本文只保存便于接手项目的最新快照。各任务的学习过程、代码片段、Code Review 和完整验收记录，以同目录下的 `M1-Txx.md` 为准。

## 任务进度

| 任务 | 状态 | 完成日期 | 主要结果 | 详细记录 |
| --- | --- | --- | --- | --- |
| M1-T01 工程骨架 | 已完成 | 2026-08-09 | 建立 `app/`、`tests/`、`pyproject.toml`、应用入口和冒烟测试 | [`M1-T01.md`](M1-T01.md) |
| M1-T02 对象引用与可变对象 | 已完成 | 2026-08-10 | 实践引用、原地修改、浅复制和状态隔离 | [`M1-T02.md`](M1-T02.md) |
| M1-T03 函数、类型注解与数据模型 | 已完成 | 2026-08-11 | 用 `dataclass` 建立 `Project`，补充类型注解和回归测试 | [`M1-T03.md`](M1-T03.md) |
| M1-T04 类、组合与模块职责 | 已完成 | 2026-08-25 | 初步拆分 Model / Service / Storage，实现内存存储和按名称查询 | [`M1-T04.md`](M1-T04.md) |
| M1-T05 模块、包与 Import 排错 | 已完成 | 2026-08-26 | 验证模块启动与脚本启动差异，掌握 `sys.path`、`__file__`、`find_spec()` 和循环导入基础排错 | [`M1-T05.md`](M1-T05.md) |
| M1-T06 异常处理与业务异常 | 已完成 | 2026-08-27 | 新增 `ProjectNotFoundError`，将 Service 查询失败从 `None` 演进为明确业务异常，并使用 `pytest.raises()` 验证 | [`M1-T06.md`](M1-T06.md) |
| M1-T07 JSON 持久化项目管理器 | 已完成 | 2026-08-29 | 新增 JSON Storage、完整 Project CRUD、CLI、持久化/异常边界及集成测试 | [`M1-T07.md`](M1-T07.md) |
| M1-T08 pytest + Debugger + Git 基线 | 待开始 | — | M1 综合测试、断点调试、Git diff/commit 与里程碑验收 | `StudyPLAN.md` |

## 当前可用能力

- `Project` 使用 `dataclass` 表达项目数据，字段为 `name`、`description`、`tags` 和 `members`。
- `ProjectService` 支持创建、列出、按名称查询、完整替换更新和删除 Project。
- 创建 Project 时复制调用方传入的 `tags` 和 `members`，避免列表引用被意外共享。
- `InMemoryProjectStorage` 保留进程内存储语义，并支持 CRUD。
- `JsonProjectStorage` 可将 Project 持久化到 JSON 文件，并在新的 Storage 实例或新的 Python 进程中重新加载。
- JSON 文件不存在或为空时按空集合处理；非法 JSON / 非法数据结构抛出 `ProjectStorageDataError`。
- 重复 Project 名称由 Service 抛出 `ProjectAlreadyExistsError`。
- Project 不存在时，Storage 返回查询事实，Service 转换为 `ProjectNotFoundError`。
- `python -m app.main` 已演进为 CLI 入口，支持 `create / list / get / update / delete`。
- CLI 支持 `--description`、重复 `--tag`、重复 `--member` 和 `--version`。
- CLI 通过 `JsonProjectStorage -> ProjectService` 调用业务，不直接操作 JSON。
- CLI 成功返回退出码 `0`；已知业务/存储失败返回退出码 `1`。
- `project_state.py` 保留 M1-T02 / M1-T03 的引用、复制和原地修改实验。
- 能区分 package 内模块通过 `python -m ...` 启动与直接执行 `.py` 文件的差异。
- 能使用 `sys.path`、模块 `__file__` 和 `importlib.util.find_spec()` 定位模块搜索与同名包问题。
- 能识别基础循环导入，并结合 Model / Service / Storage 职责判断不合理的反向依赖。
- 已建立“只捕获能够处理/转换的具体异常；无法处理则继续传播”的基础异常处理原则。

## 当前结构与职责

```text
project/
├── app/
│   ├── __init__.py
│   ├── info.py
│   ├── main.py              # argparse CLI、依赖组装、结果输出与最外层异常转换
│   ├── models.py            # Project dataclass
│   ├── project_state.py     # T02/T03 状态与复制实验
│   ├── services.py          # Project CRUD 与业务规则
│   ├── storage.py           # InMemory + JSON 两种存储实现
│   └── exceptions.py        # 业务异常与存储数据异常
├── tests/
│   ├── test_smoke.py
│   ├── test_project_state.py
│   ├── test_services.py
│   ├── test_json_storage.py
│   └── test_cli.py
├── data/
│   └── projects.json        # CLI 默认持久化文件；运行后按需创建
├── learning_records/
│   ├── M1-T01.md
│   ├── ...
│   ├── M1-T07.md
│   └── summary.md
├── AGENTS.md
├── README.md
├── StudyPLAN.md
└── pyproject.toml
```

当前核心调用关系：

```text
终端用户
  │
  ▼
argparse / app.main
  │
  ▼
ProjectService
  │
  ├── 构造/更新 Project
  ├── 业务规则与业务异常
  │
  ▼
JsonProjectStorage
  │
  ├── dataclass ↔ JSON 数据转换
  └── data/projects.json
```

测试中仍可将 `InMemoryProjectStorage` 传给 `ProjectService`。

职责边界：

```text
Model   → 数据结构
Service → 业务动作与规则
Storage → 数据存取
CLI     → 用户输入/输出与应用组装
```

当前尚未引入正式 Storage 抽象、Repository、Pydantic、FastAPI 或数据库。

## 验证基线

2026-08-29 在仓库自带虚拟环境中由用户实际执行并提供结果：

```bash
.venv/bin/python --version
# Python 3.14.6

.venv/bin/python -m pytest tests/test_cli.py -v
# 5 passed in 0.04s

.venv/bin/python -m pytest -q
# 38 passed in 0.17s
```

测试构成：

- `test_smoke.py`：2 个应用常量测试。
- `test_project_state.py`：11 个数据模型、引用和状态隔离测试。
- `test_services.py`：13 个 Service / Storage 行为与业务异常测试。
- `test_json_storage.py`：7 个 JSON 持久化、数据格式和跨实例测试。
- `test_cli.py`：5 个 CLI 到 Service/Storage/JSON 的集成测试。

总计：`38 passed`。

人工 CLI 验收：

```text
create
→ list
→ get
→ update
→ 旧名称 get 失败且 exit code = 1
→ 新名称 get 成功
→ delete
→ list 显示 No projects.
```

此前也已完成跨 Python 进程 JSON 持久化实验。

项目要求 Python 3.11 或更高版本。

## 当前设计结论

- Service 通过组合使用 Storage，不通过继承复用存储能力。
- `InMemoryProjectStorage` 与 `JsonProjectStorage` 保持各自明确语义。
- 当前共同 Storage 类型使用 `InMemoryProjectStorage | JsonProjectStorage`，只是 M1 阶段临时类型契约。
- `list_all()` 对内存 Storage 只隔离内部列表，不代表深复制 Project。
- 类型注解用于表达接口，不提供运行时数据校验；当前未引入 Pydantic。
- `field(default_factory=list)` 保证不同 `Project` 实例不共享默认列表。
- 函数参数不能使用 `tags=[]` / `members=[]` 这类可变默认对象；M1-T07 Review 已发现并修复一次回归。
- 新增数据字段时，必须检查所有对象重建和序列化/反序列化路径。
- Update 在 M1 阶段使用“完整替换”语义，不提前实现 PATCH。
- 更新操作先确认当前 Project 存在，再检查新名称冲突。
- Storage 的“未查到”可以是正常查询结果 `None` / `False`；Service 再将其解释为业务失败。
- 非法 JSON / 非法数据结构不能被转换为 `[]`。
- 当前层无法可靠恢复或转换异常时，应允许异常继续传播。
- CLI 是当前应用最外层边界，可以将已知业务/存储异常转换为用户可读错误和退出码。
- `main.py` 不直接读写 JSON；持久化职责属于 `JsonProjectStorage`。
- `data/projects.json` 当前使用相对项目工作目录的默认路径，因此 CLI 应从项目根目录执行。
- JSON 文件当前没有并发锁、事务或原子替换机制；这不是 M1-T07 的目标。

## 已知限制与后续归属

| 限制 | 计划处理任务 |
| --- | --- |
| 尚未完成 M1 综合断点调试与故障定位验收 | M1-T08 |
| 尚未完成 Git diff / commit 基线 | M1-T08 |
| 尚未提供仓库级裸 `except` / 宽泛 `except Exception` 扫描结果 | M1-T08 |
| CLI Update 当前是完整替换，不支持 HTTP/PATCH 风格部分字段更新 | M2 |
| Service 共同 Storage 类型仍是具体实现 union，尚无正式 Repository/抽象契约 | M3 |
| JSON 存储无并发控制、事务、锁和数据库级约束 | M3 / M8 |
| 当前 CLI 默认 JSON 路径依赖从项目根目录启动 | 后续工程配置阶段 |

以上限制不影响 M1-T07 已完成的验收结论。

## 下一步：M1-T08

下一任务聚焦 `pytest + Debugger + Git 基线`：

- 核对全量测试收集与覆盖意图。
- 使用断点跟踪一条真实 CLI 调用链。
- 主动制造一个错误并完成定位与修复。
- 查看 Git status / diff。
- 完成一次规范 Git commit。
- 检查裸 `except` 与宽泛 `except Exception`。
- 对 M1 Python 工程化地基做综合验收。
- 完成 M1 里程碑级验收记录和项目摘要更新。

在 M1-T08 正式完成前，不提前进入 M2 FastAPI。

## 摘要维护规则

每完成一个任务卡后：

1. 先新增或更新对应的 `learning_records/Mx-Txx.md`；
2. 再更新本文件中的进度、当前能力、结构、验证基线、限制和下一步；
3. 只保留仍然有效的项目级结论，不复制任务记录中的长篇教学内容；
4. 信息冲突时，按“当前代码与测试结果 → 最新任务记录 → 本摘要”的优先级修正。
