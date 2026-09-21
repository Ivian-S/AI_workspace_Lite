# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-21
>
> 当前阶段：M2 已完成｜下一阶段 M3 PostgreSQL、ORM、项目分层与权限
>
> 正式进度：M1、M2 已完成；下一任务 M3-T01｜PostgreSQL 基础与 SQL CRUD

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 已完成 | 2026-09-21 | FastAPI Web API、CRUD、校验、统一异常、日志排错、接口自动化测试 |
| M3 PostgreSQL、ORM、项目分层与权限 | 待开始 | — | 下一阶段；下一任务 M3-T01 |
| M4 Linux 服务排错与 Docker 化 | 待开始 | — | — |
| M5 大模型服务集成 | 待开始 | — | — |
| M6 安全 Tool Calling | 待开始 | — | — |
| M7 Workflow、Agent 与知识库 | 待开始 | — | — |
| M8 工程收口、故障演练与面试级验收 | 待开始 | — | — |

## M1 原子任务

M1-T01 ～ M1-T08 全部完成。

## M2 原子任务

```text
M2-T01  HTTP 请求/响应与 REST         ✅ 已完成
M2-T02  FastAPI 最小应用与启动流程    ✅ 已完成
M2-T03  路径参数与查询参数             ✅ 已完成
M2-T04  Pydantic 请求体与校验          ✅ 已完成
M2-T05  Projects CRUD API              ✅ 已完成
M2-T06  404、重复数据与统一异常         ✅ 已完成
M2-T07  日志与请求排错                  ✅ 已完成
M2-T08  FastAPI 接口测试               ✅ 已完成
```

已生成 / 更新记录：

```text
M2-T01.md
M2-T02.md
M2-T03.md
M2-T04.md
M2-T05.md
M2-T06.md
M2-T07.md
M2-T08.md
M2.md
```

## M2 已完成能力概览

### M2-T01｜HTTP / REST

已建立 HTTP Request / Response、Method、URL、Header、Body、Status Code、REST、Router / Service / Storage 边界，以及 CLI exit code 与 HTTP status code 的区别。

### M2-T02｜FastAPI 最小应用

已建立 FastAPI application、Uvicorn ASGI Server、最小 Route、`app.main:app`、OpenAPI 与 Swagger UI。

### M2-T03｜Path / Query

已建立 Path Parameter、Query Parameter、required / optional、`int` / `bool` 类型转换，以及非法 Query → 422 的调用链。

### M2-T04｜Pydantic Request Body

已建立 Pydantic `BaseModel`、Request Schema、`Field` 约束、required / optional、允许 `None` 与允许字段缺失的区别，以及 RequestValidationError → 422。

### M2-T05｜Projects CRUD API

已实现：

```text
POST   /projects
GET    /projects
GET    /projects/{project_name}
PATCH  /projects/{project_name}
DELETE /projects/{project_name}
```

Web Route 已正式接入：

```text
ProjectService
→ JsonProjectStorage
→ data/projects.json
```

PATCH 使用 `model_dump(exclude_unset=True)` 区分未发送字段与显式值，并由 Router 合并部分更新后复用现有完整替换 Service。

### M2-T06｜统一业务异常

已建立：

```text
ProjectNotFoundError
→ FastAPI exception handler
→ 404

ProjectAlreadyExistsError
→ FastAPI exception handler
→ 409
```

Service 不依赖 `HTTPException` / FastAPI；CLI 与 Web 各自翻译同一个业务异常。

### M2-T07｜日志与请求排错

已正式完成并验证：

```text
request_complete
business_error
validation_error
request_failed
method / path / status / duration
routing 404 与 business 404 区分
body / query 422 定位
500 traceback 文件 / 行号定位
```

实际日志已经证明：

```text
GET /projects
→ request_complete
→ 200

GET /does-not-exist
→ request_complete
→ 404
→ 无 business_error
→ routing 404

GET /projects/m2-t07-missing
→ business_error type=ProjectNotFoundError
→ request_complete
→ 404
→ business 404

POST /projects name=""
→ validation_error loc=body.name
→ 422

GET /parameter-demo/alpha?limit=abc
→ validation_error loc=query.limit
→ 422

GET /debug/m2-t07-boom
→ request_failed error_type=RuntimeError
→ HTTP 500
→ traceback 定位 app/main.py:67
→ debug_m2_t07_boom
```

临时 `/debug/m2-t07-boom` 故障路由已删除，随后再次执行全量回归：

```text
47 passed in 1.84s
```

因此 M2-T07 已完成完整闭环：

```text
日志观察
→ 故障复现
→ traceback 定位
→ 删除临时故障代码
→ 全量回归
```

### M2-T08｜FastAPI 接口测试

已新增：

```text
tests/test_web_api.py
```

共 10 条真实 HTTP application 行为测试，覆盖：

```text
空状态
Create
List
Get One
PATCH 部分更新
Delete
404
409
422
```

测试通过 `TestClient` 直接驱动 ASGI application，不要求启动 Uvicorn。

测试 fixture 使用：

```text
ProjectService
→ InMemoryProjectStorage
```

替换正式 Web service 的 JSON Storage，从而保证：

```text
test isolation
不污染 data/projects.json
测试独立 / 可重复 / 顺序无关
```

最终验证：

```text
test_web_api.py → 10 passed
Web tests       → 17 passed
full suite      → 57 passed
```

M2-T08 同时建立：

```text
只测 status code 不足以保护业务行为
Response Body / 状态变化也必须断言
```

当前接口测试依赖栈存在 2 条第三方 deprecation warning，均不影响测试通过；Starlette TestClient 的 `httpx` fallback 已提示迁移到 `httpx2`，作为依赖维护项记录。

## 当前项目能力

### Domain / Service / Storage

- `Project` 使用 dataclass，字段为 `name / description / tags / members`。
- `ProjectService` 支持完整 CRUD。
- `InMemoryProjectStorage` 保留内存实现。
- `JsonProjectStorage` 支持 JSON 持久化。
- 非法 JSON / 非法存储数据使用 `ProjectStorageDataError`。
- 重复名称使用 `ProjectAlreadyExistsError`。
- Project 不存在使用 `ProjectNotFoundError`。
- Service 不直接访问 Storage 内部状态。
- Update Service 保持完整替换语义。

### CLI

- CLI 支持 create / list / get / update / delete。
- CLI 不直接操作 JSON。
- CLI 与 Web 复用相同 Service。
- 已知业务 / 存储错误转换为 CLI 错误输出与 exit code。

### Web / FastAPI

- FastAPI 与 CLI 入口共存。
- Uvicorn 作为 ASGI Server。
- 已完成 Path / Query 与 Request Body 学习路由。
- 已实现 Projects HTTP CRUD。
- 请求校验失败返回 422。
- Project 不存在统一返回 404。
- Project 名称冲突统一返回 409。
- 已建立 HTTP middleware 请求日志。
- 已建立业务异常日志。
- 已建立 RequestValidationError 日志。
- 422 Response 继续复用 FastAPI 默认 handler。
- 当前没有默认记录完整 Body、Token 等敏感数据。
- 未知异常会记录 `request_failed`，随后重新抛出并保持 HTTP 500 语义。
- 已通过临时 RuntimeError 实验验证 traceback 能定位到自己项目文件与实际行号。
- 临时 debug route 已删除，并完成删除后的全量回归。
- 已使用 FastAPI `TestClient` 建立真实 HTTP application 行为测试。
- TestClient 测试不需要启动 Uvicorn。
- API tests 使用独立 `InMemoryProjectStorage`，不写真实 `data/projects.json`。
- 已建立 Create / List / Get / Patch / Delete / 404 / 409 / 422 自动回归。
- PATCH 测试同时断言响应内容，保护未发送字段不会被清空。


## 当前调用关系

### Web 正常请求

```text
Client
→ Uvicorn
→ HTTP logging middleware
→ FastAPI
→ Route
→ ProjectService
→ JsonProjectStorage
→ HTTP Response
→ request_complete
→ Uvicorn access log
```

### Routing 404

```text
Client
→ middleware
→ FastAPI route matching
→ no matching route
→ 404 Response
→ request_complete(status=404)
```

没有：

```text
business_error
```

### Business 404

```text
Client
→ middleware
→ Route
→ ProjectService
→ ProjectNotFoundError
→ business_error
→ exception handler
→ 404 Response
→ request_complete(status=404)
```

### Validation 422

```text
Client
→ middleware
→ FastAPI / Pydantic
→ RequestValidationError
→ validation_error(loc / type / msg)
→ FastAPI 默认 validation handler
→ 422 Response
→ request_complete(status=422)
```

### 已验证的未处理 500 链

```text
Client
→ middleware
→ application code
→ RuntimeError
→ request_failed(error_type=RuntimeError)
→ raise
→ Uvicorn / ASGI traceback
→ HTTP 500
```

本次实际 traceback 中：

```text
app/main.py:82
log_http_request
response = await call_next(request)
```

是异常传播经过 middleware 的位置；真正抛出异常的根因位置为：

```text
app/main.py:67
debug_m2_t07_boom
raise RuntimeError(...)

RuntimeError: M2-T07 intentional failure
```

因此已经能够区分：

```text
异常传播经过点
≠
真正根因
```

### Web 自动测试调用链

```text
pytest
→ TestClient
→ FastAPI ASGI application
→ middleware
→ Pydantic / Route
→ ProjectService
→ InMemoryProjectStorage
→ HTTP Response
→ assert
```

生产与测试的主要入口区别：

```text
生产：
HTTP socket → Uvicorn → ASGI application

测试：
TestClient → ASGI application
```

测试没有绕过 Route / Pydantic / exception handler，只是跳过真实网络 socket 和 Uvicorn。

## 最新验证基线

2026-09-21，M2-T08 / M2 正式收口：

```bash
pytest tests/test_web_api.py -v
# collected 10 items
# 10 passed, 2 warnings in 0.44s
```

```bash
pytest   tests/test_web_smoke.py   tests/test_web_api.py   -v

# collected 17 items
# 17 passed, 2 warnings in 0.48s
```

```bash
pytest -q
# 57 passed, 2 warnings in 1.01s
```

本次材料没有单独提供：

```bash
pytest --collect-only -q
```

但已经实际确认：

```text
test_web_api.py → 10 tests collected and passed
Web tests       → 17 tests collected and passed
full suite      → 57 passed
```

当前正式测试基线：

```text
57 tests passed
```

当前测试构成：

```text
test_smoke.py            2
test_project_state.py   11
test_services.py        13
test_json_storage.py     7
test_cli.py              7
test_web_smoke.py        7
test_web_api.py         10
--------------------------
Total                   57
```

M2-T08 API behavior tests：

```text
test_projects_start_empty
test_create_project
test_list_projects
test_get_project
test_patch_project_preserves_unsent_fields
test_delete_project
test_missing_project_returns_404
test_duplicate_project_returns_409
test_patch_rename_conflict_returns_409
test_invalid_project_body_returns_422
```

当前 pytest 有 2 条第三方 deprecation warning：

```text
Starlette TestClient:
httpx fallback deprecated; prefer httpx2

Starlette / AnyIO:
anyio.abc.BlockingPortal alias deprecated
```

处理原则：

```text
不把 warning 当作测试失败
不隐藏所有 DeprecationWarning
不修改 site-packages
记录并在依赖维护时迁移兼容版本
```

其中 TestClient dev dependency 建议迁移到：

```toml
"httpx2>=2.13,<3"
```

## 当前设计结论

- Model 负责领域数据。
- Service 负责业务动作与业务规则。
- Storage 负责数据存取。
- CLI 负责命令行协议翻译。
- FastAPI Route 负责 HTTP 协议翻译。
- Service 不依赖 FastAPI。
- Web 与 CLI 共用 Service。
- Pydantic Schema 属于 HTTP 边界。
- RequestValidationError 继续由 FastAPI 默认机制生成 422。
- `ProjectNotFoundError` 统一翻译为 404。
- `ProjectAlreadyExistsError` 统一翻译为 409。
- HTTP Status 相同不代表故障发生在同一层。
- routing 404 与 business 404 必须结合应用日志区分。
- 422 排错优先读取 `loc` 判断 path / query / body。
- Uvicorn access log 表达 HTTP 访问结果；application log 表达应用内部上下文。
- middleware 可捕获 `Exception` 用于记录，但必须 `raise` 让未知异常继续传播。
- 不使用 `except Exception` 把服务器 Bug 伪装为 4xx。
- 日志默认不记录完整 Request Body、密码、Token 或 Authorization Header。
- 日志不能代替异常处理，异常处理也不能代替日志。
- 500 排错必须最终落到 traceback 中的错误类型、自己项目文件与实际行号。
- 已实际验证 `request_failed → raise → HTTP 500 → traceback` 的完整异常链。
- traceback 中 middleware 的 `call_next()` 行是传播经过点，真正根因应继续向下定位到最内层自己代码。
- 临时故障代码用于实验后必须删除，并重新执行全量回归确认正式基线。
- TestClient 直接驱动 ASGI application，不要求真实 TCP/Uvicorn。
- Web API tests 使用 test-only InMemoryProjectStorage，避免污染真实 JSON 数据。
- 测试必须隔离状态，不能依赖测试执行顺序。
- 只断言 HTTP status 不能充分证明业务行为正确；关键 Response Body 和状态变化也应验证。
- `test_json_storage.py`、`test_services.py`、`test_web_smoke.py`、`test_web_api.py` 分别保护不同测试层。
- M2 最终已经把人工 curl 验证转换为自动 HTTP 回归测试。


## 当前 M2 能力边界

M2 已正式完成：

```text
HTTP / REST
FastAPI application
Uvicorn
OpenAPI / Swagger
Path / Query
Pydantic Request Body
422
Projects CRUD API
PATCH partial update
Router → Service → Storage
404
409
FastAPI exception handler
业务异常 → HTTP Response
HTTP middleware 日志
routing 404 / business 404 定位
validation_error 定位
500 request_failed
traceback 文件 / 行号定位
FastAPI TestClient
HTTP 接口自动化测试
test isolation
```

M2 未提前进入：

```text
PostgreSQL
SQLAlchemy
Repository
数据库 Migration / Transaction
认证 / 权限
Docker
LLM API
Tool Calling
Workflow / RAG
```

## 下一步：M3-T01

M2 已正式完成：

```text
M2｜HTTP 与 FastAPI 后端基础
✅ 已完成
```

M2 最终形成：

```text
Client
→ Uvicorn
→ FastAPI
→ Middleware
→ Pydantic / Route
→ ProjectService
→ JsonProjectStorage
→ HTTP Response
```

并形成对应自动测试链：

```text
pytest
→ TestClient
→ ASGI application
→ ProjectService
→ InMemoryProjectStorage
→ HTTP Response
→ assert
```

下一阶段：

```text
M3｜PostgreSQL、ORM、项目分层与权限
```

下一任务：

```text
M3-T01｜PostgreSQL 基础与 SQL CRUD
```

M3 将从当前 JSON Storage 继续演进到真正数据库分层；按 StudyPLAN 顺序推进，不提前堆 ORM 之外的后续能力。
