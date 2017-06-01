CREATE TABLE IF NOT EXISTS diary (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "task" TEXT NOT NULL,
    "text" TEXT NOT NULL,
    "deadline" DATETIME NOT NULL,
    "status" TEXT DEFAULT 'Не выполнено'
)
