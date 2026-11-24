import sqlite3
from pathlib import Path

from storage import get_conn

source = Path(__file__).resolve().with_name("history.db")
old = sqlite3.connect(source.as_uri() + "?mode=ro", uri=True)
new = get_conn(row_factory=None)
print(f"源文件：{source}")
print(f"目标库：{new.info.host}:{new.info.port}/{new.info.dbname}，用户：{new.info.user}")
if input("确认源文件和目标库无误后输入 yes：").strip() != "yes":
    raise SystemExit("已取消迁移")
cur = new.cursor()

# ① 目标库的 history 表必须为空，防止重跑把数据搬两遍
existing = cur.execute("SELECT count(*) FROM history").fetchone()[0]
if existing > 0:
    raise SystemExit(f"目标库的 history 表已经有 {existing} 条记录，停止迁移")

# ② 读旧库（SQLite）
rows = old.execute(
    "SELECT session_id, text, score, label, pinyin, created_at FROM history"
).fetchall()

# ③ 写新库（PostgreSQL）
for row in rows:
    cur.execute(
        "INSERT INTO history (session_id, text, score, label, pinyin, created_at)"
        " VALUES (%s, %s, %s, %s, %s, %s)",
        row,
    )
new.commit()
old.close()
new.close()

print(f"迁移完成，共 {len(rows)} 条记录")
