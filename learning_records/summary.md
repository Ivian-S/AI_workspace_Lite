# AI Workspace Lite｜项目上下文与进度摘要

> **更新日期**：2026-10-11  
> **远程仓库**：https://github.com/Ivian-S/AI_workspace_Lite  
> **当前阶段**：M3｜PostgreSQL、ORM、项目分层与权限  
> **当前进度**：M1、M2 已完成；M3-T01、M3-T2,3,4 已完成；**M3-T5,6,7,8 技术验收通过，正式记录与远程同步状态待确认**。  
> **下一任务**：M3-T09｜密码 Hash、登录与 Token。  
> **最近一次有证据的全量测试**：67 passed，2 warnings（用户开发环境；配置了独立 PostgreSQL 测试库）。

## 1. 项目定位与信息优先级

AI Workspace Lite 是一个持续演进的 Python 后端学习与工程实战项目：从 CLI 项目管理器出发，逐步实现 FastAPI、PostgreSQL 多工作空间后端、Docker、LLM、Tool Calling、Workflow/RAG，最终形成可演示和排错的 AI 项目助手。

本文件是供 AI 助手**快速接手项目**的上下文索引，不是源码、API 规范或完整学习笔记。后续判断以以下顺序为准：

1. **GitHub 当前分支的实际源码与配置**：判断“现在代码怎么运行”。
2. **`learning_records/` 中的任务验收记录和真实测试输出**：判断“完成过什么、验证过什么”。
3. **`StudyPLAN.md`**：判断任务目标、先后顺序和学习边界。
4. **本 `summary.md`**：快速建立全貌；与实时源码冲突时应更新摘要。
5. **`README.md`、`AGENTS.md`**：曾出现明显落后于工程进度的版本，使用前必须与现行代码交叉核对。



## 2. 里程碑与任务状态

| 范围 | 状态 | 关键成果 / 下一步 |
| --- | --- | --- |
| M1｜Python 工程化地基 | ✅ 完成（2026-08-29） | dataclass、Service/Storage、JSON CRUD、CLI、pytest、Debugger、Git |
| M2｜HTTP 与 FastAPI | ✅ 完成（2026-09-21） | FastAPI CRUD、Pydantic 校验、异常处理、日志、HTTP 自动化测试 |
| M3-T01｜PostgreSQL 与 SQL CRUD | ✅ 完成 | 本地 PostgreSQL、手写 SQL CRUD、独立练习表 |
| M3-T2,3,4｜原 T02～T04 合并 | ✅ 完成（2026-09-28 验收基线） | 七张核心表、PK/FK/UNIQUE、SQLAlchemy ORM、Engine/Session |
| M3-T5,6,7,8｜原 T05～T08 合并 | ✅ 技术验收通过；📝 记录同步待核 | Repository 分层、Alembic、跨表事务、分页/筛选/排序/JOIN |
| M3-T09｜密码 Hash、登录与 Token | ▶️ 下一任务 | 尚未开始 |
| M3-T10｜401/403 与 Workspace 权限隔离 | ⏳ 待开始 | 尚未实现真实身份认证和成员权限控制 |
| M3-T11～T12｜安全文件上传、下载与删除 | ⏳ 待开始 | 文件业务与权限校验尚未进入验收 |
| M4～M8 | ⏳ 待开始 | Linux/Docker → LLM → Tool Calling → Workflow/RAG → 工程收口 |

M1-T01～T08、M2-T01～T08 均已完成。任务合并名称固定为 **`M3-T2,3,4`** 与 **`M3-T5,6,7,8`**，不要误以为原子任务被跳过。

**收口规则**：技术测试通过和“任务记录已写入仓库”是两个不同事实。前一组 M3-T2,3,4 已由用户确认收尾并同步；后一组 M3-T5,6,7,8 的技术验收已通过，但其 `learning_records/M3-T5,6,7,8.md` 是否已写入并推送，尚无本轮确认。

## 3. 当前系统架构：两条业务链并存

### 3.1 M1/M2 原有 JSON 业务链（保留兼容）

```text
CLI / FastAPI 旧版 /projects
  → ProjectService
  → InMemoryProjectStorage（测试）/ JsonProjectStorage（持久化）
  → data/projects.json
```

- 领域模型 `app.models.Project` 是 dataclass：`name / description / tags / members`。
- 原 `ProjectService` 负责 CRUD；CLI 和 Web 共用 Service，业务异常由各入口转换。
- 旧版项目以 `name` 查询，`PATCH` 使用 `model_dump(exclude_unset=True)` 保留未提交字段。
- JSON 业务链**没有自动迁移到 PostgreSQL**，也不等同于新的 Workspace-scoped `ProjectRow`。
- 原 `/projects` 路由和原有测试暂时保留，避免在 M3 数据库演进时破坏 M2 基线。

### 3.2 M3 新增 PostgreSQL 业务链（已跑通）

```text
HTTP Client
  → FastAPI Router / Pydantic Schema
  → UserDbService / WorkspaceDbService / ProjectDbService / TaskDbService
  → UserRepository / WorkspaceRepository / ProjectRepository / TaskRepository
  → SQLAlchemy Session → Engine → Psycopg
  → PostgreSQL（ai_workspace_lite）
```

**职责边界：**

- **Router**：参数、HTTP 响应与错误码；不直接编写 SQL。
- **Service**：业务规则、跨对象校验、事务边界；不依赖 HTTP 协议。
- **Repository**：ORM 查询、JOIN、增删改与 `flush()`；不自行 `commit()`。
- **Session/Engine**：Session 是工作单元和事务状态，Engine 管理数据库连接基础设施。
- **Database**：执行 PK、FK、UNIQUE 等约束。**FK 不等于登录校验或访问授权**。
- `get_session()` 负责请求内 Session 生命周期；`with session.begin()` 负责业务事务生命周期。

**重要区别**：`app.models.Project`（原领域对象）与 `app.db.models.ProjectRow`（数据库 ORM 行）目前是不同模型；不要擅自合并、替换旧存储或假设二者字段完全一致。

## 4. 核心目录与查阅入口

以下是已知的关键路径；若仓库发生重构，**以 GitHub 实际文件树为准**：

```text
project/
├── app/
│   ├── main.py                    # FastAPI 入口、旧路由及全局日志/异常机制
│   ├── models.py                  # M1/M2 Project dataclass
│   ├── services.py                # 原 ProjectService + M3 数据库业务 Service
│   ├── storage.py                 # InMemory/JSON Storage
│   ├── exceptions.py              # 领域/数据库业务异常
│   ├── m3_schemas.py              # M3 HTTP Request/Response Schema
│   ├── api/workspace.py           # M3 用户、工作空间、项目、任务路由
│   ├── db/
│   │   ├── base.py                # Declarative Base
│   │   ├── models.py              # 七张正式表的 ORM 映射
│   │   └── session.py             # Engine、SessionLocal、get_session
│   └── repositories/
│       ├── users.py
│       ├── workspaces.py
│       ├── projects.py
│       └── tasks.py
├── migrations/
│   ├── env.py                     # Alembic migration environment
│   └── versions/                  # Schema revisions
├── tests/
│   ├── test_web_api.py            # 旧 /projects HTTP 行为测试
│   └── test_m3_database.py        # M3 PostgreSQL 集成测试（独立测试库）
├── learning_records/             # 逐任务验收记录与本 summary
├── sql/m3_t01_projects.sql        # T01 手写 SQL 学习资产
├── alembic.ini
├── pyproject.toml
├── StudyPLAN.md
├── AGENTS.md
└── README.md
```

目录仅突出核心模块，不表示上述是仓库的全部文件。尤其 `app/db/init_db.py` 是早期 `create_all()` 学习入口，**正式 Schema 应通过 Alembic 管理**；如该文件仍存在，不应将其作为正式迁移工具。

## 5. 数据库模型与关键不变量

正式数据库 `ai_workspace_lite` 的七张核心表：

| 表 | 关键身份/关系 | 业务作用 |
| --- | --- | --- |
| `users` | `id` PK；`username`、`email` UNIQUE | 用户 |
| `workspaces` | `id` PK；`owner_user_id → users.id` | 工作空间 |
| `workspace_members` | `(workspace_id, user_id)` 联合 PK；双 FK；`role` | 用户—工作空间成员关系 |
| `projects` | `id` PK；`workspace_id → workspaces.id`；`(workspace_id, name)` UNIQUE | 工作空间内的项目 |
| `tasks` | `id` PK；`workspace_id` FK；可空 `project_id` FK | 独立任务或项目内任务 |
| `files` | `id` PK；关联 Workspace 和上传者 | 文件元数据，文件 API 尚未开发 |
| `operation_logs` | `id` PK；可关联 Workspace/操作人 | 操作记录模型 |

已通过数据库实际验证：`users` 唯一约束、`workspace_members` 联合主键、`projects` 的 Workspace 内名称唯一性与外键，以及非法 `projects.workspace_id` 被 PostgreSQL 拒绝。

已在 M3-T5,6,7,8 **业务层**验证的关键规则：

- 创建 Workspace 必须在**同一事务**写入 `workspaces` 与 owner 的 `workspace_members(role='owner')`；人为使第二步失败时，第一步回滚。
- 创建 Task 时，若 `project_id` 不为空，Service 检查项目确实属于所请求的 Workspace；跨 Workspace 关联被拒绝。
- 但 `tasks.workspace_id` 和 `tasks.project_id` 的**两个独立 FK**本身仍不能保证这层一致性。未来可评估更强的数据库约束，现阶段不能将 Service 校验误写为 DB 约束。
- `role`、`status` 目前为字符串字段；正式权限策略、身份认证尚未落地。

## 6. 已实现的 HTTP 与查询能力

**保留的 M2 路由：**

```http
POST   /projects
GET    /projects
GET    /projects/{project_name}
PATCH  /projects/{project_name}
DELETE /projects/{project_name}
```

**新增并有 HTTP/集成测试证据的 M3 路由：**

```http
POST /users
POST /workspaces
POST /workspaces/{workspace_id}/projects
POST /workspaces/{workspace_id}/tasks
GET  /workspaces/{workspace_id}/tasks
```

M3 Task 列表已支持：

- `limit / offset` 分页，返回 `items / total / limit / offset`；`total` 是分页之前符合筛选条件的总数。
- `status`、`project_id`、`title_contains` 组合筛选；限定 Workspace 范围。
- `sort_by`（`created_at / title / status`）和 `order`（`asc / desc`），排序字段经白名单选择，**不拼接用户输入到 SQL**。
- LEFT OUTER JOIN `projects` 返回 `project_name`；无项目的 Task 仍被保留。
- `title_contains` 采用不区分大小写的 `ILIKE`，并先转义 `/`、`%`、`_` 后使用 `escape="/"`，使搜索词里的通配符按字面匹配。

**注意**：“所有查询带 `workspace_id` 过滤”目前只是数据范围控制，**不是已实现的用户权限隔离**。M3-T09/T10 完成之前，不能把这些路由描述为受身份认证和 Workspace 成员授权保护。

M2 已稳定具备 404/409/422 错误转换，以及 `request_complete`、`business_error`、`validation_error`、`request_failed` 等日志；未知异常保持 500 和 traceback 排错语义，不默认记录密码、Token 或完整请求 Body。

## 7. Alembic、事务与最新数据库基线

**已验收环境（来自用户开发机输出，非版本锁定承诺）：**

| 组件 | 已记录版本 |
| --- | --- |
| Python | 3.14.6 |
| PostgreSQL | 16.15 |
| SQLAlchemy | 2.1.1 |
| Psycopg | 3.3.6 |
| Alembic | 1.20.0 |

**Migration 链（实测）：**

```text
<base> → 908eb712de1e  baseline core schema
       → 7e0798b22604  add task query indexes  (head)
```

最近一次 `alembic current` 位于 `7e0798b22604 (head)`；`alembic check` 返回 `No new upgrade operations detected.`。

`tasks` 已验证的查询索引：

```text
ix_tasks_workspace_project_id
ix_tasks_workspace_status_created_at
```

`m3_t01_projects` 是早期学习表，**不属于七张正式业务表**；后续 Alembic 自动比较应避免将它误判为需要删除的正式 Schema 变更。

**事务原则**：Service 持有 `session.begin()` 边界，Repository 只 `add/flush/query`，同一业务动作的多表写入要么共同成功要么一起回滚；不要在 Repository 各自 commit。

## 8. 自动化验证与可复现命令

| 验证批次 | 真实记录结果 |
| --- | --- |
| M2 完成时 | 57 passed |
| M3-T2,3,4 完成时 | 57 passed，2 warnings |
| M3-T5,6,7,8 新增 PostgreSQL 集成测试 | 10 passed |
| **最近一次包含 PostgreSQL 测试的全量回归** | **67 passed，2 warnings** |
| 最近一次 Alembic 检查 | head 正确；无新 migration 差异 |

M3 的十项数据库测试覆盖 owner membership、失败回滚、项目重名、跨 Workspace 项目/任务不一致、筛选、分页与 total、排序、LEFT JOIN、`title_contains`。旧 57 项测试仍通过。

开发环境常用命令（在项目根目录、正确虚拟环境中执行）：

```bash
python -m pip install -e ".[dev]"
alembic current
alembic history
alembic check
alembic upgrade head
uvicorn app.main:app --reload
```

**数据库测试必须显式指向独立测试库**，不得使用正式 `ai_workspace_lite`：

```bash
TEST_DATABASE_URL=postgresql+psycopg:///ai_workspace_lite_test \
python -m pytest tests/test_m3_database.py -q

TEST_DATABASE_URL=postgresql+psycopg:///ai_workspace_lite_test \
python -m pytest -q
```

运行前应为 `ai_workspace_lite_test` 完成 Alembic 迁移。数据库 fixture 检查 URL/实际数据库名称，使用外层事务与 SAVEPOINT 隔离，每条测试结束回滚。**如果未设置 `TEST_DATABASE_URL`，数据库集成测试会跳过；不能将这种结果算作 67 项全覆盖。**

当前 2 条 warning 分别来自 Starlette TestClient 的 `httpx` 兼容迁移提示与 Starlette/AnyIO 的弃用 API；它们不是本次测试失败。新增的特殊字符筛选和 `project_id` 组合筛选增强测试曾被建议，但**尚无它们在用户 PostgreSQL 环境中实际通过的证据**，不得计入 67 项基线。

## 9. 已知边界、文档债务和下一步

**已知但不阻断当前验收：**

- 旧 JSON Project 与新 PostgreSQL Project 分属两条业务链；**尚未进行数据迁移或统一 CRUD**。
- Task–Project 的 Workspace 一致性已由 Service 校验，但不是两个独立 FK 自动保障。
- Workspace owner 与 owner membership 的原子创建已实现；更完整的角色授权、Token、401/403 尚未实现。
- 文件表和操作日志表已有 ORM 模型，不代表文件上传、下载、审计 API 已完成。
- 任务状态/成员角色仍可在后续业务阶段强化约束。
- `README.md` / `AGENTS.md` 曾出现滞后，后续 AI 应先读实际代码与最新学习记录。
- M3-T5,6,7,8 的**技术验收已通过**，但正式学习记录和远程同步状态仍待确认。

**下次继续工作时的顺序：**

1. 核对 GitHub 实时源码、Alembic revisions、`tests/test_m3_database.py`，确认本文件未过时；核实 `learning_records/M3-T5,6,7,8.md` 是否已同步，必要时补齐收口。
2. 进入 **M3-T09｜密码 Hash、登录与 Token**；基于已有 `users`、Service/Repository、Session/Migration 体系做增量实现，不重新起一套项目。
3. 随后 **M3-T10｜401/403 与工作空间成员权限隔离**，再进入文件安全任务 T11/T12；不要提前宣称认证/授权已经完成。
4. 每张任务先解释数据流与职责边界，再做最小增量；覆盖成功和失败路径；取得真实测试结果后写 `learning_records/Mx-Txx.md` 并更新本摘要，再标记正式收口。

**本摘要的维护目标**：只保留 *现在是什么、已经验证了什么、仍缺什么、去哪里查源码、下一步是什么*。逐行 SQL、长篇课程讲解、单次 traceback 和完整测试日志应留在源码、测试文件或相应的 `learning_records/`，不要再复制到这里。
