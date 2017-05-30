CREATE TABLE IF NOT EXISTS diary (
    "Номер" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Задача" TEXT NOT NULL,
    "Комментарий" TEXT NOT NULL DEFAULT '',
    "Статус" TEXT DEFAULT 'Не выполнено',
    "ДатаСоздания" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
)
