# 新增：/project/tests/test_smoke.py

# 现在这个测试只有一个作用：

# 判断这个刚搭起来的工程有没有完全坏掉。

from app import APP_NAME
from app.info import APP_VERSION



def test_app_name() -> None:
    assert APP_NAME == "AI Workspace Lite"


def test_app_version() -> None:
    assert APP_VERSION == "0.1.0"
