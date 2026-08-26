# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-08-26
>
> 当前阶段：M1 Python 工程化地基
>
> 正式进度：M1-T01 ～ M1-T05 已完成，下一任务为 M1-T06

本文只保存便于接手项目的最新快照。各任务的学习过程、代码片段、Code Review 和完整验收记录，以同目录下的 `M1-Txx.md` 为准。

## 任务进度

| 任务                     | 状态  | 完成日期       | 主要结果                                                           | 详细记录                     |
| ---------------------- | --- | ---------- | -------------------------------------------------------------- | ------------------------ |
| M1-T01 工程骨架            | 已完成 | 2026-08-09 | 建立 `app/`、`tests/`、`pyproject.toml`、应用入口和冒烟测试                  | [`M1-T01.md`](M1-T01.md) |
| M1-T02 对象引用与可变对象       | 已完成 | 2026-08-10 | 实践引用、原地修改、浅复制和状态隔离                                             | [`M1-T02.md`](M1-T02.md) |
| M1-T03 函数、类型注解与数据模型    | 已完成 | 2026-08-11 | 用 `dataclass` 建立 `Project`，补充类型注解和回归测试                         | [`M1-T03.md`](M1-T03.md) |
| M1-T04 类、组合与模块职责       | 已完成 | 2026-08-25 | 初步拆分 Model / Service / Storage，实现内存存储和按名称查询                    | [`M1-T04.md`](M1-T04.md) |
| M1-T05 模块、包与 Import 排错 | 已完成 | 2026-08-26 | 验证模块启动与脚本启动差异，掌握 `sys.path`、`__file__`、`find_spec()` 和循环导入基础排错 | [`M1-T05.md`](M1-T05.md) |
| M1-T06 异常处理与业务异常       | 待开始 | —          | 下一任务：具体异常、`raise`、自定义异常与业务失败表达                                 | `StudyPLAN.md`           |

## 当前可用能力

- `Project` 使用 `dataclass` 表达项目数据，字段为 `name`、`description`、`tags` 和 `members`。
- `ProjectService` 支持创建项目、列出项目和按名称查询项目。
- `InMemoryProjectStorage` 在进程内保存项目，并通过返回新列表避免直接暴露内部列表。
- 创建 Project 时复制调用方传入的 `tags` 和 `members`，避免列表引用被意外共享。
- `project_state.py` 保留 M1-T02 / M1-T03 的引用、复制和原地修改实验，作为现阶段学习材料。
- `python -m app.main` 可启动当前入口；入口目前只输出应用名称和版本，还不是完整 CLI 管理器。
- 能区分 package 内模块通过 `python -m ...` 启动与直接执行 `.py` 文件的差异。
- 能使用 `sys.path`、模块 `__file__` 和 `importlib.util.find_spec()` 定位模块搜索与同名包问题。
- 能识别基础循环导入，并结合 Model / Service / Storage 职责判断不合理的反向依赖。
## 当前结构与职责

```text
project/
├── app/
│   ├── __init__.py          # APP_NAME
│   ├── info.py              # APP_VERSION
│   ├── main.py              # 当前应用入口
│   ├── models.py            # Project 数据模型
│   ├── project_state.py     # T02/T03 状态与复制实验
│   ├── services.py          # Project 业务动作
│   └── storage.py           # 内存存储实现
├── tests/
│   ├── test_smoke.py
│   ├── test_project_state.py
│   └── test_services.py
├── learning_records/        # 已完成任务的详细验收记录与本摘要
├── AGENTS.md                # 仓库协作约定
├── README.md                # 项目说明与使用入口
├── StudyPLAN.md             # M1～M8 学习路线
└── pyproject.toml           # Python 版本、构建配置和依赖
```

当前核心调用关系：

```text
调用方
  └── ProjectService
        ├── 构造 Project
        └── 组合 InMemoryProjectStorage
              └── 保存或查询 Project
```

职责边界：Model 表达数据，Service 组织业务动作，Storage 管理数据存取。当前只是最小分层，尚未引入 Storage 抽象接口。

## 验证基线

2026-08-26 在仓库自带虚拟环境中验证：

```bash
.venv/bin/python --version
# Python 3.14.6

.venv/bin/python -m pytest -q
# 19 passed in 0.13s

.venv/bin/python -m app.main
# AI Workspace Lite started. 0.1.0
```

测试构成：

- `test_smoke.py`：2 个应用常量测试；
- `test_project_state.py`：11 个数据模型、引用和状态隔离测试；
- `test_services.py`：6 个 Service / Storage 行为测试。

项目要求 Python 3.11 或更高版本，开发依赖目前只有 `pytest>=8,<10`。系统环境若没有 `python` 命令，可激活 `.venv`，或直接使用 `.venv/bin/python`。

## 当前设计结论

- Service 通过组合使用 Storage，不通过继承复用存储能力。
- `list_all()` 只隔离 Storage 的内部列表；列表中的 `Project` 仍是同一批可变对象，不应把它误解为深复制。
- 类型注解用于表达接口，不提供运行时数据校验；当前未引入 Pydantic。
- `field(default_factory=list)` 保证不同 `Project` 实例不共享默认列表。
- 新增数据字段时，必须检查所有对象重建路径；M1-T03 曾修复 `with_tag()` 遗漏 `description` 的问题。
- 测试通过之外，还应确认测试被 pytest 收集，并检查断言是否真正覆盖业务预期。

## 已知限制与后续归属

| 限制                                | 计划处理任务         |
| --------------------------------- | -------------- |
| 尚未系统验证包、模块搜索路径和循环导入               | M1-T05         |
| 查询不存在项目时返回 `None`，尚无自定义业务异常       | M1-T06         |
| 只支持内存存储，进程退出后数据丢失                 | M1-T07         |
| 尚无完整 CLI CRUD、重复名称规则和更新/删除能力      | M1-T07         |
| 尚未完成 M1 综合调试与 Git 验收              | M1-T08         |
| `project_state.py` 中仍有学习实验和较多教学注释 | 在正式业务模块稳定后评估清理 |

这些限制均不影响 M1-T04 已完成的验收结论。不要在 M1-T05 中提前实现异常、JSON 持久化、FastAPI 或数据库。

## 下一步：M1-T05

下一任务聚焦“模块、包与 Import 排错”，不增加业务功能。应基于现有多文件结构完成以下学习与验收：

- 解释 module、package、`__init__.py` 和项目根目录；
- 解释 `from app...` 绝对导入如何解析；
- 观察不同启动目录或启动方式对导入的影响；
- 能定位 `ModuleNotFoundError`；
- 识别循环导入的形成原因和基础排查方法。

## 摘要维护规则

每完成一个任务卡后：

1. 先新增或更新对应的 `learning_records/Mx-Txx.md`；
2. 再更新本文件中的进度、当前能力、结构、验证基线、限制和下一步；
3. 只保留仍然有效的项目级结论，不复制任务记录中的长篇教学内容；
4. 信息冲突时，按“当前代码与测试结果 → 最新任务记录 → 本摘要”的优先级修正。

