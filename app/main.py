# 新增：/project/app/main.py

from app import APP_NAME
from app.info import APP_VERSION



def main() -> None:
    print(f"{APP_NAME} started. {APP_VERSION}")


if __name__ == "__main__":
    main()
