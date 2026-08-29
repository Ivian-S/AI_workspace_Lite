# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-08-29
>
> 当前阶段：M1 已完成，准备进入 M2 HTTP 与 FastAPI 后端基础
>
> 正式进度：M1-T01 ～ M1-T08 全部完成；下一任务 M2-T01

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 待开始 | — | 下一阶段 |
| M3 PostgreSQL、ORM、项目分层与权限 | 待开始 | — | — |
| M4 Linux 服务排错与 Docker 化 | 待开始 | — | — |
| M5 大模型服务集成 | 待开始 | — | — |
| M6 安全 Tool Calling | 待开始 | — | — |
| M7 Workflow、Agent 与知识库 | 待开始 | — | — |
| M8 工程收口、故障演练与面试级验收 | 待开始 | — | — |

## M1 原子任务

M1-T01 ～ M1-T08 全部完成。

详细记录：

```text
M1-T01.md
M1-T02.md
M1-T03.md
M1-T04.md
M1-T05.md
M1-T06.md
M1-T07.md
M1-T08.md
M1.md
```

## 当前项目能力

- `Project` 使用 dataclass，字段为 `name / description / tags / members`。
- `ProjectService` 支持完整 CRUD。
- `InMemoryProjectStorage` 保留内存实现。
- `JsonProjectStorage` 支持 JSON 持久化、跨实例和跨进程加载。
- 非法 JSON / 非法存储数据使用 `ProjectStorageDataError`。
- 重复名称使用 `ProjectAlreadyExistsError`。
- Project 不存在由 Service 转换为 `ProjectNotFoundError`。
- CLI 支持 `create / list / get / update / delete`。
- CLI 不直接操作 JSON。
- 成功退出码为 `0`；已知业务/存储错误为 `1`。
- 能排查 package/module/import 问题。
- 能使用 Debugger 跟踪真实 CLI 调用链。
- 能主动制造故障、定位根因并完成回归。
- 能确认 pytest 测试被实际收集。
- Git 基线验收完成。

## 当前调用关系

```text
Terminal
  │
  ▼
argparse / main.py
  │
  ▼
ProjectService
  │
  ▼
JsonProjectStorage
  │
  ▼
data/projects.json
```

职责：

```text
Model   → 数据
Service → 业务动作与规则
Storage → 数据存取
CLI     → 参数解析、应用组装、用户输出与退出码
```

## 最新验证基线

2026-08-29：

```bash
pytest --collect-only -q
# 40 tests collected in 0.51s

pytest tests/test_cli.py -v
# 7 passed in 0.57s

pytest -q
# 40 passed in 0.10s
```

测试构成：

```text
test_smoke.py           2
test_project_state.py  11
test_services.py       13
test_json_storage.py    7
test_cli.py             7
-------------------------
Total                  40
```

M1-T08 的 Debugger、主动 Bug 定位、except 扫描和 Git 验收由用户确认均已完成并通过；未提供完整输出的项目不虚构具体日志或 commit hash。

## 当前设计结论

- Service 通过组合使用 Storage。
- Service 不直接访问 Storage 内部状态。
- `InMemoryProjectStorage` 与 `JsonProjectStorage` 保持明确不同的存储语义。
- 当前共同 Storage 类型仍是具体实现 union，正式抽象留到后续 Repository 分层。
- dataclass 可变字段使用 `field(default_factory=list)`。
- 函数参数不使用可变默认对象。
- Update 当前使用完整替换语义。
- 非法 JSON 不能被转换为空数据。
- 只捕获当前层能够处理或转换的异常。
- `main.py` 不直接进行 JSON 持久化。
- 测试通过之外必须确认测试收集。
- Debugger 应定位数据第一次异常变化的层。

## M1 已完成能力边界

M1 已正式完成：

```text
Python 工程结构
对象引用
dataclass / 类型注解
组合与职责
Import 排错
业务异常
JSON CRUD
CLI
pytest
Debugger
Git 基线
```

M1 未进入：

```text
HTTP
FastAPI
Pydantic
PostgreSQL
SQLAlchemy
Docker
LLM API
Agent
```

## 下一步：M2-T01

```text
M2-T01｜HTTP 请求/响应与 REST
```

M2 的核心数据流将从：

```text
Terminal → CLI → Service → Storage
```

演进为：

```text
Client
→ HTTP Request
→ FastAPI Router
→ Service
→ Storage
→ HTTP Response
```

继续坚持先理解 HTTP 请求/响应，再引入 FastAPI。
