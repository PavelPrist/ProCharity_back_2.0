import sys
from functools import wraps

from src.settings import settings

TASK_DEADLINE_FORMAT = "%d.%m.%y"


def display_tasks(task):
    deadline = task.deadline.strftime(TASK_DEADLINE_FORMAT)
    bonus_link = "https://help.procharity.ru/article/10053"
    return (
        f"От фонда: {task.name_organization}\n\n"
        f"Категория: {task.category.name}\n\n"
        f"Срок: {deadline}\n"
        f"Бонусы: <a href='{bonus_link}'>{task.bonus * '💎'}</a>\n"
        f"<a href='{task.link}'>{'Посмотреть задание'}</a>"
    )


def display_task_verbosely(task):
    deadline = task.deadline.strftime(TASK_DEADLINE_FORMAT)
    bonus_link = "https://help.procharity.ru/article/10053"
    return (
        f"От фонда: {task.name_organization}\n\n"
        f"Категория: {task.category.name}\n\n"
        f"Срок: {deadline}\n"
        f"Бонусы: {task.bonus * '💎'}{bonus_link}\n"
        f"{task.description}"
    )


def auto_commit(func):
    @wraps(func)
    async def auto_commit_wraps(self, *args, commit=True):
        result = await func(self, *args)
        if commit:
            await self._session.commit()
        return result

    return auto_commit_wraps


def set_ngrok():
    from pyngrok import ngrok

    port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 8000
    settings.APPLICATION_URL = ngrok.connect(port).public_url
