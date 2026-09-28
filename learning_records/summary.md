# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-28
>
> 当前阶段：M3 进行中｜M3-T01 与 M3-T2,3,4 已完成
>
> 正式进度：M1、M2 已完成；M3 已完成 T01～T04；下一任务 M3-T05｜Router / Service / Repository 分层

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 已完成 | 2026-09-21 | FastAPI Web API、CRUD、校验、统一异常、日志排错、接口自动化测试 |
| M3 PostgreSQL、ORM、项目分层与权限 | 进行中 | — | M3-T01～T04 已完成；下一任务 M3-T05 |
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

## M3 原子任务

```text
M3-T01      PostgreSQL 基础与 SQL CRUD                    ✅ 已完成
M3-T2,3,4  主外键/实体关系 + 核心表 + SQLAlchemy ORM      ✅ 已完成
            （合并原 M3-T02 / M3-T03 / M3-T04）
M3-T05      Router / Service / Repository 分层             ▶️ 下一任务
M3-T06      数据库迁移                                     ⏳ 待开始
M3-T07      事务                                           ⏳ 待开始
M3-T08      分页、排序、筛选与 JOIN                        ⏳ 待开始
M3-T09      密码 Hash、登录与 Token                        ⏳ 待开始
M3-T10      401 / 403 与工作空间权限隔离                   ⏳ 待开始
M3-T11      安全文件上传                                   ⏳ 待开始
M3-T12      文件下载/删除与权限校验                        ⏳ 待开始
```

已生成 / 更新记录：

```text
M3-T01.md
M3-T2,3,4.md
summary.md
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

## M3 当前进度

### M3-T01｜PostgreSQL 基础与 SQL CRUD

已在 PostgreSQL 16.15 中完成单表 SQL CRUD：

```text
INSERT
SELECT / WHERE / ORDER BY
UPDATE
DELETE
```

并完成 `ai_workspace_lite` 数据库与 `m3_t01_projects` 学习表验证。

### M3-T2,3,4｜关系设计 + 核心表 + ORM / Session

本任务合并原 M3-T02、M3-T03、M3-T04。

已完成七张正式核心表：

```text
users
workspaces
workspace_members
projects
tasks
files
operation_logs
```

已经实际验证：

```text
users.id                       → PRIMARY KEY
users.username / email         → UNIQUE
workspace_members              → (workspace_id, user_id) 联合主键
workspace_members.user_id      → users.id
workspace_members.workspace_id → workspaces.id
projects.workspace_id          → workspaces.id
projects(workspace_id, name)   → UNIQUE
tasks.workspace_id             → workspaces.id
tasks.project_id               → projects.id
```

非法：

```text
projects.workspace_id = 999999
```

已被 PostgreSQL Foreign Key 直接拒绝。

当前 ORM 栈：

```text
SQLAlchemy 2.1.1
Psycopg 3.3.6
PostgreSQL 16.15
```

Session 已实际验证：

```text
ORM Object
→ session.add()
→ id = None
→ flush()
→ PostgreSQL 生成 id
→ commit()
→ 新 Session reload
```

本阶段仍未将 FastAPI / Service 切换到 PostgreSQL；正式业务链仍使用 `JsonProjectStorage`。

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


### PostgreSQL / ORM

- PostgreSQL 16.15 已作为本地学习数据库运行。
- 已创建 `ai_workspace_lite`。
- 已建立七张正式核心表：`users / workspaces / workspace_members / projects / tasks / files / operation_logs`。
- 已掌握 PK、FK、UNIQUE、一对多、多对多中间表。
- 已验证 `workspace_members` 联合主键。
- 已验证 `projects(workspace_id, name)` workspace 内唯一性。
- 已通过非法 `workspace_id` 插入实验确认数据库级 FK 引用完整性。
- SQLAlchemy 2.1.1 + Psycopg 3.3.6 已接入。
- 已建立 Declarative ORM、Engine 与 Session。
- 已实际验证 `add → flush → generated id → commit → reload`。
- `create_all()` 当前仅用于首次 bootstrap，不视为 migration。
- FastAPI / Service 尚未切换到 PostgreSQL；该接入属于 M3-T05。

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

### PostgreSQL Schema 初始化链

```text
ORM Classes
→ Base.metadata
→ create_all()
→ Engine
→ Psycopg
→ PostgreSQL
→ 7 张核心表
```

### SQLAlchemy Session 写入链

```text
ORM Object
→ Session.add()
→ pending
→ flush()
→ SQL
→ Engine
→ Psycopg
→ PostgreSQL
→ generated id
→ commit()
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

### 2026-09-28｜M3-T2,3,4

实际环境：

```text
PostgreSQL 16.15
SQLAlchemy 2.1.1
Psycopg 3.3.6
Python 3.14.6
```

数据库结构已经确认七张核心表存在，并验证关键 PK / UNIQUE / FK。

Foreign Key 失败实验：

```text
INSERT projects(workspace_id=999999)
→ ERROR
→ projects_workspace_id_fkey
```

Session 实验：

```text
before flush: None
after flush: 2
loaded: 2 m3_t234_demo m3_t234_demo@example.com
```

全量回归：

```bash
pytest -q
# 57 passed, 2 warnings in 2.37s
```

因此当前正式 Python 测试基线仍为：

```text
57 tests passed
```

两条 warning 仍为既有 Starlette TestClient / AnyIO 第三方 deprecation warning，不属于数据库层失败。

### 2026-09-21｜M2-T08 / M2


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
- 数据库稳定身份使用整数 Primary Key，不再让 `Project.name` 承担数据库身份。
- `UNIQUE` 表达业务唯一性，`PRIMARY KEY` 表达稳定行身份，两者职责不同。
- `ForeignKey` 保证引用完整性，但不等于认证或权限校验。
- `workspace_members` 使用联合主键表达 User ↔ Workspace 多对多成员关系。
- `projects(workspace_id, name)` 保证项目名仅在 Workspace 内唯一。
- `relationship()` 属于 ORM 对象导航；真正的数据库引用约束由 `ForeignKey` 提供。
- `Session.add()` 只让对象进入 Session 管理；`flush()` 才会把待处理变化同步到数据库；`commit()` 提交事务。
- `Base.metadata.create_all()` 只作为当前空数据库 bootstrap 手段，不替代后续 migration。
- 当前 `tasks.workspace_id` 与 `tasks.project_id` 仍存在“Project 与 Workspace 一致性”待后续业务校验或更强数据库约束解决。
- 未来创建 Workspace 时，应保持 `owner_user_id` 与 `workspace_members(role='owner')` 的业务一致性。

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

## 当前 M3 能力边界

M3 当前已完成：

```text
PostgreSQL 基础 SQL CRUD
Primary Key / Foreign Key / UNIQUE
一对多 / 多对多关系设计
七张核心表
SQLAlchemy typed ORM
Declarative Base
Engine
Session
add / flush / commit
数据库级 FK 失败实验
```

M3 当前尚未进入：

```text
Repository
Service → PostgreSQL
FastAPI → PostgreSQL
Migration
多表事务
JOIN / 分页 / 排序 / 筛选
认证 / Token
Workspace 权限
文件安全
```

## 下一步：M3-T05

M3 当前：

```text
M3-T01
PostgreSQL 基础与 SQL CRUD
✅ 已完成

M3-T2,3,4
主键/外键与实体关系
+ 七张核心表
+ SQLAlchemy ORM / Session
✅ 已完成
```

当前存在两条尚未接通的链：

```text
应用业务链：
Client / CLI
→ FastAPI / CLI
→ ProjectService
→ JsonProjectStorage
→ data/projects.json
```

```text
数据库链：
ORM Object
→ Session
→ SQLAlchemy
→ Psycopg
→ PostgreSQL
→ users / workspaces / workspace_members / projects / tasks / files / operation_logs
```

下一任务：

```text
M3-T05｜Router / Service / Repository 分层
```

M3-T05 的核心不是继续堆表，而是把数据库访问职责收进 Repository，并开始让 Service 面向 Repository 工作；仍不会把 SQL 直接塞进 Router。
