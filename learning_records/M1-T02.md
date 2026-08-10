# M1-T02｜Python 对象引用与可变对象

状态：已完成

完成日期：2026-08-10

## 完成内容

本任务围绕 Python 中的对象引用、可变对象、浅拷贝、独立复制和函数参数共享对象展开，并将相关概念集成到 AI Workspace Lite 的 Project 数据结构中。

完成内容包括：

* 理解变量名称与对象之间的引用关系。
* 验证 `b = a` 只建立新的对象引用，而不会复制对象。
* 区分 `==` 与 `is`：

  * `==` 比较对象的值。
  * `is` 判断是否为同一个对象。
* 理解 `list`、`dict` 等可变对象被多个变量共享时产生的状态污染问题。
* 理解函数参数绑定到传入对象后，函数内部的原地修改可以影响调用方持有的对象。
* 理解 `dict.copy()` 属于浅拷贝，嵌套可变对象仍可能共享。
* 理解深拷贝能够解决嵌套对象共享问题，同时认识其时间、内存和设计层面的成本。
* 认识 Python 可变默认参数的共享风险，并学习使用 `None` 后在函数内部创建新列表的方式避免共享。
* 区分“明确原地修改”和“返回新对象”两种函数设计。

## 代码变更

### `app/project_state.py`

新增 Project 的基础数据行为。

`create_project(name)`：

* 正确保留传入的项目名称。
* 每次调用独立创建 `tags` 列表。
* 每次调用独立创建 `members` 列表。

当前结构：

```python
{
    "name": name,
    "tags": [],
    "members": [],
}
```

实现已经保证不同 Project 不会因为默认数据结构而共享 `tags` 或 `members`。

新增 `add_tag_in_place()`：

* 使用 `append()` 修改传入 Project 的 `tags`。
* 明确体现 in-place mutation。
* 调用方与函数参数共享同一个 Project 及其内部 `tags` 对象，因此调用后原 Project 会发生变化。

新增 `with_tag()`：

* 不修改原 Project。
* 创建新的 Project 字典。
* 为返回结果创建新的 `tags` 列表。
* 用于比较“原地修改”和“返回新值”两种数据处理方式。

新增可变默认参数实验：

* `create_project_test1(name, tags=[])` 用于观察可变默认参数可能造成的列表共享问题。
* `create_project_test2(name, tags=None)` 使用 `None` 后在函数内部创建列表，避免不同调用意外共享同一默认列表。

新增 `clone_project()`：

* 返回新的 Project 字典。
* 为当前 Project 数据结构中的 `tags` 创建独立列表。
* 为 `members` 创建独立列表。
* 不直接使用 `deepcopy()`，而是根据当前明确的数据结构手工复制需要隔离的可变字段。

当前选择手工复制是有意的：现阶段 Project 结构简单，可以明确知道哪些字段需要独立；如果未来 `members` 等字段内部继续包含嵌套 `dict/list`，需要重新评估该复制策略。

### `tests/test_project_state.py`

新增 6 个专项测试场景：

1. 验证赋值后两个变量引用同一个 Project。
2. 验证 `add_tag_in_place()` 会修改原 Project。
3. 验证 `with_tag()` 返回新 Project，并且不会修改原 `tags`。
4. 验证两个独立创建的 Project 不共享 `members`。
5. 验证 `dict.copy()` 的浅拷贝仍然共享嵌套 `members`。
6. 验证 `clone_project()` 返回不同 Project，并隔离 `tags` 和 `members`。

专项测试最终成功被 pytest 收集：

```text
collected 6 items

tests/test_project_state.py ...... [100%]

6 passed
```



## 核心知识验收

### 1. 为什么 `b = a` 不是复制？

因为赋值操作不会自动创建一个与 `a` 内容相同的新对象。

执行：

```python
b = a
```

后，`a` 和 `b` 都可以引用同一个对象。

因此对于可变对象，如果通过 `b` 原地修改对象，`a` 再访问时也会观察到同样的变化。

### 2. `==` 与 `is` 有什么区别？

`==`：

```text
比较两个对象的值是否相等
```

`is`：

```text
判断两个变量是否引用同一个对象
```

因此可能出现：

```python
a == b
```

为 `True`，但：

```python
a is b
```

为 `False`。

### 3. 为什么 `dict.copy()` 可能污染原数据？

`dict.copy()` 只建立新的最外层字典。

如果字典内部保存：

```text
list
dict
set
```

等可变对象，新旧字典中的对应字段仍可能引用同一个嵌套对象。

因此修改副本中的嵌套列表，有可能同时改变原字典观察到的数据。

### 4. 为什么函数执行 `add_tag_in_place(project, ...)` 后，函数外 Project 也会变化？

调用函数时并不会自动复制完整 Project。

函数形参 `project` 与调用方变量可以绑定到同一个 Project 对象。

Project 中的 `tags` 又是一个可变列表，而：

```python
project["tags"].append(...)
```

是原地修改该列表。

因此函数执行结束后，调用方仍然引用已经被修改的同一个对象，自然能够看到变化。

### 5. `deepcopy()` 解决什么问题？为什么不能无脑使用？

深拷贝会递归处理嵌套数据，在适用情况下可以避免浅拷贝留下的嵌套对象共享引用问题。

但不应该把 `deepcopy()` 当成所有引用问题的默认答案，因为大型对象的深拷贝可能：

* 消耗额外内存。
* 增加运行时间。
* 复制本来应该共享的对象。
* 掩盖数据结构和函数职责设计问题。

更合理的原则是首先明确：

```text
哪些对象应该共享？
哪些对象必须独立？
这个函数应该修改原对象还是返回新对象？
```

然后选择对应的数据复制方式。

## 数据流总结

### 原地修改

```text
调用者 project
        │
        ▼
同一个 Project dict
        │
        ▼
同一个 tags list
        │
add_tag_in_place()
        │
        ▼
append()
        │
        ▼
原列表发生变化
        │
        ▼
调用者观察到变化
```

### 返回新 Project

```text
original Project
        │
        ▼
with_tag()
        │
        ├── 创建新的 dict
        │
        └── 创建新的 tags list
                 │
                 ▼
           updated Project

original 保持不变
```

### 浅拷贝

```text
original dict ──► members list
                         ▲
                         │
copied dict ─────────────┘
```

最外层字典不同，但嵌套列表仍然可能共享。

### 当前 `clone_project()`

```text
original dict ──► original tags
             └──► original members

cloned dict   ──► cloned tags
             └──► cloned members
```

针对当前 Project 结构，需要隔离的两个可变字段已经显式复制。

## 验证命令及结果

### M1-T02 专项测试

```bash
pytest tests/test_project_state.py
```

结果：

```text
collected 6 items
tests/test_project_state.py ...... [100%]

6 passed
```

### 项目全量回归测试

执行：

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

这证明：

* M1-T02 的 6 个专项测试全部通过。
* M1-T01 原有的 2 个 smoke tests 没有被此次修改破坏。
* 当前项目全量测试回归通过。

### Git 验证

最终状态：

```text
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```



说明 M1-T02 代码已经进入版本控制，并完成当前 Git 工作区收口。

## Code Review 结论

本任务验收通过。

过程中发现并修复了两个具有实际工程意义的问题：

### 问题一：测试通过但业务代码实际错误

初始 `create_project(name)` 没有真正使用传入的 `name`。

同时测试设计恰好没有有效捕获该问题。

这说明：

```text
pytest 绿色
≠
业务逻辑一定正确
```

测试代码本身同样需要 Code Review。

后续测试应优先断言明确的业务预期，而不是只依靠过于宽松的条件。

### 问题二：测试函数未被 pytest 收集

浅拷贝测试最初没有采用 `test_...` 命名，因此虽然代码存在，但 pytest 没有执行。

修正后专项测试由 5 个增加至 6 个并全部通过。

这说明以后看到：

```text
N passed
```

不能只看“passed”，还需要确认：

```text
预期的测试是否真的被 collected
```

## 遗留问题

以下问题不阻塞本任务完成，但后续需要保持关注：

1. `clone_project()` 当前只对已知的 `tags` 和 `members` 做一层独立复制。

   如果以后数据变成：

   ```python
   "members": [
       {
           "name": "Alice",
           "roles": ["admin"],
       }
   ]
   ```

   仅复制 `members` 外层列表已经不足以实现完全隔离。

2. 测试应继续提高断言质量。

   优先检查明确的最终值，而不是仅验证：

   ```text
   != 某个错误值
   ```

3. 学习实验函数如：

   ```text
   create_project_test1
   create_project_test2
   ```

   当前用于理解可变默认参数是合理的；随着项目进入真正业务阶段，不应长期混入生产业务 API。

4. 当前 Project 仍然使用裸 `dict` 表示。

   这是本阶段刻意保留的简单结构，不提前引入复杂模型。下一阶段将开始学习类型注解与正式数据模型。

## 本任务获得的核心能力

完成 M1-T02 后，应能够独立判断：

```text
变量是否只是共享引用
对象是否可变
一次操作是否属于原地修改
浅拷贝是否仍共享嵌套状态
是否真的需要深拷贝
函数是否会修改调用者持有的数据
两个 Project 是否意外共享列表
```

本任务对应 Python 工程基础中的对象引用、可变对象、浅拷贝、深拷贝和参数传递能力，也是后续业务状态管理的重要基础。学习路线明确要求在 Python 第一阶段掌握这些内容。

## 下一步

下一任务：

**M1-T03｜函数、类型注解与数据模型**

下一阶段将在当前 `dict` Project 的基础上继续解决：

* 函数参数与返回值契约。
* 默认参数。
* `None`。
* Python 类型注解。
* 数据模型。
* `dataclass`。
* 如何让 Project 从“随意拼接的字典”逐渐变成结构明确、可以被静态阅读和维护的数据对象。

暂不进入类的复杂职责拆分；类、组合和模块职责将在 M1-T04 单独处理。
