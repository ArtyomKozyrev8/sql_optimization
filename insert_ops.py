from aiopg import Cursor

from typing import Optional


async def create_client_type(
    curs: Cursor,
    client_type: int,
) -> None:
    query = "INSERT INTO client_type(client_type) VALUES (%(client_type)s) ON CONFLICT DO NOTHING;"

    await curs.execute(query, {"client_type": client_type})


async def create_client(
    curs: Cursor,
    fio: str,
    birthdate: str,
    client_type: int,
) -> str:
    query = (
        "INSERT INTO client(fio, birthdate, client_type)"
        " VALUES (%(fio)s, %(birthdate)s, %(client_type)s)"
        " RETURNING client_id;"
    )

    await curs.execute(query, {"fio": fio, "birthdate": birthdate, "client_type": client_type})

    client_id = (await curs.fetchall())[0][0]

    return str(client_id)


async def create_client_contact(
    curs: Cursor,
    client_id: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
) -> None:
    query = "INSERT INTO client_contact(phone, email, client_id) VALUES (%(phone)s, %(email)s, %(client_id)s);"

    await curs.execute(query, {"phone": phone, "email": email, "client_id": client_id})


async def create_client_passport(
    curs: Cursor,
    client_id: str,
    seria: str = None,
    number: str = None,
) -> None:
    query = "INSERT INTO client_passport(seria, number, client_id) VALUES (%(seria)s, %(number)s, %(client_id)s);"

    await curs.execute(query, {"seria": seria, "number": number, "client_id": client_id})


async def create_client_address(
    curs: Cursor,
    client_id: str,
    address: str = None,
) -> None:
    query = "INSERT INTO client_address(address, client_id) VALUES (%(address)s, %(client_id)s);"

    await curs.execute(query, {"address": address, "client_id": client_id})


async def create_client_wallet(
    curs: Cursor,
    client_id: str,
    balance: float = 0.0,
) -> None:
    query = "INSERT INTO client_wallet(balance, client_id) VALUES (%(balance)s, %(client_id)s) RETURNING wallet_id;"

    await curs.execute(query, {"balance": balance, "client_id": client_id})

    wallet_id = (await curs.fetchall())[0][0]

    return str(wallet_id)
