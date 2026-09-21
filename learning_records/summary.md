# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-21
>
> 当前阶段：M2 进行中｜HTTP 与 FastAPI 后端基础
>
> 正式进度：M1 已完成；M2-T01 ～ M2-T06 已完成；下一任务 M2-T07

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 进行中 | — | M2-T01 ～ M2-T06 已完成；下一任务 M2-T07 |
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
M2-T07  日志与请求排错                  → 下一任务
```

已生成记录：

```text
M2-T01.md
M2-T02.md
M2-T03.md
M2-T04.md
M2-T05.md
M2-T06.md
```

## M2 已完成能力概览

### M2-T01｜HTTP / REST

已建立：

```text
HTTP Request / Response
Method / URL / Header / Body
Status Code
HTTP 与 REST 的区别
Router / Service / Storage 的职责边界
CLI exit code 与 HTTP status code 的边界
```

当前 Project 尚无数据库 `id`，HTTP 资源继续暂以 `name` 作为标识。

### M2-T02｜FastAPI 最小应用

已建立：

```text
FastAPI application
Uvicorn ASGI Server
GET /
app.main:app
路由注册
/openapi.json
/docs
```

能够解释：

```text
Client
→ Uvicorn
→ FastAPI
→ Route
→ endpoint
→ HTTP Response
```

### M2-T03｜Path / Query

已建立：

```text
Path Parameter
Query Parameter
required / optional
int / bool 类型解析
非法 Query → 422
```

能够解释：

```text
URL 中的数据首先是文本
→ FastAPI 根据 Python 类型注解解析 / 校验
→ Python 参数
```

### M2-T04｜Pydantic Request Body

已建立：

```text
Pydantic BaseModel
Request Schema
Field 约束
required / optional
允许 None 与允许缺失的区别
JSON Body → Python Pydantic object
RequestValidationError → 422
```

当前：

```text
ProjectRequestBody
→ HTTP 输入 Schema

Project dataclass
→ Domain Model
```

两者保持职责分离。

### M2-T05｜Projects CRUD API

已实现：

```text
POST   /projects
GET    /projects
GET    /projects/{project_name}
PATCH  /projects/{project_name}
DELETE /projects/{project_name}
```

真实调用链：

```text
Client
→ Uvicorn
→ FastAPI
→ Pydantic / Path
→ Web Route
→ ProjectService
→ JsonProjectStorage
→ data/projects.json
→ HTTP Response
```

Web 与 CLI 复用同一个 `ProjectService`，Route 不复制业务规则。

PATCH 使用：

```python
body.model_dump(exclude_unset=True)
```

识别客户端真正发送的字段，并由 Router 将局部更新合并为完整数据后调用现有完整替换 Service。

已建立：

```text
字段没传
≠
字段显式为 null
```

### M2-T06｜统一业务异常 → HTTP

已建立 FastAPI exception handler：

```text
ProjectNotFoundError
→ 404 Not Found

ProjectAlreadyExistsError
→ 409 Conflict
```

Service 保持：

```text
只表达业务失败原因
不依赖 HTTPException
不依赖 FastAPI
```

不同入口分别翻译：

```text
CLI
→ Error 文本 + exit code

Web
→ HTTP status + JSON
```

当前能够明确区分：

```text
422
→ Request / Pydantic 校验失败

404
→ Service 判定资源不存在

409
→ Service 判定业务状态冲突

500
→ 未处理的服务器内部错误
```

不使用：

```python
except Exception:
```

把未知服务器错误伪装成 4xx。

## 当前项目能力

### Domain / Service / Storage

- `Project` 使用 dataclass，字段为 `name / description / tags / members`。
- `ProjectService` 支持完整 CRUD。
- `InMemoryProjectStorage` 保留内存实现。
- `JsonProjectStorage` 支持 JSON 持久化、跨实例和跨进程加载。
- 非法 JSON / 非法存储数据使用 `ProjectStorageDataError`。
- 重复名称使用 `ProjectAlreadyExistsError`。
- Project 不存在使用 `ProjectNotFoundError`。
- Service 不直接访问 Storage 内部状态。
- Update Service 继续保持完整替换语义。

### CLI

- CLI 支持 `create / list / get / update / delete`。
- CLI 不直接操作 JSON。
- 成功退出码为 `0`。
- 已知业务 / 存储错误返回 `1`。
- CLI 与 Web 复用相同 Service 业务规则。

### Web / FastAPI

- FastAPI application 与原 CLI 入口共存。
- Uvicorn 作为 ASGI Server。
- 已建立 GET `/`。
- 已建立 Path / Query 学习路由。
- 已建立 Pydantic Request Body 学习路由。
- 已实现 Projects HTTP CRUD。
- POST 创建成功使用 201。
- DELETE 成功使用 204。
- FastAPI / Pydantic 请求校验失败返回 422。
- Project 不存在统一返回 404。
- Project 名称冲突统一返回 409。
- CRUD Route 不直接访问 JSON。
- CRUD Route 调用 `ProjectService`。
- 业务异常通过 application exception handler 统一翻译。

## 当前调用关系

### CLI

```text
Terminal
→ argparse / main.py
→ ProjectService
→ JsonProjectStorage
→ data/projects.json
```

### Web 成功路径

```text
Client
→ Uvicorn
→ FastAPI
→ Route
→ ProjectService
→ JsonProjectStorage
→ data/projects.json
→ Project / list[Project]
→ Response Schema
→ HTTP Response
```

### Web Request 校验失败

```text
Client
→ FastAPI
→ Pydantic
→ RequestValidationError
→ FastAPI 默认 handler
→ HTTP 422
```

### Web 资源不存在

```text
Client
→ FastAPI
→ Route
→ ProjectService
→ ProjectNotFoundError
→ FastAPI exception handler
→ HTTP 404
```

### Web 业务状态冲突

```text
Client
→ FastAPI
→ Route
→ ProjectService
→ ProjectAlreadyExistsError
→ FastAPI exception handler
→ HTTP 409
```

### PATCH

```text
PATCH partial body
→ Pydantic ProjectUpdateRequest
→ model_dump(exclude_unset=True)
→ 读取当前 Project
→ Router 合并未修改字段
→ ProjectService.update_project(...)
→ JsonProjectStorage
→ HTTP Response
```

## 最新验证基线

2026-09-21，M2-T06：

```bash
pytest --collect-only -q
# 46 tests collected in 1.80s

pytest tests/test_web_smoke.py -v
# 6 passed in 0.33s

pytest -q
# 46 passed in 0.46s
```

当前测试构成：

```text
test_smoke.py            2
test_project_state.py   11
test_services.py        13
test_json_storage.py     7
test_cli.py              7
test_web_smoke.py        6
--------------------------
Total                   46
```

Web smoke tests：

```text
test_fastapi_app_exists
test_root_route_is_in_openapi_schema
test_parameter_demo_is_in_openapi_schema
test_request_body_demo_is_in_openapi_schema
test_project_crud_routes_are_in_openapi_schema
test_project_exception_handlers_are_registered
```

M2-T06 实际 HTTP：

```text
POST /projects
name = m2-t06-alpha
→ 201 Created
```

```text
POST duplicate
name = m2-t06-alpha
→ 409 Conflict
→ Project already exists
```

```text
GET /projects/m2-t06-missing
→ 404 Not Found
→ Project not found
```

```text
DELETE /projects/m2-t06-missing
→ 404 Not Found
→ Project not found
```

```text
PATCH /projects/m2-t06-alpha
name = m2-t06-beta（已存在）
→ 409 Conflict
→ Project already exists
```

本次材料没有重新执行 `name=""` 的 422 curl 对照实验；该行为已在 M2-T04 实测，本卡没有修改相应 Request Schema，因此不虚构本次执行记录，也不影响 M2-T06 404 / 409 核心验收。

部分成功请求的 JSON 正文仍有下一条 `curl -i \` 覆盖字符的终端采集污染；异常响应 404 / 409 的关键 JSON 完整可读，pytest 与状态码证据有效。

## 当前设计结论

- Model 负责领域数据。
- Service 负责业务动作和业务规则。
- Storage 负责数据存取。
- CLI 负责命令行协议翻译。
- FastAPI Route 负责 HTTP 协议翻译。
- Service 不依赖 CLI，也不依赖 FastAPI。
- Web Route 不直接操作 JSON。
- Web 与 CLI 共用 Service。
- Pydantic Schema 属于 HTTP 边界，不替代当前 Domain dataclass。
- Request 参数 / Body 校验在 endpoint 正常业务逻辑之前完成。
- RequestValidationError 继续由 FastAPI 默认处理为 422。
- `ProjectNotFoundError` 是业务异常，由 Web 统一翻译为 404。
- `ProjectAlreadyExistsError` 是业务异常，由 Web 统一翻译为 409。
- 同一种业务异常不在每个 endpoint 重复 try/except。
- Service 不抛 `HTTPException`，避免业务层依赖 HTTP 框架。
- 不捕获所有 `Exception` 并转换成 4xx。
- 未知服务器程序错误应保留为 500 类错误，以便后续日志和排错。
- 当前 `Project` 没有稳定数据库主键，继续使用 `project_name` 作为 HTTP 资源标识。
- M2-T05 的 PATCH 由 Router 负责把部分更新翻译为 Service 的完整替换 Update。
- M2-T06 已闭合业务异常到 HTTP Response 的边界。

## 当前 M2 能力边界

已经完成：

```text
HTTP / REST
FastAPI application
Uvicorn
Path Parameter
Query Parameter
Pydantic Request Body
Request Schema
422
Projects CRUD API
PATCH partial update
Router → Service → Storage
404
409
FastAPI exception handler
业务异常 → HTTP Response
```

尚未正式进入：

```text
结构化日志
请求排错
500 traceback 分析
完整 FastAPI TestClient API 测试
PostgreSQL
SQLAlchemy
Docker
LLM API
Tool Calling
Workflow / RAG
```

## 下一步：M2-T07

```text
M2-T07｜日志与请求排错
```

M2-T06 已经能区分：

```text
422 → 请求输入校验失败
404 → 资源不存在
409 → 业务状态冲突
500 → 未处理服务器错误
```

下一任务开始关注：

```text
错误发生时如何留下足够信息
请求 Method / Path
业务上下文
异常信息
traceback
404 / 422 / 500 如何定位
参数到底在哪一层丢失
```

M2-T07 的重点是**可观测性和故障定位**，不是继续增加新的 CRUD 功能。

继续保持任务边界：不提前进入 M2-T08 完整接口自动化测试，也不进入 M3 数据库。
