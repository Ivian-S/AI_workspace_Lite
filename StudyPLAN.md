核心顺序：**Python → HTTP/FastAPI → 数据库/权限 → Linux/Docker → 模型 API → Tool Calling → Workflow/RAG → 工程完善**，不会提前堆 Agent 框架。

整个过程只维护一个项目：`/project` 的 **AI Workspace Lite**。附件明确要求它从普通项目管理系统逐步长成 AI 工作空间，而不是不断新建练手项目。

# AI Workspace Lite · 八大里程碑目录

## M1｜Python 工程化地基

**对应：第 1–2 周**

目标不是“再学一遍 Python 语法”，而是从单文件脚本跨到**可维护的多文件工程**：模块、包、异常、类型、虚拟环境、测试和 Git。附件把这一阶段的验收重点放在“能解释文件职责、解决导入问题、独立加字段、写测试和使用 Git”。

**原子任务卡片：**

* **M1-T01｜建立 `/project` 与 Python 工程骨架**

  * `pyproject.toml`
  * `app/`
  * `tests/`
  * 虚拟环境与依赖管理

* **M1-T02｜Python 对象引用与可变对象**

  * `list/dict/set/tuple`
  * 引用
  * 浅拷贝/深拷贝
  * 参数传递

* **M1-T03｜函数、类型注解与数据模型**

  * 参数/返回值
  * `None`
  * dataclass
  * 类型注解

* **M1-T04｜类、组合与模块职责**

  * Model / Service / Storage 的最小拆分
  * 重点理解“谁负责什么”

* **M1-T05｜模块、包与 Import 排错**

  * 绝对导入
  * 包
  * 项目根目录
  * `ModuleNotFoundError`
  * 循环导入认知

* **M1-T06｜异常处理与业务异常**

  * 捕获具体异常
  * `raise`
  * 自定义异常
  * 不允许裸 `except`

* **M1-T07｜JSON 持久化项目管理器**

  * 创建/查询/修改/删除 Project
  * JSON 文件读写

* **M1-T08｜pytest + Debugger + Git 基线**

  * ≥8 个测试
  * 断点调试
  * Git commit
  * 查看 diff

**阶段产物：**

```text
/project
├── app/
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   ├── storage.py
│   └── exceptions.py
├── tests/
└── pyproject.toml
```

---

## M2｜HTTP 与 FastAPI 后端基础

**对应：第 3–4 周**

这一阶段把 CLI 改造成真正的 HTTP 服务，核心不是背 FastAPI 装饰器，而是能解释：

`客户端 → HTTP → Router → 业务逻辑 → 数据 → Response`。

**原子任务卡片：**

* **M2-T01｜HTTP 请求/响应与 REST**

  * Method
  * URL
  * Header
  * Body
  * Status Code

* **M2-T02｜FastAPI 最小应用与启动流程**

  * `main.py`
  * 路由
  * OpenAPI/Swagger

* **M2-T03｜路径参数与查询参数**

  * Path
  * Query
  * 参数类型转换

* **M2-T04｜Pydantic 请求体与校验**

  * Request Schema
  * 422 的来源

* **M2-T05｜Projects CRUD API**

  * `POST /projects`
  * `GET /projects`
  * `GET /projects/{id}`
  * `PATCH`
  * `DELETE`

* **M2-T06｜404、重复数据与统一异常**

  * 业务异常 → HTTP 响应

* **M2-T07｜日志与请求排错**

  * 404 / 422 / 500
  * 参数在哪里丢失

* **M2-T08｜FastAPI 接口测试**

  * 正常路径
  * 非法输入
  * 不存在资源

**里程碑验收：**

你必须能独立解释一个 HTTP 请求到底经过了哪些函数，而不是只会“访问 Swagger 点 Execute”。

---

## M3｜PostgreSQL、ORM、项目分层与权限

**对应：第 5–8 周**

这里开始进入真正后端工程。附件要求建立 `Router → Service → Repository → Database` 分层，并增加用户、工作空间、任务、成员、文件和日志等核心实体。

第 8 周继续补认证、权限和文件管理。

**原子任务卡片：**

* **M3-T01｜PostgreSQL 基础与 SQL CRUD**

* **M3-T02｜主键、外键与实体关系设计**

* **M3-T03｜设计 AI Workspace Lite 核心表**

  * `users`
  * `workspaces`
  * `workspace_members`
  * `projects`
  * `tasks`
  * `files`
  * `operation_logs`

* **M3-T04｜SQLAlchemy ORM 与 Session**

* **M3-T05｜Router / Service / Repository 分层**

* **M3-T06｜数据库迁移**

* **M3-T07｜事务：一个业务操作修改多张表**

* **M3-T08｜分页、排序、筛选与 JOIN**

* **M3-T09｜密码 Hash、登录与 Token**

* **M3-T10｜401 / 403 与工作空间权限隔离**

* **M3-T11｜安全文件上传**

  * 大小限制
  * 类型限制
  * 路径安全

* **M3-T12｜文件下载/删除与权限校验**

**核心能力验收：**

必须能回答：

> 为什么 API 层不能直接写一堆 SQL？

> 为什么 `task` 必须与 Workspace 建立边界？

> 用户传一个 `workspace_id`，为什么不能直接相信？

---

## M4｜Linux 服务排错与 Docker 化

**对应：第 9–12 周**

第 9–10 周不是背 Linux 命令，而是把 `/project` 真正部署起来并制造故障；第 11–12 周再容器化 FastAPI 和 PostgreSQL。 

**原子任务卡片：**

* **M4-T01｜Linux 文件、权限与环境变量**

* **M4-T02｜进程、端口与资源排查**

* **M4-T03｜日志与服务启动失败排查**

* **M4-T04｜SSH 部署 `/project`**

* **M4-T05｜Shell 启动脚本**

  * `start.sh`

* **M4-T06｜Shell 健康检查脚本**

  * `health_check.sh`

* **M4-T07｜编写 Dockerfile**

* **M4-T08｜镜像、容器与端口映射**

* **M4-T09｜Docker Volume 与数据库持久化**

* **M4-T10｜Docker 网络**

  * 重点排查：
  * 为什么容器里不能用 `localhost` 连 PostgreSQL

* **M4-T11｜Docker Compose**

  * FastAPI
  * PostgreSQL

* **M4-T12｜容器级故障演练**

  * 重启循环
  * 错误环境变量
  * 端口冲突
  * 数据丢失
  * DB 未就绪

**最终要求：**

```bash
docker compose up -d
```

能够启动整个非 AI 版 Workspace。

---

# 从这里开始，才正式进入 AI 应用

这是路线中的关键分界线。

附件明确指出，真正目标是 **Python 后端 + AI 应用 + Linux/Docker + 模型服务集成**，而不是“大模型训练工程师”。

---

## M5｜LLM 服务集成与多模型适配

**对应：第 13–15 周**

先学普通模型 API，再碰本地模型；先理解“应用如何调用模型服务”，而不是研究推理引擎源码。

**原子任务卡片：**

* **M5-T01｜LLM 请求的数据结构**

  * system/user/assistant
  * Token
  * Context

* **M5-T02｜实现 `/ai/chat`**

* **M5-T03｜实现流式 `/ai/chat/stream`**

* **M5-T04｜结构化输出 `/ai/extract-task`**

* **M5-T05｜超时、重试与错误分类**

* **M5-T06｜模型调用日志**

* **M5-T07｜API Key 与配置安全**

* **M5-T08｜Ollama 本地模型服务**

* **M5-T09｜LM Studio API 接入**

* **M5-T10｜统一 `ModelProvider` 抽象**

* **M5-T11｜配置驱动的模型切换**

* **M5-T12｜Provider 健康检查与失败回退**

### 仅认知卡片，不实操

* `llama.cpp`
* GGUF
* 量化
* CPU/GPU 混合推理
* vLLM 的定位

附件也明确要求 llama.cpp 暂时不研究源码，vLLM 则等有适合 GPU 环境再进一步实践。

---

## M6｜安全 Tool Calling

**对应：第 16 周**

这一阶段的重点不是“让模型能调用函数”，而是：

> **模型提出意图，后端决定是否允许执行。**

附件特别要求权限、超时、幂等、日志以及写操作确认。

**原子任务卡片：**

* **M6-T01｜Tool Schema 设计**
* **M6-T02｜工具参数校验**
* **M6-T03｜实现 `list_projects`**
* **M6-T04｜实现 `get_project`**
* **M6-T05｜实现 `list_tasks`**
* **M6-T06｜实现 `create_task`**
* **M6-T07｜实现 `search_files`**
* **M6-T08｜实现 `get_file_metadata`**
* **M6-T09｜工具权限检查**
* **M6-T10｜工具超时与失败处理**
* **M6-T11｜写操作幂等与重复执行防护**
* **M6-T12｜人工确认机制**
* **M6-T13｜Tool Call 审计日志**

**红线：**

LLM **永远不能直接拥有数据库操作权限**。

---

## M7｜Workflow、Agent 与知识库

**对应：第 17–19 周**

先用普通 Python 实现确定性工作流，之后才能接 LangGraph。附件明确反对“把工作流逻辑全部藏进 Prompt”。

第 19 周再增加 RAG / 知识库和工作空间隔离。

**原子任务卡片：**

* **M7-T01｜纯 Python 确定性 Workflow**
* **M7-T02｜State 与执行上下文**
* **M7-T03｜条件分支**
* **M7-T04｜失败重试**
* **M7-T05｜最大执行次数**
* **M7-T06｜写操作人工确认节点**
* **M7-T07｜状态持久化**
* **M7-T08｜Workflow 执行日志**
* **M7-T09｜LangGraph 认知与最小迁移**
* **M7-T10｜文档解析**
* **M7-T11｜文本切分与索引**
* **M7-T12｜Embedding / 向量检索**
* **M7-T13｜工作空间级检索隔离**
* **M7-T14｜回答来源引用**
* **M7-T15｜无答案时禁止编造**
* **M7-T16｜恶意跨 Workspace Prompt 测试**

### 仅认知卡片

* 多 Agent 复杂协作
* Agent 框架生态比较

不进行“框架动物园”式实操。

---

## M8｜工程收口、故障演练与面试级验收

**对应：第 20 周**

最后一周不是继续加炫酷功能，而是把整个项目变成一个**别人能够启动、测试、理解和修改的工程**。附件要求补全测试、README、架构图、部署说明、故障排查手册，并能解释请求如何穿过整个系统。

**原子任务卡片：**

* **M8-T01｜测试债务清理**

* **M8-T02｜统一异常体系**

* **M8-T03｜统一结构化日志**

* **M8-T04｜健康检查**

* **M8-T05｜环境变量与 `.env.example`**

* **M8-T06｜Docker Compose 最终部署**

* **M8-T07｜README**

* **M8-T08｜系统架构图**

* **M8-T09｜数据库 ER 图**

* **M8-T10｜API 文档**

* **M8-T11｜模型配置文档**

* **M8-T12｜故障排查手册**

* **M8-T13｜端到端故障演练**

* **M8-T14｜随机需求修改演练**

  * 例如：
  * 给 Task 增加 `assignee`
  * 数据库迁移
  * ORM
  * Schema
  * Service
  * API
  * 测试
  * 部署升级

* **M8-T15｜项目答辩与面试问答**

附件给出的最终衡量标准非常实用：面试官临时让你给任务增加“负责人”字段并支持查询，你应能自己判断需要修改数据库、迁移、ORM、Schema、Service、API、测试以及旧数据兼容问题。

---

# 20 周 → 八大里程碑映射

| 周期         | 里程碑                       | 项目形态                 |
| ---------- | ------------------------- | -------------------- |
| Week 1–2   | **M1 Python 工程化地基**       | CLI 项目管理器            |
| Week 3–4   | **M2 HTTP + FastAPI**     | Web API              |
| Week 5–8   | **M3 数据库 + 分层 + 权限 + 文件** | 正常 Workspace 后端      |
| Week 9–12  | **M4 Linux + Docker**     | 可部署 Workspace        |
| Week 13–15 | **M5 LLM 服务集成**           | AI Workspace         |
| Week 16    | **M6 Tool Calling**       | 可安全操作 Workspace 的 AI |
| Week 17–19 | **M7 Workflow + RAG**     | AI 项目助手              |
| Week 20    | **M8 工程收口**               | 可演示、可部署、可面试项目        |

我们的执行方式也固定下来：**你指定一个 `Mx` 或 `Mx-Txx`，我才展开那个任务，不提前输出后续课程。** 每个具体任务都会严格采用你规定的 7 段格式，并且代码始终基于 `/project` 增量演进；每节最后都会留下必须独立完成的“无 AI 验收任务”。附件本身也要求每天保留无 AI 时间，通过独立写接口、SQL、测试、Bug 定位或数据流图来保持代码控制能力。

**下一步请直接回复：`M1` 或具体卡片，例如 `M1-T01`。**
