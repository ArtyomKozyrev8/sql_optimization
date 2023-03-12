import asyncio
import sys
import random
import time
import datetime

from create_db_ops import InitTables
from insert_ops import (
    create_client,
    create_client_address,
    create_client_contact,
    create_client_passport,
    create_client_wallet,
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

                print("A")
                x = await create_client(curs, "11", "22")
                print(x)
                await create_client_contact(curs, phone="+7", email="email", client_id=x)
                await create_client_passport(curs, seria="7777", number="123444", client_id=x)
                await create_client_address(curs, address="1-1-1-1-1", client_id=x)
                z = await create_client_wallet(curs, client_id=x, balance=random.randint(1, 100))
                print(z)
    finally:
        pg_pool.close()
        await pg_pool.wait_closed()


if __name__ == '__main__':

    "docker run --name some_db -p 9459:5432 -e ENCODING=UTF8  -e POSTGRES_PASSWORD=some_pswd -e POSTGRES_USER=some_user -e POSTGRES_DB=some_db -d postgres -c max_connections=500"

    if sys.version_info >= (3, 8) and sys.platform.lower().startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(amain())
