# Support Dashboard

Система поддержки клиентов
Это внутренняя система для обработки обращений клиентов. Как те самые чаты поддержки, где операторы отвечают на вопросы.

## Технологии

- **Backend**: Python, FastAPI, MySQL
- **Frontend**: React, TypeScript, Tailwind CSS

### 1. Клонирование и настройка

git clone <URL-репозитория>
cd support-dashboard

# Создать виртуальное окружение

python -m venv .venv
.venv\Scripts\Activate # Windows
source .venv/bin/activate # Linux/Mac

# Установить зависимости

pip install -r requirements.txt

шаблоны конфигурации
.env.example .env
alembic.example.ini

Настройте свои параметры
Отредактируйте скопированные файлы с вашими реальными данными:
.env - Настройки приложения:

env
DATABASE*URL=mysql+pymysql://ваш_username:ваш*пароль@localhost:3306/support*db
SECRET_KEY=ваш*очень*длинный*секретный*ключ*минимум*32*символа
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
alembic.ini - Миграции базы данных:

ini
sqlalchemy.url = mysql+pymysql://ваш*username:ваш*пароль@localhost:3306/support_db

# Настройка базы данных

Применить миграции базы данных
alembic upgrade head

# Запуск приложения

cd backend
uvicorn app.main:app --reload
Доступ к приложению:
Главная: http://localhost:8000
Документация API: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
python -m uvicorn app.main:app --reload

Безопасность конфигурации
Файлы, которые НИКОГДА нельзя коммитить:
.env - Содержит пароли БД и секретные ключи
alembic.ini - Содержит строку подключения к БД

Управление базой данных
Создать новую миграцию:
alembic revision --autogenerate -m "Описание изменений"
Применить миграции:
alembic upgrade head
Проверить текущую миграцию:
alembic current

Решение проблем
Частые проблемы:
"ModuleNotFoundError: No module named 'app'"
Запускайте команды из корня проекта, а не папки backend
Ошибки подключения к БД
Проверьте, что URL БД в .env и alembic.ini совпадают
Убедитесь, что MySQL запущен
Ошибки миграций
Убедитесь, что вы в корне проекта с alembic.ini

Проверьте документацию API: http://localhost:8000/docs
Просмотрите историю миграций: alembic history

При проблемах с настройкой проверьте:
Этот README файл
Документацию API на /docs
Статус миграций с alembic current

## Важное примечание о безопасности

Этот проект использует переменные окружения для безопасности. **НЕ КОММИТЬТЕ** файлы, содержащие пароли или секретные ключи.
