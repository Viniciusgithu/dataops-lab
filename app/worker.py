from __future__ import annotations

import asyncio
import concurrent.futures
from temporalio.client import Client
from temporalio.worker import Worker

from app.activities import (
    aggregate_orders_activity,
    generate_csv_activity,
    load_csv_to_mongodb_activity,
)
from app.workflows import OrdersPipelineWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    worker = Worker(
        client,
        task_queue="orders-task-queue",
        workflows=[OrdersPipelineWorkflow],
        activities=[
            generate_csv_activity,
            load_csv_to_mongodb_activity,
            aggregate_orders_activity,
        ],
        activity_executor=concurrent.futures.ThreadPoolExecutor(),
    )

    print("Worker started. Waiting for workflows...")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())