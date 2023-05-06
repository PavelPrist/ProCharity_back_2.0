import asyncio
import string

from datetime import datetime, timedelta
from random import randint, choice, random, choices
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)

from src.core.db.models import Category, Task
from src.core.db import get_session


CHARACTERS = string.ascii_uppercase + string.digits

CATEGORIES_TEST_DATA = [
    {"id": "1", "name": "Дизайн и верстка"},
    {"id": "2", "name": "Маркетинг и коммуникации"},
    {"id": "3", "name": "Переводы"},
    {"id": "4", "name": "IT"},
    {"id": "5", "name": "Юридические услуги"},
    {"id": "6", "name": "Стратегический консалтинг"},
    {"id": "7", "name": "Фото и видео"},
    {"id": "8", "name": "Обучение и тренинги"},
    {"id": "9", "name": "Финансы и фандрайзинг"},
    {"id": "10", "name": "Менеджмент"}
    ]
TEST_LOCATION = [
    "Москва",
    "Санкт-Петербург",
    "Новосибирск",
    "Екатеринбург",
    "Казань",
    "Нижний Новгород",
    "Челябинск",
    "Самара",
    "Омск",
    "Ростов-на-Дону"
]
TEST_ORGANIZATION = [
    "Нефть без границ",
    "Транспортный гигант-2",
    "Российские роботы",
    "Строй Инновация",
    "Медицинский Колос"
]
TEST_TASKS = [
    {"id": "1", "tasks": [
        "Создание макета сайта в графическом редакторе",
        "Изучение основных принципов дизайна: цвет, типографика, композиция",
        "Создание векторной графики для использования на сайте",
        "Создание нескольких вариантов дизайна для выбора наилучшего решения",
        "Разработка дизайна логотипа и фирменного стиля"
    ]},
    {"id": "2", "tasks": [
        "Разработка и продвижение программы лояльности для доноров.",
        "Организация и проведение благотворительного аукциона или лотереи.",
        "Проведение промо-акций в социальных сетях для привлечения доноров.",
        "Организация и проведение благотворительного мероприятия.",
        "Создание PR-кампаний и пресс-релизов."
    ]},
    {"id": "3", "tasks": [
        "Перевод средств на поддержку нуждающихся",
        "Организация благотворительных мероприятий через переводы",
        "Регулярные переводы на улучшение условий жизни нуждающихся",
        "Перевод на медицинскую помощь нуждающимся",
        "Помощь с переводом для мигрантов и беженцев",
    ]},
    {"id": "4", "tasks": [
        "Разработка и поддержка сайта организации",
        "Создание базы данных для учета доноров и получателей помощи",
        "Разработка мобильного приложения для сбора пожертвований",
        "Автоматизация процесса учета и отчетности в организации",
        "Разработка системы онлайн-консультаций для получателей помощи"
    ]},
    {"id": "5", "tasks": [
        "Регистрация благотворительной организации",
        "Разработка устава и другой внутренней документации",
        "Получение статуса НКО",
        "Консультации по налогообложению и отчетности",
        "Правовая поддержка при взаимодействии с государственными органами"
    ]},
    {"id": "6", "tasks": [
        "Определение и разработка концепции долгосрочного развития организации.",
        "Поиск и обеспечение новых источников финансирования.",
        "Разработка стратегии маркетинга и продвижения организации.",
        "Оптимизация деятельности и уменьшение издержек организации.",
        "Оценка эффективности программ благотворительной помощи.",
    ]},
    {"id": "7", "tasks": [
        "Создание промо-видео",
        "Фотоотчет",
        "Создание видеоинструкций",
        "Фотографирование пациентов",
        "Создание коротких видеороликов",
    ]},
    {"id": "8", "tasks": [
        "Развитие навыков лидерства и командной работы",
        "Навыки эффективной коммуникации и делового переговоров",
        "Финансовое планирование и управление бюджетом",
        "Управление проектами и достижение целей организации",
        "Развитие личной эффективности и эмоционального интеллекта"
    ]},
    {"id": "9", "tasks": [
        "Разработка стратегии привлечения доноров на следующий квартал.",
        "Проведение анализа эффективности рекламных кампаний.",
        "Организация благотворительного концерта с участием артистов.",
        "Проведение финансовой аудитории для улучшения финансовой дисциплины.",
        "Разработка системы мотивации для волонтеров."
     ]},
    {"id": "10", "tasks": [
        "Разработать стратегию привлечения новых доноров",
        "Организация гала-вечеринки в поддержку благотворительной программы",
        "Подготовка презентации о деятельности организации.",
        "Провести опрос среди населения для выявления актуальных проблем.",
        "Разработать план волонтерской деятельности для привлечения помощи."
    ]}
]


async def get_task_name_by_id(category_id):
    """Function for selecting tasks from the TEST_TASKS list."""
    for task in TEST_TASKS:
        if int(task["id"]) == category_id:
            for i in task["tasks"]:
                yield i


async def filling_category_in_db(
        session: async_sessionmaker[AsyncSession],
        ) -> None:
    """Filling the database with test data Categories.
    The fields id, name, archive are filled in.
    """
    for category in CATEGORIES_TEST_DATA:
        category_obj = Category(
            name=category['name'],
            archive=choice([True, False]),
            id=int(category['id']),
        )
        session.add(category_obj)
    await session.commit()


async def filling_task_in_db(
        session: async_sessionmaker[AsyncSession],
        ) -> None:
    """Filling the database with test data: Tasks.
    The fields title, name_organization, deadline, category,
    location, description, archive.
     """
    for category_id in range(1, len(CATEGORIES_TEST_DATA) + 1):
        async for title in get_task_name_by_id(category_id):
            task = Task(
                name_organization=f'{choice(TEST_ORGANIZATION)}',
                deadline=datetime.now() + timedelta(days=10),
                category_id=category_id,
                title=title,
                bonus=randint(100, 1000),
                location=f'{choice(TEST_LOCATION)}',
                link=f"http://example.com/task/"
                f"{''.join(choices(CHARACTERS, k=6))}",
                description=f"Description {title}",
                archive=choice([True, False])
            )
            session.add(task)
        await session.commit()


async def delete_all_data(session: async_sessionmaker[AsyncSession],) -> None:
    """The function deletes data from the tables Category, Tasks."""
    await session.execute(
        text("""TRUNCATE TABLE tasks, categories CASCADE""")
    )
    await session.commit()


async def run():
    sessions = get_session()
    async with sessions as session:
        await delete_all_data(session)
        print("Deleted data from the Tasks, Categories table.")
        await filling_category_in_db(session)
        print("The table with the Categories is full.")
        await filling_task_in_db(session)
        print("The Tasks table is full.")

if __name__ == "__main__":
    asyncio.run(run())
