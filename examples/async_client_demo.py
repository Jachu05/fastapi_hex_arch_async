"""examples/async_client_demo.py
Demonstration of asynchronous interaction with the running FastAPI application.

Prerequisites:
1. Start the FastAPI app first (e.g. ``uvicorn app.main:app --reload``)
2. Then run this script: ``python examples/async_client_demo.py``

The script concurrently creates several tasks via the ``POST /tasks/`` endpoint and
finally retrieves all tasks via ``GET /tasks/`` to show the results.
"""

import asyncio
from typing import List

import httpx

BASE_URL = "http://localhost:8000"  # Adjust if your Uvicorn host/port differs


async def create_task(description: str, client: httpx.AsyncClient) -> dict:
    """Create a single task on the API and return the JSON response."""
    response = await client.post(f"{BASE_URL}/tasks/", json={"description": description})
    response.raise_for_status()
    return response.json()


async def list_tasks(client: httpx.AsyncClient) -> List[dict]:
    """Retrieve all tasks from the API."""
    response = await client.get(f"{BASE_URL}/tasks/")
    response.raise_for_status()
    return response.json()


async def delete_task(task_id: int, client: httpx.AsyncClient) -> None:
    """Delete a task from the API."""
    response = await client.delete(f"{BASE_URL}/tasks/{task_id}")
    response.raise_for_status()


async def main() -> None:
    descriptions = [f"Async task {i}" for i in range(1, 6)]

    # Re-use a single HTTP client for connection pooling efficiency
    async with httpx.AsyncClient(timeout=10.0) as client:
        # 1. Launch creation requests concurrently
        print("Launching create requests concurrently…")
        create_coros = [create_task(desc, client) for desc in descriptions]
        created_tasks = await asyncio.gather(*create_coros)

        print("\nAll tasks created!\n")
        for t in created_tasks:
            print(f" - {t['id']}: {t['description']}")

        # 2. List tasks after creation (server-side)
        print("\nListing tasks from server…\n")
        tasks = await list_tasks(client)
        for t in tasks:
            print(f" - {t['id']}: {t['description']}")

        # 3. Delete tasks concurrently
        print("\nDeleting tasks concurrently…\n")
        delete_coros = [delete_task(t["id"], client) for t in created_tasks]
        await asyncio.gather(*delete_coros)

        # 4. Verify deletion
        remaining = await list_tasks(client)
        if not remaining:
            print("\nAll tasks deleted — no tasks remaining.")
        else:
            print("\nTasks remaining after deletion:")
            for t in remaining:
                print(f" - {t['id']}: {t['description']}")


if __name__ == "__main__":
    asyncio.run(main()) 