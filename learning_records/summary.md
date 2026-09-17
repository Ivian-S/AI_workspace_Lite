# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-17
>
> 当前阶段：M2 进行中｜HTTP 与 FastAPI 后端基础
>
> 正式进度：M1 已完成；M2-T01、M2-T02、M2-T03、M2-T04、M2-T05 已完成；下一任务 M2-T06

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 进行中 | — | M2-T01 ～ M2-T05 已完成；下一任务 M2-T06 |
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

## M2 原子任务

当前进度：

```text
M2-T01  HTTP 请求/响应与 REST         ✅ 已完成
M2-T02  FastAPI 最小应用与启动流程    ✅ 已完成
M2-T03  路径参数与查询参数             ✅ 已完成
M2-T04  Pydantic 请求体与校验          ✅ 已完成
M2-T05  Projects CRUD API              ✅ 已完成
M2-T06  404、重复数据与统一异常         → 下一任务
```

已生成记录：

```text
M2-T01.md
M2-T02.md
M2-T03.md
M2-T04.md
M2-T05.md
```

M2-T01 完成 HTTP Request / Response 与 REST 基础认知，没有修改源码。

M2-T02 正式引入 FastAPI 与 Uvicorn，在保留原 CLI 入口的基础上增加最小 FastAPI application、GET `/` 路由以及 OpenAPI / Swagger 基础。

M2-T03 增加 Path Parameter、Query Parameter 和参数类型转换学习路由，验证默认 Query 参数、显式 Query 参数、`int` / `bool` 类型解析以及非法参数在 endpoint 调用前被拒绝的行为。

M2-T04 增加 Pydantic Request Schema 和 `POST /request-body-demo` 学习路由，建立 JSON Request Body、required / optional、字段类型、字段约束以及 FastAPI 自动 422 的基础认知。

M2-T05 把 FastAPI Web 路由正式接入现有 `ProjectService` 和 `JsonProjectStorage`，实现 Projects HTTP CRUD。PATCH 由 Router 负责把部分更新请求合并成完整数据，再复用现有完整替换 `ProjectService.update_project()`。

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
- 已引入 FastAPI application，同时保留原 CLI 入口。
- 已使用 Uvicorn 作为 ASGI Server 启动 FastAPI application。
- Web application 拥有 GET `/` 路由。
- 已建立 `/parameter-demo/{project_name}` 参数学习路由。
- 能处理 Path Parameter 和带默认值的 Query Parameter。
- FastAPI 能依据 Python 类型注解将请求参数解析为 `int` / `bool` 等 Python 类型。
- 非法 Query 参数会在 endpoint 正常执行前被 FastAPI 拒绝。
- 已建立 `POST /request-body-demo` Request Body 学习路由。
- 已使用 Pydantic `BaseModel` 定义 Request Schema。
- 能处理 required 字段、可省略字段、`list[str]` 等字段类型和基础 `Field` 约束。
- 非法 Request Body 会在 endpoint 正常执行前由 FastAPI / Pydantic 拒绝并返回 422。
- 已通过 OpenAPI smoke tests 验证 Path / Query / Request Body 声明。
- 已实现 Projects HTTP CRUD：
  - `POST /projects`
  - `GET /projects`
  - `GET /projects/{project_name}`
  - `PATCH /projects/{project_name}`
  - `DELETE /projects/{project_name}`
- Web Projects API 已正式调用 `ProjectService`。
- Web Projects API 通过 `JsonProjectStorage` 使用现有 JSON 持久化。
- 创建 Project 返回 HTTP 201。
- 删除成功返回 HTTP 204。
- PATCH 能只更新客户端实际发送的字段并保留其他字段。
- 当前 `Project` 仍没有数据库 `id`，HTTP 资源继续以 `project_name` 标识。
- 404 / 重复数据等业务异常尚未统一翻译为 HTTP 响应；该部分进入 M2-T06。

## 当前 M2 学习能力

M2-T01 已建立：

- 能拆解 HTTP Request 的 Method、request target、Headers 与 Body。
- 能拆解 HTTP Response 的 Status Code、Headers 与 Body。
- 能区分 HTTP 协议与 REST 架构风格。
- 能按资源导向设计当前 Project 的基本 CRUD URL。
- 当前 Project 尚无 `id`，HTTP 设计暂以 `name` 作为资源标识。
- 能为查询、创建、删除、不存在、重复数据和未处理服务器异常选择合理状态码。
- 能解释 CLI exit code 与 HTTP Status Code 属于不同边界。
- 能画出 `Client → HTTP → Router → Service → Storage → HTTP Response`。
- 能解释 Router 负责协议翻译、Service 负责业务规则。
- 已识别当前完整替换 `update_project()` 与未来 `PATCH` 部分更新之间的语义差异。

M2-T02 已建立：

- 已正式引入 FastAPI 与 Uvicorn。
- 能区分 Uvicorn ASGI Server 与 FastAPI Web Framework 的职责。
- 能解释 `app.main:app` 中 package、module 与 application attribute 的含义。
- 能解释 Uvicorn import `app.main` 时为什么不会执行 CLI `main()`。
- 已建立最小 FastAPI application instance 和 GET route。
- 能解释 route decorator 在模块导入阶段完成路由注册。
- 能区分 `/openapi.json` 与 `/docs`。
- 能解释 Swagger UI 使用 OpenAPI Schema 展示接口。
- 能画出当前真实请求链：
  `Client → Uvicorn → FastAPI → Route → read_root() → HTTP Response → Client`。
- 能说明最小 HTTP 路由不需要虚构 Service / Storage 调用。
- 能区分 module import 失败和 module 内 application attribute 查找失败。
- 已通过临时修改 route 观察 FastAPI 路由匹配与 404 行为。

M2-T03 已建立：

- 能区分 Path Parameter 与 Query Parameter。
- 参数是否来自 Path，首先取决于参数名是否出现在 route path 的 `{...}` 中，而不是由 Python 类型决定。
- 能说明 Query Parameter 可以 required，也可以通过默认值成为 optional。
- 能说明 Path Parameter 属于路由结构，在 FastAPI 中始终 required。
- 能解释 HTTP URL 中的参数首先是文本形式，而不是 Python `int` / `bool` 对象。
- 能解释 FastAPI 如何根据 Python 类型注解执行参数解析和校验。
- 能解释 `"8"` 如何成为 Python `int 8`。
- 能解释 `"true"` 如何成为 Python `bool True`。
- 能解释非法 `limit=abc` 为什么不会正常进入 endpoint。
- 已实际观察非法整数 Query 返回 HTTP 422。
- 能画出：
  `Client → Uvicorn → FastAPI → 路由匹配 → 参数提取 → 类型转换/校验 → endpoint → Response`。
- 已独立增加 `offset: int = 0` Query Parameter，并验证默认值和显式传参。

M2-T04 已建立：

- 能区分 Path / Query 与 JSON Request Body 的数据来源。
- 能使用 Pydantic `BaseModel` 定义 HTTP Request Schema。
- 能使用 `Field` 添加基础字段约束。
- 能说明 required 字段与默认值之间的关系。
- 能区分“允许值为 None”和“允许字段缺失”。
- 能说明 `list[str]` 等字段类型会参与请求校验。
- 能解释 FastAPI / Pydantic 在 endpoint 正常执行前完成 Body 解析、转换和校验。
- 已实际观察缺少 required 字段、字段类型错误、字段约束失败返回 HTTP 422。
- 能从错误响应读取 `loc: body / <field>` 与错误类型。
- 能画出：
  `Client → Uvicorn → FastAPI → JSON Body → Pydantic Request Schema → Python object → endpoint / 422`。
- 已通过 OpenAPI smoke test 验证 Request Body Schema。

M2-T05 已建立：

- 能把 FastAPI Route 接入已有 `ProjectService` 和 `JsonProjectStorage`。
- 能说明 Web 与 CLI 应复用同一业务层，而不是复制业务规则。
- 已实现 Project 的 Create / List / Get / Patch / Delete HTTP 接口。
- 能说明创建成功使用 201、删除成功使用 204。
- 能解释 `body.model_dump(exclude_unset=True)` 在 PATCH 中的作用。
- 能区分 PATCH 中“字段未发送”与“显式发送 null”。
- 能通过 Router 合并当前 Project 和局部更新，再调用现有完整替换 Service。
- 能说明项目重名属于 Service 业务规则，不属于 Route 的重复实现。
- 已独立验证只修改 `description` 时 `name / tags / members` 保持不变。
- 已验证修改 `name` 后，可以使用新名称继续操作资源。
- 已验证删除成功返回 204。
- 能画出：
  `Client → Uvicorn → FastAPI → Pydantic / Path → Route → Service → Storage → JSON → Response`。

## 当前调用关系

### CLI 调用链

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

### Web 参数学习调用链

```text
Client
→ Uvicorn
→ FastAPI
→ 路由匹配
→ Path / Query 参数提取
→ 类型解析与校验
→ read_parameter_demo(...)
→ HTTP JSON Response
```

### Web Request Body 学习调用链

```text
Client
→ Uvicorn
→ FastAPI
→ 读取 / 解析 JSON Body
→ Pydantic Request Schema
   ├─ 校验成功 → Python object → endpoint → 200
   └─ 校验失败 → RequestValidationError → FastAPI 默认异常处理 → 422
```

### 当前 Projects Web API 调用链

```text
Client
  │
  ▼
Uvicorn
  │
  ▼
FastAPI
  │
  ├── Method + Path 路由匹配
  ├── Path / Request Body 提取
  ├── Pydantic 解析与校验
  │
  ▼
Projects Route
  │
  ▼
ProjectService
  │
  ▼
JsonProjectStorage
  │
  ▼
data/projects.json
  │
  ▼
Project / list[Project]
  │
  ▼
HTTP Response
```

PATCH 的额外 Router 翻译：

```text
PATCH partial body
→ exclude_unset=True
→ 读取当前 Project
→ 合并未修改字段
→ 完整 update 数据
→ ProjectService.update_project(...)
```

职责：

```text
Model      → 领域数据
Service    → 业务动作与规则
Storage    → 数据存取
CLI        → CLI 参数解析、应用组装、用户输出与退出码
Uvicorn    → ASGI Server，监听网络并运行 Web application
FastAPI    → HTTP 路由、参数/Body 处理、响应与 OpenAPI
Web Route  → HTTP 协议翻译，并调用 Service
```

## 最新验证基线

2026-09-17，M2-T05：

```bash
pytest --collect-only -q
# 45 tests collected in 2.38s

pytest tests/test_web_smoke.py -v
# 5 passed in 0.31s
```

本次验收材料未包含：

```bash
pytest -q
```

因此当前记录**不写成**：

```text
45 passed
```

也不虚构全量回归耗时。

当前测试构成：

```text
test_smoke.py            2
test_project_state.py   11
test_services.py        13
test_json_storage.py     7
test_cli.py              7
test_web_smoke.py        5
--------------------------
Total                   45 collected
```

Web smoke tests：

```text
test_fastapi_app_exists
test_root_route_is_in_openapi_schema
test_parameter_demo_is_in_openapi_schema
test_request_body_demo_is_in_openapi_schema
test_project_crud_routes_are_in_openapi_schema
```

M2-T05 实际 HTTP 验证：

```text
POST /projects
→ 201 Created
```

```text
GET /projects
→ 200 OK
```

```text
GET /projects/m2-t05-demo
→ 200 OK
```

```text
PATCH /projects/m2-t05-demo
Body: {"description": "patched"}
→ 200 OK
→ name / tags / members 保持不变
```

```text
PATCH /projects/m2-t05-demo
Body: {"description": null}
→ 200 OK
→ description = null
```

```text
PATCH /projects/m2-t05-demo
Body: {"name": "m2-t05-renamed"}
→ 200 OK
```

```text
DELETE /projects/m2-t05-renamed
→ 204 No Content
```

本次若干 curl 响应正文存在终端采集污染：下一条 `curl -i \` 命令覆盖了上一条 JSON 的部分字符。因此正式记录不把污染后的字符串当成真实 API 数据；HTTP 状态、后续 CRUD 行为、OpenAPI smoke tests 以及独立 PATCH 验收仍然有效。

## 当前设计结论

- Service 通过组合使用 Storage。
- Service 不直接访问 Storage 内部状态。
- `InMemoryProjectStorage` 与 `JsonProjectStorage` 保持明确不同的存储语义。
- 当前共同 Storage 类型仍是具体实现 union，正式抽象留到后续 Repository 分层。
- dataclass 可变字段使用 `field(default_factory=list)`。
- 函数参数不使用可变默认对象。
- 原 Service Update 保持完整替换语义。
- 非法 JSON 不能被转换为空数据。
- 只捕获当前层能够处理或转换的异常。
- CLI `main.py` 不直接进行 JSON 持久化。
- 测试通过之外必须确认测试收集。
- Debugger 应定位数据第一次异常变化的层。
- HTTP 与 REST 不等价：HTTP 是协议，REST 是架构风格。
- Method 表达意图，URL / request target 表达资源目标。
- Router 负责 HTTP 协议翻译，Service 保持业务规则独立。
- HTTP Status Code 不与 CLI exit code 机械一一映射。
- 当前 Project 没有 `id`，HTTP 暂以 `project_name` 作为资源标识。
- Uvicorn 是 ASGI Server；FastAPI 是 Web Framework，两者职责不同。
- `app.main:app` 表示 `package.module:attribute`。
- FastAPI 路由由 Method + Path 共同决定。
- `/openapi.json` 是机器可读 OpenAPI Schema；`/docs` 是基于 Schema 的 Swagger UI。
- Path / Query 表示参数来源，Python 类型注解表示 FastAPI 应将输入解析为什么 Python 类型。
- Query Parameter 不天然等于 optional。
- FastAPI 在调用 endpoint 前完成参数解析和请求体验证。
- Request Schema 属于 HTTP 输入边界，不等同于现有 `Project` dataclass。
- 请求体验证失败时由 FastAPI 默认异常处理形成 422。
- Web Projects Route 不直接操作 JSON，必须调用 `ProjectService`。
- Web 与 CLI 共享同一业务规则来源。
- PATCH 的 HTTP 部分更新语义由 Router 翻译为现有 Service 的完整替换 Update。
- `exclude_unset=True` 用于识别客户端实际发送字段，避免未发送字段被默认值覆盖。
- “字段缺失”和“字段显式为 null”是不同的 PATCH 输入语义。
- 项目重名属于 Service 业务规则，Route 不重复实现。
- 404 / 重复数据等业务异常到 HTTP Response 的统一映射留到 M2-T06。
- 不因为学习计划示例使用 `{id}` 就虚构当前不存在的 Project id。

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

M1 未进入、但当前后续阶段正在逐步补齐：

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

其中 HTTP / FastAPI / Pydantic 已在 M2-T01 ～ M2-T05 正式进入。

## 下一步：M2-T06

```text
M2-T06｜404、重复数据与统一异常
```

M2-T05 已经建立真实业务 HTTP 调用链：

```text
Client
→ Uvicorn
→ FastAPI
→ Request / Path
→ Route
→ ProjectService
→ JsonProjectStorage
→ data/projects.json
→ Response
```

下一任务解决当前业务异常与 HTTP 边界之间的翻译：

```text
ProjectNotFoundError
→ HTTP 404

ProjectAlreadyExistsError
→ HTTP 409（按本项目状态码约定）

存储相关异常
→ 明确哪些可以转换为 HTTP 响应

真正未处理异常
→ HTTP 500
```

M2-T06 的重点不是在每个 endpoint 里散落重复的 `try/except`，而是建立统一、可复用的：

```text
Domain / Service Exception
→ HTTP Response
```

转换机制。

继续保持任务边界：不提前进入 M2-T07 日志专项、M2-T08 完整 FastAPI 接口测试或 M3 数据库。
