# Monitoring Access Control

Система управления доступом и мониторингом  
Это внутренняя система для контроля и мониторинга доступа пользователей, с разграничением ролей и безопасностью.

## Технологии

- **Backend**: Python, FastAPI, MySQL
- **Frontend**: React, TypeScript, Tailwind CSS

# Структура проекта
```
auth-system/
├── backend/           # FastAPI приложение
├── frontend/          # React интерфейс
├── alembic.ini        # конфиг миграций (НЕ коммитить!)
└── .env               # переменные окружения (НЕ коммитить!)
```

## 1. Клонирование и настройка

```bash
git clone <URL-репозитория>
cd monitoring_access_control
Создать виртуальное окружение
python -m venv .venv
```

# Windows
.venv\Scripts\Activate

# Linux/Mac
source .venv/bin/activate

Установить зависимости
```bash
pip install -r requirements.txt
Шаблоны конфигурации
.env.example → .env
```


Отредактируйте файлы с вашими данными:
alembic.example.ini → alembic.ini
.env – настройки приложения:

env
Копировать код
DATABASE_URL=mysql+pymysql://ваш_username:ваш_пароль@localhost:3306/monitoring_access_db
SECRET_KEY=ваш_длинный_секретный_ключ_не_менее_32_символов
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
alembic.ini – миграции базы данных:

ini
sqlalchemy.url = mysql+pymysql://ваш_username:ваш_пароль@localhost:3306/monitoring_access_db


2. Настройка базы данных
Применяем миграции:
alembic upgrade head


3. Запуск приложения
Backend
```bash
Копировать код
cd backend
uvicorn app.main:app --reload
```

Доступ к приложению:
Главная: http://localhost:8000
Документация API (Swagger): http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

4. Безопасность конфигурации
Файлы, которые НИКОГДА нельзя коммитить:
.env – содержит пароли БД и секретные ключи
alembic.ini – содержит строку подключения к БД

5. Управление базой данных
Создать новую миграцию:
```
alembic revision --autogenerate -m "Описание изменений"
Применить миграции:

alembic upgrade head
Проверить текущую миграцию:
alembic current
```

История миграций: alembic history

Важное примечание о безопасности
Проект использует переменные окружения для конфиденциальных данных.
НЕ КОММИТЬ файлы с паролями или секретными ключами.


## Быстрый старт
```
# Клонирование
git clone <URL-репозитория>
cd auth-system

# Настройка окружения
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или .venv\Scripts\activate  # Windows

# Зависимости
pip install -r requirements.txt

# Настройка конфигов (скопировать и заполнить)
cp .env.example .env
cp alembic.example.ini alembic.ini

# Миграции БД
alembic upgrade head
```

# Что реализовано
Регистрация и вход пользователей
JWT аутентификация (access + refresh токены)
Миграции базы данных через Alembic
Документированное API (Swagger/ReDoc)
Базовый фронтенд на React

# Безопасность
Важно: Файлы .env и alembic.ini с чувствительными данными никогда не должны попадать в репозиторий. Используйте .env.example и alembic.example.ini как шаблоны.
