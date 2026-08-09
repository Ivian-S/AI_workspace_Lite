# 仓库指南

## 项目结构与模块组织

AI Workspace Lite 是一个渐进式 Python 后端学习项目。生产代码放在 `app/`，测试放在 `tests/`。当前入口为 `app/main.py`；包级常量放在 `app/__init__.py`。随着里程碑逐步实现 CLI 管理器，请按职责拆分为聚焦的模块，例如 `models.py`、`services.py`、`storage.py` 和 `exceptions.py`，具体规划见 `README.md` 与 `StudyPLAN.md`。

测试应按验证的功能组织，而不是与实现文件同路径存放：例如，用 `tests/test_services.py` 测试服务层行为。请勿将运行时数据、本地虚拟环境或生成的 JSON 文件放入 `app/`。

## 构建、测试与开发命令

使用 Python 3.11 或更高版本。在仓库根目录执行：

```bash
python -m pip install -e ".[dev]"  # 安装项目与 pytest
python -m app.main                 # 运行当前应用入口
python -m pytest                   # 运行全部测试
python -m pytest tests/test_smoke.py -q  # 运行单个测试模块
```

当前里程碑尚未引入格式化工具、代码检查工具、Docker 配置或 API 服务。这些工具成为项目依赖后，请在此补充对应命令。

## 代码风格与命名规范

遵循标准 Python 规范：使用四个空格缩进；函数、变量和模块使用 `snake_case`；类使用 `PascalCase`；常量使用 `UPPER_SNAKE_CASE`。优先编写小型、带类型标注且返回类型明确的函数，例如 `def create_project(name: str) -> Project:`。使用从 `app` 开始的绝对导入，保持模块职责单一，并抛出具体异常；禁止使用裸 `except`。

## 测试指南

测试框架为 pytest。测试文件命名为 `test_*.py`，测试函数命名为 `test_*`；断言应具备确定性，避免依赖机器特定路径或已有数据。功能变更时，应同时覆盖成功路径和预期失败路径。CLI 项目管理器完成后，M1 学习计划要求至少八个测试。

## 提交与拉取请求指南

现有提交历史使用简洁、祈使语气的 Conventional Commit 风格，例如 `chore: v1_M1T01_finished`。请继续使用 `feat:`、`fix:`、`test:`、`docs:` 和 `chore:` 等前缀；适合时标注相关里程碑或任务。每次提交应保持聚焦。

拉取请求应说明所属里程碑或任务，概述行为变更，列出验证命令及结果，并在可能时关联相关 issue。对于用户可见的 CLI/API 变更，应附上终端输出或截图；请勿提交包含失败测试的变更。
