'''
@Project ：beerbot
@File    ：main.py
@IDE     ：vscode
@Author  ：cjxpj
@Date    ：2025-1-23 20:47:34
'''
import ast
import sqlite3
import os
from typing import List, Optional


class Database:
    def __init__(
        self, conn: sqlite3.Connection, cursor: sqlite3.Cursor, table_name: str
    ):
        """初始化数据"""
        self.conn = conn
        self.cursor = cursor
        self.table_name = table_name

    def 增加(self, key: str, value: int) -> None:
        """增加键值"""
        try:
            self.cursor.execute(
                f"""
                INSERT INTO `{self.table_name}` (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=value+excluded.value
                """,
                (key, value),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during increment operation: {e}")
            self.conn.rollback()

    def 减少(self, key: str, value: int) -> None:
        """减少键值"""
        try:
            self.cursor.execute(
                f"""
                INSERT INTO `{self.table_name}` (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=value-excluded.value
                """,
                (key, value),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during decrement operation: {e}")
            self.conn.rollback()

    def 自增(self, key: str, value: int = 1) -> None:
        """自增键值"""
        try:
            self.cursor.execute(
                f"""
                UPDATE `{self.table_name}` SET value=value+? WHERE key=?
                """,
                (value, key),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during increment operation: {e}")
            self.conn.rollback()

    def 自减(self, key: str, value: int = 1) -> None:
        """自减键值"""
        try:
            self.cursor.execute(
                f"""
                UPDATE `{self.table_name}` SET value=value-? WHERE key=?
                """,
                (value, key),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during decrement operation: {e}")
            self.conn.rollback()

    def 重命名(self, key: str, new_key: str) -> None:
        """重命名键"""
        try:
            self.cursor.execute(
                f"""
                UPDATE `{self.table_name}` SET key=? WHERE key=?
                """,
                (new_key, key),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during rename operation: {e}")
            self.conn.rollback()

    def 写(self, key: str, value) -> None:
        """插入或更新键值"""
        if type(value) == list:
            value = str(value)
        elif type(value) == dict:
            value = str(value)
        elif type(value) == bool:
            value = str(value)
        try:
            self.cursor.execute(
                f"""
                INSERT INTO `{self.table_name}` (key, value)
                VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value
                """,
                (key, value),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during set operation: {e}")
            self.conn.rollback()

    def 写多个(self, data: dict):
        """批量插入或更新键值
        set_all({
            'key1': 'value',
            'key2': 1,
            'key3': [],
            'key4': None
            'key5': True
            'key6': {}
        })
        """
        for key, value in data.items():
            self.set(key, value)

    def 获取全部(self) -> dict:
        """获取全部键值"""
        try:
            self.cursor.execute(f"SELECT * FROM `{self.table_name}`")
            result = self.cursor.fetchall()
            return {row[0]: row[1] for row in result}
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get_all operation: {e}")
            return {}

    def 获取全部INT(self) -> dict:
        """获取全部键INT值"""
        try:
            self.cursor.execute(f"SELECT * FROM `{self.table_name}`")
            result = self.cursor.fetchall()
            return {row[0]: int(row[1]) for row in result}
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get_all operation: {e}")
            return {}

    def 读全部_values(self) -> list:
        """获取全部值"""
        try:
            self.cursor.execute(f"SELECT value FROM `{self.table_name}`")
            result = self.cursor.fetchall()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get_all_values operation: {e}")
            return []

    def 读全部_keys(self) -> list:
        """获取全部键"""
        try:
            self.cursor.execute(f"SELECT key FROM `{self.table_name}`")
            result = self.cursor.fetchall()
            return [row[0] for row in result]
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get_all_keys operation: {e}")
            return []

    def 读(self, key: str, res: Optional[str] = None) -> Optional[str]:
        """获取键对应的值"""
        try:
            self.cursor.execute(
                f"""
                SELECT value FROM `{self.table_name}` WHERE key=?
                """,
                (key,),
            )
            result = self.cursor.fetchone()
            return result[0] if result else res
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get operation: {e}")
            return res

    def 读INT(self, key: str, res: Optional[int] = None) -> Optional[int]:
        """获取键对应的值"""
        try:
            self.cursor.execute(
                f"""
                SELECT value FROM `{self.table_name}` WHERE key=?
                """,
                (key,),
            )
            result = self.cursor.fetchone()
            return int(result[0]) if result else res
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get operation: {e}")
            return res

    def 读List(self, key: str) -> list:
        """获取键对应的值"""
        try:
            self.cursor.execute(
                f"""
                SELECT value FROM `{self.table_name}` WHERE key=?
                """,
                (key,),
            )
            result = self.cursor.fetchone()
            return ast.literal_eval(result[0]) if result else []
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get operation: {e}")
            return []

    def 读Dict(self, key: str) -> dict:
        """获取键对应的值"""
        try:
            self.cursor.execute(
                f"""
                SELECT value FROM `{self.table_name}` WHERE key=?
                """,
                (key,),
            )
            result = self.cursor.fetchone()
            return ast.literal_eval(result[0]) if result else {}
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get operation: {e}")
            return {}

    def 读_val_key(self, value: str, res: Optional[str] = None) -> Optional[str]:
        """获取值对应的键"""
        try:
            self.cursor.execute(
                f"""
                SELECT key FROM `{self.table_name}` WHERE value=?
                """,
                (value,),
            )
            result = self.cursor.fetchone()
            return result[0] if result else res
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get operation: {e}")
            return res

    def delete(self, key: str) -> None:
        """删除指定键"""
        try:
            self.cursor.execute(
                f"""
                DELETE FROM `{self.table_name}` WHERE key = ?
                """,
                (key,),
            )
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during delete operation: {e}")
            self.conn.rollback()


class 打开文件:
    def __init__(self, db_name: str, table_name: str = ""):
        """初始化数据库连接"""
        db_name += ".db"
        os.makedirs(os.path.dirname(db_name), exist_ok=True)  # 自动创建文件夹

        self.path = os.path.abspath(db_name)
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.table_name = table_name
        self._create_table()

    def _create_table(self) -> None:
        """创建表"""
        if self.table_name:
            try:
                self.cursor.execute(
                    f"""
                    CREATE TABLE IF NOT EXISTS `{self.table_name}` (
                        key TEXT PRIMARY KEY,
                        value TEXT
                    )
                    """
                )
                self.conn.commit()
            except sqlite3.Error as e:
                print(f"[ERROR] Error during table creation: {e}")
                self.conn.rollback()

    def get_all_tables(self) -> List[str]:
        """获取所有表名"""
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"[ERROR] Error during get tables operation: {e}")
            return []

    def 重命名表(self, old_name: str, new_name: str) -> None:
        """重命名表"""
        try:
            self.cursor.execute(f"ALTER TABLE `{old_name}` RENAME TO `{new_name}`;")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Error during table renaming: {e}")
            self.conn.rollback()

    def 读库(self, table_name: str = ":memory:") -> Database:
        """设置表名并返回 Database 对象"""
        self.table_name = table_name
        self._create_table()
        return Database(self.conn, self.cursor, self.table_name)

    def 重置(self):
        """删除数据库文件"""
        try:
            self.conn.close()
            os.remove(self.path)
            return 打开文件(self.path, self.table_name)
        except sqlite3.Error as e:
            print(f"[ERROR] Error during database deletion: {e}")
        except FileNotFoundError:
            print("[ERROR] Database file not found.")

    def 关闭(self) -> None:
        """关闭数据库连接"""
        try:
            self.conn.close()
        except sqlite3.Error as e:
            print(f"[ERROR] Error closing connection: {e}")
