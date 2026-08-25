# 仓库指南

## 项目与当前阶段

AI Workspace Lite 是一个按 `StudyPLAN.md` 渐进实现的 Python 后端学习项目。当前处于 **M1 Python 工程化地基**，M1-T01 ～ M1-T04 已完成，下一任务是 **M1-T05 模块、包与 Import 排错**。

当前已有 `Project` dataclass、`ProjectService`、`InMemoryProjectStorage` 和 19 个测试。应用入口目前只输出名称与版本；业务异常、JSON 持久化和完整 CLI CRUD 尚未实现，不要在当前任务中提前引入 FastAPI、数据库或 Docker。

## 项目结构与模块职责

生产代码放在 `app/`，测试放在 `tests/`：

- `app/main.py`：当前应用入口；
- `app/models.py`：`Project` 数据模型；
- `app/services.py`：创建、列出和查询项目的业务动作；
- `app/storage.py`：进程内存储实现；
- `app/project_state.py`：M1-T02 / M1-T03 的引用、复制与可变状态实验；
- `tests/test_smoke.py`：应用常量冒烟测试；
- `tests/test_project_state.py`：模型与状态行为测试；
- `tests/test_services.py`：Service / Storage 行为测试。

新增模块时保持单一职责，并使用从 `app` 开始的绝对导入。测试按功能组织，不要求与实现文件一一对应。不要把运行时数据、生成的 JSON、虚拟环境或缓存文件放入 `app/`。

## 学习进度记录

`learning_records/` 是任务正式收口的一部分。每完成一个里程碑或原子任务，必须新增或更新对应的 `Mx-Txx.md`，至少写明：

- 完成内容与涉及文件；
- 关键设计或学习结论；
- 验证命令与实际结果；
- 遗留问题及其计划归属；
- 下一任务。

随后同步更新 `learning_records/summary.md`，只保留最新项目快照，不重复任务记录中的长篇教学过程。发生信息冲突时，以当前代码和测试结果为第一事实来源，其次是最新任务记录，再其次是 summary。

## 构建、测试与开发命令

使用 Python 3.11 或更高版本，在仓库根目录执行：

```bash
python -m pip install -e ".[dev]"       # 安装项目与 pytest
python -m app.main                       # 运行当前应用入口
python -m pytest -q                      # 运行全部测试
python -m pytest tests/test_smoke.py -q  # 运行单个测试模块
```

未激活虚拟环境且系统不存在 `python` 命令时，可使用 `.venv/bin/python`。截至 2026-08-25 的基线是 `19 passed`，入口输出 `AI Workspace Lite started. 0.1.0`。功能变更后必须重新运行相关测试和全量测试，不要只沿用历史结果。

当前尚未引入格式化器、代码检查器、Docker 或 API 服务；引入后再补充相应命令。

## 代码风格与设计边界

遵循标准 Python 规范：四个空格缩进；函数、变量和模块使用 `snake_case`；类使用 `PascalCase`；常量使用 `UPPER_SNAKE_CASE`。函数应尽量小且职责明确，使用准确的参数和返回类型注解。

- Model 表达数据，Service 组织业务动作，Storage 负责数据存取；
- Service 通过组合使用 Storage，不继承 Storage；
- 不直接访问 `_projects`，也不向调用方泄漏内部 collection；
- 外部传入的可变对象应明确选择共享或复制，不能无意共享状态；
- 类型注解不等于运行时校验；不要在 M1 当前阶段擅自引入 Pydantic；
- 抛出和捕获具体异常，禁止裸 `except`；自定义业务异常按 M1-T06 引入。

## 测试指南

使用 pytest。测试文件命名为 `test_*.py`，测试函数命名为 `test_*`，断言必须确定且真正验证需求，避免依赖机器特定路径或已有数据。

行为变更应同时覆盖成功路径和预期失败路径。除确认测试绿色外，还要确认预期用例已被 pytest 收集。新增 `Project` 字段时，应审计创建、复制和重建对象的全部路径，并增加回归测试。

## 提交与拉取请求

提交采用简洁、聚焦的 Conventional Commit 风格，如 `feat:`、`fix:`、`test:`、`docs:` 和 `chore:`；适合时在主题中标注里程碑或任务。

拉取请求应说明所属里程碑或任务、行为变化、验证命令及结果，并在可能时关联 issue。用户可见的 CLI/API 变化应附终端输出或截图；不要提交失败的测试。
