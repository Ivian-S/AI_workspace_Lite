# AI Workspace Lite

一个从零开始、逐步演进的 Python 后端工程实战项目。

## 项目定位

从 CLI 项目管理器起步，历经 **Web API → 数据库分层 → Docker 部署 → LLM 集成 → Tool Calling → Workflow/RAG → 工程收口**，最终成长为一个可演示、可部署、可面试的 AI 项目助手。

## 路线图

| 周期 | 里程碑 | 项目形态 |
|------|--------|----------|
| Week 1–2 | **M1 Python 工程化地基** | CLI 项目管理器 |
| Week 3–4 | **M2 HTTP + FastAPI** | Web API |
| Week 5–8 | **M3 数据库 + 分层 + 权限 + 文件** | 正常 Workspace 后端 |
| Week 9–12 | **M4 Linux + Docker** | 可部署 Workspace |
| Week 13–15 | **M5 LLM 服务集成** | AI Workspace |
| Week 16 | **M6 Tool Calling** | 可安全操作 Workspace 的 AI |
| Week 17–19 | **M7 Workflow + RAG** | AI 项目助手 |
| Week 20 | **M8 工程收口** | 可演示、可部署、可面试项目 |

## 项目结构

```
/project
├── app/                  # 应用核心代码
│   ├── main.py          # 入口
│   ├── models.py        # 数据模型
│   ├── services.py      # 业务逻辑
│   ├── storage.py       # 数据持久化
│   └── exceptions.py    # 自定义异常
├── tests/               # 测试
├── pyproject.toml       # 项目配置与依赖
├── StudyPLAN.md         # 详细学习计划
└── README.md
```

> 项目结构随里程碑逐步演进，最终将包含数据库、API 路由、Docker 编排、LLM 服务集成等完整工程目录。

## 学习方式

- 每个里程碑（M1–M8）拆分为若干原子任务卡片（T01–Txx）
- 按序推进，不提前输出后续内容
- 每节末尾留有**无 AI 验收任务**，确保独立代码控制能力
- 全程仅维护一个项目，不新建练手项目

## 里程碑一览

### M1 — Python 工程化地基
模块、包、异常、类型注解、虚拟环境、pytest、Git。产出基于 JSON 持久化的 CLI 项目管理器。

### M2 — HTTP 与 FastAPI 后端基础
CLI → HTTP API，理解请求/响应周期、路由、Pydantic 校验、RESTful CRUD 与接口测试。

### M3 — PostgreSQL、ORM、分层与权限
引入 Router → Service → Repository → Database 四层架构，实现用户、工作空间、项目、任务、文件等核心实体，覆盖认证、权限隔离与文件管理。

### M4 — Linux 服务排错与 Docker 化
Linux 服务部署与故障排查，编写 Dockerfile 与 Docker Compose，容器化 FastAPI + PostgreSQL。

### M5 — LLM 服务集成
实现 `/ai/chat`、流式响应、结构化输出、多模型 Provider 抽象（OpenAI / Ollama / LM Studio），支持配置驱动的模型切换与失败回退。

### M6 — 安全 Tool Calling
模型提意图，后端决定执行。实现工具 Schema、参数校验、权限检查、超时、幂等、人工确认与审计日志。

### M7 — Workflow、Agent 与知识库
纯 Python 确定性 Workflow → LangGraph 迁移，文档解析 → 文本切分 → Embedding → 向量检索 → 来源引用，工作空间级检索隔离。

### M8 — 工程收口
补全测试、统一异常与日志、健康检查、架构图、ER 图、API 文档、Docker Compose 最终部署、故障排查手册、随机需求修改演练。

## 启动

（各阶段启动方式不同，详见对应里程碑说明）

```bash
# M1 阶段
cd project
python -m app.main

# M4+ 阶段
docker compose up -d
```

## 许可

仅供个人学习使用。