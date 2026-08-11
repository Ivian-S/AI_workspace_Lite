# AI Workspace Lite 项目进度总结

## 项目概览

* **项目名称**：AI Workspace Lite
* **当前所处大阶段**：M1（Python 工程化地基）
* **当前已完成卡片**：

  * **M1-T01｜建立 `/project` 与 Python 工程骨架**
  * **M1-T02｜Python 对象引用与可变对象**
  * **M1-T03｜函数、类型注解与数据模型**

当前项目仍处于：

M1｜Python 工程化地基

## 当前阶段目标

M1 阶段的总体目标是将项目从单文件脚本逐步发展为**可维护、可测试、职责清晰的多文件 Python 工程**。

本阶段重点包括：

* Python 模块与包；
* 函数、类型注解与数据模型；
* 对象引用与可变对象；
* 类、组合与模块职责；
* Import 与项目根目录；
* 异常处理；
* 虚拟环境与依赖管理；
* pytest 测试；
* Debugger；
* Git 基础。

阶段验收重点是能够理解并解释各文件职责、解决常见导入问题、独立修改数据结构、编写测试并使用 Git 管理项目。

## 已完成任务详情

### M1-T01：建立 `/project` 与 Python 工程骨架

* **完成日期**：2026-08-09

* **核心产出**：

  * 建立 `app/` 应用代码目录；
  * 建立 `tests/` 测试目录；
  * 新增并配置 `pyproject.toml`；
  * 配置可编辑安装及 pytest 开发依赖；
  * 新增 `app/info.py`，通过 `APP_VERSION` 暴露应用版本；
  * 更新 `app/main.py`，使应用启动时输出应用名称和版本；
  * 增加冒烟测试，验证应用名称和版本常量。

* **关键知识点**：

  * Python 多文件工程的基本目录结构；
  * `pyproject.toml` 的基础作用；
  * Python 包和模块；
  * 项目入口；
  * 开发依赖管理；
  * 可编辑安装；
  * pytest 冒烟测试。

* **测试结果**：

  * `pytest`：**2 passed**
  * 应用入口验证输出：

    ```text
    AI Workspace Lite started. 0.1.0
    ```

* **遗留问题或注意事项**：

  * 此时项目仍只有基础工程骨架与冒烟测试；
  * 数据模型、业务逻辑、JSON 持久化及更完整测试尚未实现；
  * 后续 M1 卡片将在当前工程骨架上持续增量开发。

### M1-T02：Python 对象引用与可变对象

* **完成日期**：2026-08-10

* **核心产出**：

  新增核心模块：

  ```text
  app/project_state.py
  ```

  当前模块实现了 Project 的基础状态操作，包括：

  * `create_project(name)`

    * 创建 Project；
    * 保存传入的项目名称；
    * 每次调用独立创建 `tags`；
    * 每次调用独立创建 `members`。

  当前 Project 基础结构：

  ```python
  {
      "name": name,
      "tags": [],
      "members": [],
  }
  ```

  * `add_tag_in_place()`

    * 使用 `append()` 原地修改 Project 的 `tags`；
    * 用于展示函数内部修改共享可变对象的行为。

  * `with_tag()`

    * 不直接修改原 Project；
    * 返回新的 Project 字典；
    * 为返回结果创建新的 `tags` 列表；
    * 用于对比“原地修改”与“返回新对象”两种设计。

  * `create_project_test1(name, tags=[])`

    * 用于实验和观察可变默认参数造成的共享问题。

  * `create_project_test2(name, tags=None)`

    * 使用 `None` 作为默认值；
    * 在函数内部创建新列表，避免默认可变对象被不同调用共享。

  * `clone_project()`

    * 返回新的 Project 字典；
    * 独立复制当前结构中的 `tags`；
    * 独立复制 `members`；
    * 当前没有直接使用 `deepcopy()`，而是根据已知数据结构显式复制需要隔离的可变字段。

  新增测试模块：

  ```text
  tests/test_project_state.py
  ```

  包含 6 个专项测试：

  1. 验证赋值后两个变量引用同一个 Project；
  2. 验证 `add_tag_in_place()` 会修改原 Project；
  3. 验证 `with_tag()` 返回新 Project，并且不会修改原 `tags`；
  4. 验证两个独立创建的 Project 不共享 `members`；
  5. 验证 `dict.copy()` 浅拷贝仍然共享嵌套 `members`；
  6. 验证 `clone_project()` 返回不同 Project，并隔离 `tags` 和 `members`。

* **关键知识点**：

  * Python 变量保存的是对象引用；
  * `b = a` 不会自动复制对象；
  * `==` 与 `is` 的区别；
  * `list`、`dict` 等可变对象的共享状态；
  * 函数参数与调用者共享对象时的修改行为；
  * 原地修改（in-place mutation）；
  * 返回新对象的数据处理方式；
  * 浅拷贝；
  * 深拷贝；
  * 可变默认参数风险；
  * 使用 `None` 避免默认列表共享；
  * 根据数据结构和职责选择复制策略。

* **测试结果**：

  M1-T02 专项测试：

  ```bash
  pytest tests/test_project_state.py
  ```

  结果：

  ```text
  6 passed
  ```

  项目全量回归：

  ```bash
  pytest
  ```

  结果：

  ```text
  collected 8 items

  tests/test_project_state.py ...... [ 75%]
  tests/test_smoke.py ..             [100%]

  8 passed in 0.10s
  ```

* **遗留问题或注意事项**：

  * `clone_project()` 当前只针对已知的 `tags` 和 `members` 做显式的一层复制；
  * 如果未来 `members` 内部继续出现嵌套的 `dict`、`list` 等可变对象，现有复制策略将不足以保证完全隔离，需要重新评估；
  * 不应因为存在 `deepcopy()` 就默认对所有对象进行深拷贝，应先明确哪些状态应该共享、哪些必须隔离；
  * 当前 Project 仍使用裸 `dict` 表示，这是 M1-T02 阶段刻意保留的简单结构；
  * `create_project_test1()`、`create_project_test2()` 属于学习实验函数，后续进入正式业务开发后不应长期作为生产 API 保留；
  * 测试本身同样需要 Code Review：曾出现测试通过但业务代码实际上没有正确使用 `name` 参数的问题；
  * 曾出现测试函数因为没有使用 `test_...` 命名而未被 pytest 收集的问题，因此后续不能只关注 `passed`，还应确认预期测试确实被 collected。

### M1-T03：函数、类型注解与数据模型

* **完成日期**：2026-08-11

* **核心产出**：

  新增数据模型模块：

  ```text
  app/models.py
  ```

  新增 `Project` dataclass：

  ```python
  @dataclass
  class Project:
      name: str
      description: str | None = None
      tags: list[str] = field(default_factory=list)
      members: list[str] = field(default_factory=list)
  ```

  Project 从 M1-T02 的裸 `dict` 结构正式演进为字段明确的数据对象。

  修改：

  ```text
  app/project_state.py
  ```

  将核心 Project 操作增加类型注解并迁移至 dataclass：

  * `create_project(...) -> Project`
  * `add_tag_in_place(...) -> None`
  * `with_tag(...) -> Project`
  * `clone_project(...) -> Project`

  `create_project()` 当前支持：

  * `name: str`
  * `description: str | None`
  * `tags: list[str] | None`
  * `members: list[str] | None`

  对外部传入的 `tags` 和 `members` 建立独立列表，避免无意共享调用者的可变对象。

  独立验收中增加：

  ```text
  description
  ```

  字段。

  其类型为：

  ```python
  str | None
  ```

  默认值为：

  ```python
  None
  ```

* **关键知识点**：

  * 函数参数类型注解；
  * 函数返回值类型注解；
  * `None` 与可选类型；
  * `str | None`；
  * `list[str]`；
  * `dataclass`；
  * `field(default_factory=list)`；
  * 类型注解与运行时校验的区别；
  * 原地修改函数与返回新对象函数的接口差异；
  * 外部可变对象与内部状态隔离；
  * 数据模型增加字段后检查所有复制和重新构造路径；
  * 测试绿色不等于测试断言一定有效。

* **Code Review 结果**：

  Review 中发现增加 `description` 后，最初版本的 `with_tag()` 创建新 Project 时遗漏该字段，会造成：

  ```text
  original.description 有值
  → with_tag()
  → updated.description 变为 None
  ```

  该问题属于真实的数据丢失回归。

  已增加：

  ```text
  test_with_tag_preserves_description
  ```

  对该行为建立回归保护，最终测试通过。

  Review 同时发现原对象引用测试中存在“测试通过但断言验证力度不足”的问题。

  后续测试要求继续遵守：

  ```text
  断言真正验证需求
  +
  预期测试被 pytest collected
  +
  全量回归通过
  ```

* **测试结果**：

  执行：

  ```bash
  pytest -v
  ```

  最终结果：

  ```text
  collected 13 items
  13 passed in 0.08s
  ```

  当前组成：

  ```text
  tests/test_project_state.py   11
  tests/test_smoke.py            2
  -------------------------------
  总计                          13
  ```

* **Git 状态**：

  M1-T03 修改已提交 Git，并已同步远程仓库。

* **遗留问题或注意事项**：

  * Python 类型注解目前主要用于表达设计意图和辅助静态分析，不等于完整运行时输入校验；
  * 当前没有提前引入 Pydantic；
  * `clone_project()` 仍然基于当前简单的 `list[str]` 数据结构显式复制字段；
  * 如果未来出现更复杂的嵌套可变对象，需要重新评估复制策略；
  * `Project` 当前主要负责表达数据，不提前承担 Service / Storage 等业务职责；
  * M1-T02 中的部分学习实验函数和历史注释后续需要逐步清理；
  * 数据模型新增字段以后，必须检查所有构造新对象、复制对象、序列化对象的代码路径。

---

## 项目结构与文件职责

当前目录快照：

```text
.
├── AGENTS.md
├── README.md
├── StudyPLAN.md
├── app
│   ├── __init__.py
│   ├── models.py
│   ├── project_state.py
│   ├── __pycache__
│   │   ├── __init__.cpython-312.pyc
│   │   ├── __init__.cpython-314.pyc
│   │   ├── info.cpython-312.pyc
│   │   ├── info.cpython-314.pyc
│   │   ├── main.cpython-312.pyc
│   │   ├── main.cpython-314.pyc
│   │   ├── project_snapshot.cpython-314.pyc
│   │   └── project_state.cpython-314.pyc
│   ├── info.py
│   ├── main.py
│   ├── project_state.py
│   └── temp.py
├── learning_records
│   ├── M1-T01.md
│   └── M1-T02.md
├── pyproject.toml
└── tests
    ├── __pycache__
    │   ├── test_project_snapshot.cpython-314-pytest-9.1.1.pyc
    │   ├── test_project_state.cpython-314-pytest-9.1.1.pyc
    │   └── test_smoke.cpython-314-pytest-9.1.1.pyc
    ├── test_project_state.py
    └── test_smoke.py

6 directories, 24 files
```

### `app/`

项目当前的 Python 应用代码目录。

#### `app/__init__.py`

使 `app` 可以作为 Python 包使用。

#### `app/info.py`

保存应用基础信息。

当前已知职责是通过：

```python
APP_VERSION
```

暴露应用版本。

#### `app/main.py`

当前应用入口模块。

M1-T01 中已实现启动时输出应用名称及版本，用于验证包安装、模块导入以及程序入口能够正常工作。


#### `app/models.py`

当前负责定义项目中的基础数据模型。

目前包含：

```text
Project
```

`Project` 当前字段：

```text
name
description
tags
members
```

该模块的目标是明确：

```text
Project 数据长什么样
```

而不是承担复杂业务操作。

#### `app/project_state.py`

* 创建 Project；
* Project tag 原地修改；
* 返回新的带 tag Project；
* Project 克隆；
* 对调用者传入的可变列表进行状态隔离；
* 保留部分 M1-T02 对象引用和可变对象学习实验。

当前已经开始使用：

```text
Project dataclass
+
函数类型注解
```

但尚未进入正式 Service / Storage 分层。

#### `app/temp.py`

当前目录中存在该文件，但本次提供材料没有说明其具体职责，因此暂不做进一步推断。

#### `app/__pycache__/`

Python 自动生成的字节码缓存目录，不属于项目核心源代码。

### `tests/`

项目测试目录。

#### `tests/test_smoke.py`

M1-T01 建立的基础冒烟测试。

当前已知覆盖：

* 应用名称；
* 应用版本常量。

共 2 个测试。

#### `tests/test_project_state.py`

M1-T02 新增的 Project 状态专项测试。

共 6 个测试，重点验证：

* 对象引用共享；
* 原地修改；
* 返回新对象；
* 独立 Project 的可变字段隔离；
* 浅拷贝的嵌套引用共享；
* `clone_project()` 的字段隔离行为。

### `learning_records/`

存放已完成任务卡片的学习和工程记录。

当前包含：

```text
M1-T01.md
M1-T02.md
```

这些文件记录任务完成日期、代码变更、知识点、测试结果、Code Review 结果以及下一步计划，是后续维护本进度总结的重要依据。

### `pyproject.toml`

Python 项目的构建、元数据和依赖配置文件。

当前配置包括：

```toml
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "ai-workspace-lite"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8,<10",
]
```

目前没有声明运行时第三方依赖。

### `README.md`、`StudyPLAN.md`、`AGENTS.md`

这些文件存在于当前项目目录中，但本次材料没有提供其完整内容，因此本总结不进一步推断其具体职责。

## 环境与依赖

### Python 版本

`pyproject.toml` 当前要求：

```text
Python >= 3.11
```

这是项目声明的最低 Python 版本要求。

### 虚拟环境

项目使用项目根目录下的：

```text
.venv/
```

M1-T01 中已经验证可以直接通过虚拟环境解释器运行：

```bash
.venv/bin/python -m pytest
.venv/bin/python -m app.main
```

当前目录快照的 Shell 提示符也显示虚拟环境处于激活状态：

```text
(.venv)
```

激活命令：

```bash
.venv/bin/activate
```

### 核心依赖

#### 构建系统

```text
setuptools
```

构建后端：

```text
setuptools.build_meta
```

#### 运行时依赖

当前：

```toml
dependencies = []
```

即尚未声明第三方运行时依赖。

#### 开发依赖

当前开发依赖：

```text
pytest >= 8, < 10
```

#### 可编辑安装

M1-T01 已完成项目的可编辑安装配置。

具体安装命令未在本次材料中记录，因此本总结不额外补充未经验证的命令。

## 测试状态

### 当前测试总览

当前项目全量测试：

```text
总测试数：13
通过：13
失败：0
通过率：100%
```

组成：

```text
tests/test_smoke.py            2
tests/test_project_state.py   11
-------------------------------
总计                          13
```

### 测试命令

全量回归：

```bash
pytest
```

M1-T02 专项测试：

```bash
pytest tests/test_project_state.py
```

M1-T01 中也验证过使用项目虚拟环境直接执行：

```bash
.venv/bin/python -m pytest
```

### 当前测试覆盖场景

#### 冒烟测试

主要验证最基础的工程可运行性：

* 应用名称；
* 应用版本常量。

#### Project 状态专项测试

主要覆盖：

* 多变量引用同一个 Project；
* 原地修改；
* 返回新 Project；
* 不同 Project 默认列表隔离；
* `dict.copy()` 浅拷贝嵌套对象共享；
* Project 克隆；
* `create_project()` 返回 Project 类型；
* 外部输入 tags 与 Project 内部状态隔离；
* `description` 默认值；
* `description` 显式赋值；
* `with_tag()` 创建新对象时保持 `description`；
* 应用名称和版本冒烟测试。

当前测试还验证了一个重要工程原则：

> 测试全部通过并不自动等于业务逻辑正确。

除了关注测试是否绿色，还需要检查测试断言质量以及预期测试是否真的被 pytest 收集。

## 核心设计决策与已知问题

### Project 已从裸 dict 演进为 dataclass

M1-T02 中：

```python
{
    "name": name,
    "tags": [],
    "members": [],
}
```

属于刻意保留的学习型数据结构。

M1-T03 后，当前正式结构为：

```python
@dataclass
class Project:
    name: str
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
```

因此旧总结中：

```text
Project 当前使用裸 dict
```

已经失效，不应继续描述为当前事实。

### 类型注解暂不承担运行时校验

当前：

```python
name: str
description: str | None
```

主要负责：

* 表达代码意图；
* 提高可读性；
* 为 IDE 和静态检查提供类型信息。

当前阶段不提前引入 Pydantic 或其他复杂运行时校验体系。

### 可变字段使用 default_factory

`tags` 和 `members` 使用：

```python
field(default_factory=list)
```

保证每个 Project 实例拥有独立列表。

### 外部可变对象默认采取隔离策略

`create_project()` 接收外部 `tags` / `members` 后建立新的 list，而不是默认共享同一引用。

当前原则：

```text
是否共享可变状态必须是明确设计决定，
不能由无意的对象引用决定。
```

### 新字段必须审计全部对象重建路径

M1-T03 已出现一次真实回归：

```text
新增 description
→ with_tag() 忘记复制
→ 新对象 description 丢失
```

因此后续每次数据模型新增或删除字段，都应检查：

```text
构造函数
clone/copy
返回新对象函数
持久化
序列化
测试
```

随着项目进入数据库和 API 阶段，该检查范围还会继续扩大。

## 下一步计划

下一个待执行任务：

### M1-T04｜类、组合与模块职责

下一任务重点：

* 类和对象职责；
* 数据与行为的边界；
* 组合；
* 模块职责；
* Model / Service / Storage 的最小职责认知；
* 判断“代码应该放在哪里”。

M1-T04 将基于当前 `Project` dataclass 继续演进。

不会提前进入：

```text
FastAPI
数据库
ORM
复杂设计模式
```

重点从：

```text
数据长什么样
```

逐步推进到：

```text
谁负责什么
```

## 使用指南（给后续 AI 助手）

本文档用于提供 **AI Workspace Lite 当前开发和学习状态的集中快照**。

后续 AI 助手接手项目时，应首先阅读本文档，以快速确认：

* 项目当前处于哪个里程碑；
* 哪些任务已经完成；
* 当前 Project 数据结构是什么；
* 已经实现了哪些模块；
* 当前测试基线是多少；
* 哪些设计是暂时性的；
* 已知技术债有哪些；
* 下一张任务卡是什么。

本文档的作用不是替代任务卡片，而是将多个任务卡片中的关键信息汇总成项目级上下文，方便后续协助规划学习、Code Review 和下一步开发。

### 后续增量维护规则

每完成新的 `Mx-Txx` 任务后，应基于新任务卡片增量更新本文档，而不是重新猜测项目状态。

至少需要更新以下内容：

1. **项目概览**

   * 将新完成的任务加入“当前已完成卡片”。

2. **已完成任务详情**

   * 增加对应 `Mx-Txx` 小节；
   * 记录完成日期；
   * 记录文件变更；
   * 记录核心知识点；
   * 记录测试结果；
   * 记录遗留问题。

3. **项目结构与文件职责**

   * 如果新增、删除或重命名文件，同步更新目录树和职责说明。

4. **环境与依赖**

   * 如果 `pyproject.toml` 或运行环境发生变化，同步更新 Python 版本和依赖信息。

5. **测试状态**

   * 使用最新全量 `pytest` 结果更新总测试数、通过率及覆盖场景。

6. **核心设计决策与已知问题**

   * 已解决的问题应更新或移除；
   * 新发现的技术债应追加；
   * 不应把已经失效的临时设计继续描述为当前事实。

7. **下一步计划**

   * 始终指向当前最新完成任务之后的下一张任务卡。

后续维护应优先以以下资料作为事实来源：

```text
最新任务卡片
→ 当前代码和目录结构
→ pyproject.toml
→ pytest 全量测试结果
→ Git / Code Review 结果
→ 本总结中的既有上下文
```

如果新任务卡片与旧总结发生冲突，应以**当前代码、最新任务记录和最新验证结果**为准，并同步修正文档，避免继续传播已经过期的项目状态。
