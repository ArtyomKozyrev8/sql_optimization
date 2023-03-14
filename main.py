import asyncio
import sys
import random
import time
import datetime

from create_db_ops import InitTables
from populate_db_ops import (
    create_client_and_related_data,
    create_client_types,
)


import aiopg


def random_date(seed):
    random.seed(seed)
    d = random.randint(1, int(time.time()))
    return datetime.fromtimestamp(d).strftime('%Y-%m-%d')


async def amain():
    DBNAME = "some_db"
    DBUSER = "some_user"
    DBPSWD = "some_pswd"
    DBHOST = "127.0.0.1"
    DBPORT = 9459

    dbdsn = (
        f"dbname={DBNAME} "
        f"user={DBUSER} "
        f"password={DBPSWD} "
        f"host={DBHOST} "
        f"port={DBPORT}"
    )

    pg_pool = await aiopg.create_pool(dsn=dbdsn)

    try:
        async with pg_pool.acquire() as conn:
            async with conn.cursor() as curs:
                await InitTables(curs).create_db_tables()
                await create_client_types(curs=curs)
                await create_client_and_related_data(curs=curs, client_type=1)
                await create_client_and_related_data(curs=curs, client_type=1)
                await create_client_and_related_data(curs=curs, client_type=4)
                await create_client_and_related_data(curs=curs, wallets_number=3, client_type=2)
                await create_client_and_related_data(curs=curs, wallets_number=2, client_type=3)
                await create_client_and_related_data(curs=curs, wallets_number=0, client_type=1)
                await create_client_and_related_data(curs=curs, wallets_number=0, client_type=1)
    finally:
        pg_pool.close()
        await pg_pool.wait_closed()


if __name__ == '__main__':

    "docker run --name some_db -p 9459:5432 -e ENCODING=UTF8  -e POSTGRES_PASSWORD=some_pswd -e POSTGRES_USER=some_user -e POSTGRES_DB=some_db -d postgres -c max_connections=500"

    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(amain())
