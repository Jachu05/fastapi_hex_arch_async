import asyncio
from typing import List

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from app.usecases.task_service import TaskService
from app.api.dependencies import get_task_service
from app.api.requests import TaskCreateRequest, TaskResponse

router = APIRouter()

# Logger for this module
logger = logging.getLogger(__name__)


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    payload: TaskCreateRequest,
    service: TaskService = Depends(get_task_service),
):
    logger.info("Creating task: %s", payload.description)

    # Simulate a *tiny* IO wait just to showcase that the endpoint remains
    # responsive (remove or adjust in real projects).
    await asyncio.sleep(0.5)
    task = await service.create_task(payload.description)

    logger.info("Task created: %s", task.id)

    return TaskResponse(id=task.id, description=task.description)


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(service: TaskService = Depends(get_task_service)):
    tasks = await service.list_tasks()
    return [TaskResponse(id=t.id, description=t.description) for t in tasks]


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        task = await service.get_task(task_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return TaskResponse(id=task.id, description=task.description)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    try:
        await service.delete_task(task_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found") 