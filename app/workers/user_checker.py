import asyncio
from tqdm import tqdm

from app.db.database import create_table_async, save_data_collection
from app.users.user_collector import get_users_by_id

USERS_COUNT_IN_REQUEST = 100
REQUESTS_PER_SECOND = 3

async def process_checking(min_id, max_id):
    try:
        await create_table_async()
        chunk_size = REQUESTS_PER_SECOND * USERS_COUNT_IN_REQUEST

        # num_chunks = (max_id + chunk_size - 1) // chunk_size
        #
        # chunks_parsed = min_id // chunk_size
        #
        prev_id = min_id
        for cur_id in tqdm(range(min_id+prev_id, max_id, chunk_size), desc="Processing chunks (1500 ids)", unit="chunk"):
            start_index = prev_id
            end_index = cur_id
            prev_id = cur_id
            user_ids = list(range(start_index, end_index))
            batches = [user_ids[i:i + USERS_COUNT_IN_REQUEST] for i in range(0, len(user_ids), USERS_COUNT_IN_REQUEST)]
            chunk_tasks = [get_users_by_id(batch) for batch in batches]
            await process_chunk(chunk_tasks)
            await asyncio.sleep(1)
    except Exception as e:
        print(e)
        await asyncio.sleep(5)
        pass

async def process_chunk(chunk_tasks):
    results = await asyncio.gather(*chunk_tasks)
    all_data = []
    for result in results:
        all_data.extend(result)
    await save_data_collection(all_data)