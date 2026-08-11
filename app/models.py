#新增：app/models.py

from dataclasses import dataclass, field

@dataclass
class Project:
    name: str
    description: str | None = None
    tags: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)

# 可变对象作为默认值
# → 多次创建之间可能共享状态

# default_factory=list 表示：
# 每次创建新实例时，调用 list() 生成一个全新空列表