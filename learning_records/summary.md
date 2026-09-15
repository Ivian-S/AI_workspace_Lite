# AI Workspace Lite｜项目进度摘要

> 最后更新：2026-09-15
>
> 当前阶段：M2 进行中｜HTTP 与 FastAPI 后端基础
>
> 正式进度：M1 已完成；M2-T01、M2-T02、M2-T03 已完成；M2-T04 代码与 HTTP 验证已通过，待补 2 项无 AI 验收；下一任务仍为 M2-T04 收口

## 里程碑进度

| 里程碑 | 状态 | 完成日期 | 结果 |
| --- | --- | --- | --- |
| M1 Python 工程化地基 | 已完成 | 2026-08-29 | 多文件工程、分层、异常、JSON CRUD、CLI、pytest、Debugger、Git 基线 |
| M2 HTTP 与 FastAPI 后端基础 | 进行中 | — | M2-T01、M2-T02、M2-T03 已完成；M2-T04 代码与 HTTP 验证已通过，待补 2 项无 AI 验收 |
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
M2-T04  Pydantic 请求体与校验          🟡 待补 2 项无 AI 验收
```

已生成记录：

```text
M2-T01.md
M2-T02.md
M2-T03.md
M2-T04.md
```

M2-T01 完成 HTTP Request / Response 与 REST 基础认知，没有修改源码。

M2-T02 正式引入 FastAPI 与 Uvicorn，在保留原 CLI 入口的基础上增加最小 FastAPI application、GET `/` 路由以及 OpenAPI / Swagger 基础。

M2-T03 增加 Path Parameter、Query Parameter 和参数类型转换学习路由，验证默认 Query 参数、显式 Query 参数、`int` / `bool` 类型解析以及非法参数在 endpoint 调用前被拒绝的行为。

M2-T04 已在本地增加 Pydantic Request Schema 和 `POST /request-body-demo` 学习路由，验证 required 字段、`Field(min_length=1)`、`list[str]` 类型校验、默认字段以及 FastAPI 自动 422；自动测试与 HTTP 验证已通过，但无 AI 验收第 3、4 项尚未提交，因此尚未正式收口。

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
- 当前 Web application 已拥有最小 GET `/` 路由。
- 已建立 `/parameter-demo/{project_name}` 参数学习路由。
- 能处理 Path Parameter 和带默认值的 Query Parameter。
- FastAPI 能依据 Python 类型注解将请求参数解析为 `int` / `bool` 等 Python 类型。
- 非法 Query 参数会在 endpoint 正常执行前被 FastAPI 拒绝。
- 已建立 `POST /request-body-demo` Request Body 学习路由。
- 已使用 Pydantic `BaseModel` 定义 `ProjectRequestBody` Request Schema。
- `name` 使用 `Field(min_length=1)`；`description` 使用 `str | None = None`；`tags / members` 使用 `default_factory=list`。
- 能观察缺少 required 字段、字段类型错误和字段约束失败产生的 HTTP 422。
- 当前 HTTP 学习路由尚未接入 `ProjectService` / `JsonProjectStorage`。
- 已使用 OpenAPI smoke test 验证 Web 路由、参数声明和 Request Body Schema。

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
- 能说明当前最小 HTTP 路由尚未调用 `ProjectService` / `JsonProjectStorage`。
- 能区分 module import 失败和 module 内 application attribute 查找失败。
- 已通过临时修改 `/` → `/hello` 观察 FastAPI 路由匹配与 404 行为。

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

M2-T04 当前已建立（代码 / HTTP 部分）：

- 能说明 JSON Request Body 与 Path / Query Parameter 的来源差异。
- 能使用 Pydantic `BaseModel` 定义 HTTP Request Schema。
- 能使用 `Field(min_length=1)` 添加基础字段约束。
- 能说明 `description: str | None = None` 同时表示允许 `None` 且允许字段缺失。
- 已理解“允许 `None`”与“允许字段缺失”不是同一概念；对应的无 AI required 实验尚待补交。
- 能说明 `tags: list[str]` 为什么拒绝字符串输入。
- 能解释 FastAPI / Pydantic 在 endpoint 正常执行前完成 Request Body 解析和校验。
- 已实际观察缺少 `name`、`tags` 类型错误、`name` 长度不足产生 HTTP 422。
- 能从错误响应读取 `loc: body / <field>` 与错误类型。
- 能画出：
  `Client → Uvicorn → FastAPI → JSON Body → Pydantic Request Schema → Python object → endpoint / 422`。
- 已通过 OpenAPI smoke test 验证 Request Body Schema。
- `priority: int = 0` 的独立三场景实验尚待补交。

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

### 当前 Web HTTP 边界学习调用链

Path / Query 学习路由：

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

Request Body 学习路由：

```text
Client
→ Uvicorn
→ FastAPI
→ 路由匹配
→ 读取 / 解析 JSON Request Body
→ Pydantic ProjectRequestBody
   ├─ 校验成功 → Python object → read_request_body_demo(...) → 200 JSON Response
   └─ 校验失败 → RequestValidationError → FastAPI 默认异常处理 → 422
```

当前这些调用链尚未进入：

```text
ProjectService
→ JsonProjectStorage
→ data/projects.json
```

因此当前参数与 Request Body 学习接口仍属于 HTTP 边界学习，不代表 Projects 业务 API 已经完成。

职责：

```text
Model     → 数据
Service   → 业务动作与规则
Storage   → 数据存取
CLI       → 参数解析、应用组装、用户输出与退出码
Uvicorn   → ASGI Server，监听网络并运行 Web application
FastAPI   → HTTP 路由、参数处理、响应以及 OpenAPI
```

## 最新验证基线

2026-09-15，M2-T04 本地验证：

```bash
pytest --collect-only -q
# 44 tests collected in 1.18s

pytest tests/test_web_smoke.py -v
# 4 passed in 0.27s

pytest -q
# 44 passed in 0.31s
```

当前测试构成：

```text
test_smoke.py            2
test_project_state.py   11
test_services.py        13
test_json_storage.py     7
test_cli.py              7
test_web_smoke.py        4
--------------------------
Total                   44
```

Web smoke tests：

```text
test_fastapi_app_exists
test_root_route_is_in_openapi_schema
test_parameter_demo_is_in_openapi_schema
test_request_body_demo_is_in_openapi_schema
```

M2-T03 实际 HTTP 验证：

```text
GET /parameter-demo/alpha
→ 200 OK
→ project_name = "alpha"
→ limit = 10
→ include_archived = false
→ offset = 0
```

```text
GET /parameter-demo/alpha?limit=5&include_archived=true&offset=10
→ 200 OK
→ project_name = "alpha"
→ limit = 5
→ include_archived = true
→ offset = 10
```

```text
GET /parameter-demo/alpha?limit=abc
→ 422 Unprocessable Content
→ error location: query / limit
→ error type: int_parsing
```

M2-T04 实际 HTTP 验证：

```text
POST /request-body-demo
合法 JSON Body
→ 200 OK
```

```text
缺少 name
→ 422 Unprocessable Content
→ error location: body / name
→ error type: missing
```

```text
tags = "python"
→ 422 Unprocessable Content
→ error location: body / tags
→ error type: list_type
```

```text
name = ""
→ 422 Unprocessable Content
→ error location: body / name
→ error type: string_too_short
→ min_length = 1
```

说明：本次终端记录的前三段 curl 响应正文存在下一条 `curl -i \` 命令覆盖部分字符的采集污染；HTTP Status、错误位置/类型、最后一段完整错误响应以及自动测试仍可作为可靠验收依据。正式记录不把被覆盖的字符串当作真实 API 返回值。

当前正式本地代码验证基线：

```text
44 tests collected
44 tests passed
```

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

- HTTP 与 REST 不等价：HTTP 是协议，REST 是架构风格。
- Method 表达意图，URL / request target 表达资源目标。
- Router 负责 HTTP 协议翻译，Service 保持业务规则独立。
- HTTP Status Code 不与 CLI exit code 机械一一映射。
- 当前 Project 没有 `id`，M2-T01 不虚构 `project.id`。
- 当前 Update 是完整替换语义，未来 `PATCH` 部分更新需要后续正式演进。
- Uvicorn 是 ASGI Server；FastAPI 是 Web Framework，两者职责不同。
- `app.main:app` 表示 `package.module:attribute`，最后的 `app` 是 FastAPI application instance。
- Uvicorn 通过 import 加载 `app.main` 时，模块的 `__name__` 为 `app.main`，不会触发原 CLI 的 `if __name__ == "__main__"`。
- FastAPI 路由由 Method + Path 共同决定。
- `/openapi.json` 是机器可读的 OpenAPI Schema；`/docs` 是基于 Schema 的 Swagger UI。
- 当前最小 HTTP 请求只经过 FastAPI route，不提前虚构 Service / Storage 调用。
- 当前阶段继续保留 CLI 与 Web application 的过渡共存，不为单一路由提前拆分 Router 目录。
- Path / Query 表示参数来源，Python 类型注解表示 FastAPI 应将输入解析为什么 Python 类型。
- 参数是否来自 Path，由它是否出现在 route path 的 `{...}` 中决定。
- Query Parameter 不天然等于 optional；是否允许省略取决于声明方式和默认值。
- Path Parameter 属于 URL 路由结构，在 FastAPI 中始终 required。
- FastAPI 在调用 endpoint 前完成参数解析和校验。
- 参数解析失败时 endpoint 不正常执行，由 FastAPI 在 HTTP 边界返回错误响应。
- 当前参数学习 route 不接入 Project 业务层，不提前实现 Projects CRUD。
- Pydantic Request Schema 属于 HTTP 输入边界，不等同于现有 `Project` dataclass。
- Request Body 在进入 endpoint 前由 FastAPI / Pydantic 完成解析、类型转换和字段校验。
- 请求体验证失败时由 FastAPI 默认异常处理形成 422，endpoint 不按正常路径执行。
- `str | None` 表示值允许为 `None`；字段是否允许缺失还取决于是否存在默认值。
- 类型正确不代表字段一定合法，`Field(min_length=1)` 等约束会继续参与校验。


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

进入：

```text
M2-T05｜Projects CRUD API
```

M2-T05 才开始把 HTTP 路由真正接入现有 `ProjectService`；继续遵守当前模型事实，不提前虚构不存在的业务字段或数据库层。
