import asyncio

import insert_ops as ins
import utils as ut

from aiopg import Cursor

async def create_client_and_related_data(curs: Cursor, wallets_number: int = 1, client_type: int=1) -> None:
    id_ = await ins.create_client(curs, ut.create_fio(), ut.create_birthday(), client_type)
    await ins.create_client_contact(curs, id_, ut.create_phone_number(), ut.create_email())
    await ins.create_client_address(curs, id_, ut.create_address())
    await ins.create_client_passport(curs, id_, ut.create_passport_seria(), ut.create_passport_number())
    for _ in range(wallets_number):
        await ins.create_client_wallet(curs, id_, ut.create_balance())


async def create_client_types(curs: Cursor):
    for type_ in range(1, 5):
        await ins.create_client_type(curs, client_type=type_)
