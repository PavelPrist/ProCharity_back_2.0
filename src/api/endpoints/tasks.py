from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.api.schemas import TaskRequest, TaskResponse
from src.api.services import TaskService
from src.api.services.messages import TelegramNotificationService
from src.core.db.models import Task
from src.core.utils import display_tasks
from src.depends import Container

task_router = APIRouter()


@task_router.post("/", description="Актуализирует список задач.")
@inject
async def actualize_tasks(
    tasks: list[TaskRequest],
    task_service: TaskService = Depends(Provide[Container.task_service]),
    telegram_notification_service: TelegramNotificationService = Depends(Provide[Container.message_service]),
) -> None:
    new_tasks_ids = await task_service.actualize_objects(tasks, Task)
    new_category_tasks = await task_service.get_user_tasks_ids(new_tasks_ids)
    for task in new_category_tasks:
        message = display_tasks(task)
        await telegram_notification_service.send_messages_to_subscribed_users(message, task.category_id)


@task_router.get(
    "/{user_id}",
    response_model=list[TaskResponse],
    response_model_exclude_none=True,
    description="Получает список всех задач из категорий на которые подписан юзер.",
)
@inject
async def get_tasks_for_user(
    user_id: int, task_service: TaskService = Depends(Provide[Container.task_service])
) -> list[TaskResponse]:
    return await task_service.get_tasks_for_user(user_id)


@task_router.get(
    "/",
    response_model=list[TaskResponse],
    response_model_exclude_none=True,
    description="Получает список всех задач.",
)
@inject
async def get_all_tasks(task_service: TaskService = Depends(Provide[Container.task_service])) -> list[TaskResponse]:
    return await task_service.get_all()
