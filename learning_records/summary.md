# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-21
>
> 当前阶段：M2 进行中｜HTTP 与 FastAPI 后端基础
>
> 正式进度：M1 已完成；M2-T01 ～ M2-T07 已完成；下一任务 M2-T08｜FastAPI 接口测试

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 进行中 | — | M2-T01 ～ M2-T07 已完成；下一任务 M2-T08 |
| M3 PostgreSQL、ORM、项目分层与权限 | 待开始 | — | — |
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
M2-T08  FastAPI 接口测试               → 下一任务
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

## 最新验证基线

2026-09-21，M2-T07 正式收口：

首次正式代码验证：

```bash
pytest --collect-only -q
# 47 tests collected in 0.50s

pytest tests/test_web_smoke.py -v
# 7 passed in 0.33s

pytest -q
# 47 passed in 0.42s
```

随后临时加入 `/debug/m2-t07-boom` 制造 RuntimeError，实际观察：

```text
request_failed
method=GET
path=/debug/m2-t07-boom
duration_ms=1.06
error_type=RuntimeError
```

Uvicorn access log：

```text
GET /debug/m2-t07-boom
→ 500 Internal Server Error
```

traceback 最终定位：

```text
app/main.py:67
debug_m2_t07_boom
raise RuntimeError(...)

RuntimeError: M2-T07 intentional failure
```

实验结束后已删除临时 debug route，并再次执行：

```bash
pytest -q
# 47 passed in 1.84s
```

因此当前正式代码基线为：

```text
47 tests collected
47 tests passed
临时 debug route 已删除
```

当前测试构成：

```text
test_smoke.py            2
test_project_state.py   11
test_services.py        13
test_json_storage.py     7
test_cli.py              7
test_web_smoke.py        7
--------------------------
Total                   47
```

Web smoke tests：

```text
test_fastapi_app_exists
test_root_route_is_in_openapi_schema
test_parameter_demo_is_in_openapi_schema
test_request_body_demo_is_in_openapi_schema
test_project_crud_routes_are_in_openapi_schema
test_project_exception_handlers_are_registered
test_request_validation_handler_is_registered
```

M2-T07 已验证日志：

```text
200
→ request_complete

routing 404
→ request_complete
→ 无 business_error

business 404
→ business_error type=ProjectNotFoundError
→ request_complete

Body 422
→ validation_error loc=body.name

Query 422
→ validation_error loc=query.limit

500
→ request_failed error_type=RuntimeError
→ traceback
→ app/main.py:67
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

## 当前 M2 能力边界

已经完成：

```text
HTTP / REST
FastAPI application
Uvicorn
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
故障实验后的代码清理与回归
```

尚未正式进入：

```text
M2-T08 FastAPI 完整接口测试
PostgreSQL
SQLAlchemy
Docker
LLM API
Tool Calling
Workflow / RAG
```

## 下一步：M2-T08

```text
M2-T08｜FastAPI 接口测试
```

M2-T07 已正式完成：

```text
request_complete
business_error
validation_error
request_failed
routing 404 / business 404
422 参数位置定位
500 traceback 定位
临时故障代码清理
最终 pytest 回归
```

当前正式测试基线：

```text
47 tests collected
47 tests passed
```

M2-T08 将进入 M2 最后一张任务卡，重点从当前的 OpenAPI / handler smoke tests 扩展到真实 HTTP 接口自动化测试：

```text
正常路径
非法输入
不存在资源
重复数据
CRUD 行为
状态码与响应体
```

继续保持任务边界：M2-T08 只完成 FastAPI 接口测试和 M2 收口，不提前进入 M3 PostgreSQL / ORM。
