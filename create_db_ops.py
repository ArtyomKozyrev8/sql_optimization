from aiopg import Cursor


class InitTables:
    def __init__(self, curs: Cursor) -> None:
        self.curs = curs

    async def _create_table_client_type(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client_type(
                id SERIAL PRIMARY KEY,
                client_type INTEGER,
                UNIQUE(client_type)
            );
        """
        await self.curs.execute(q)
        

    async def _create_table_client(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                client_id uuid DEFAULT uuid_generate_v4 () UNIQUE,
                fio VARCHAR(120),
                birthdate VARCHAR(10),
                client_type INTEGER,
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW(),
                CONSTRAINT fk_client_type_client_type_tb
                    FOREIGN KEY(client_type) 
                    REFERENCES client_type(client_type)
                    ON DELETE SET NULL ON UPDATE CASCADE
            );
        """
        await self.curs.execute(q)


    async def _create_table_client_contact(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client_contact(
                id SERIAL PRIMARY KEY,
                client_id uuid UNIQUE,
                phone VARCHAR(20) DEFAULT NULL,
                email VARCHAR(40) DEFAULT NULL,
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW(),
            CONSTRAINT fk_client_id_clients_tb
                FOREIGN KEY(client_id) 
                REFERENCES client(client_id)
                ON DELETE SET NULL ON UPDATE CASCADE
            );
        """
        await self.curs.execute(q)


    async def _create_table_client_address(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client_address(
                id SERIAL PRIMARY KEY,
                client_id uuid UNIQUE,
                address VARCHAR(50) DEFAULT NULL,
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW(),
            CONSTRAINT fk_client_id_clients_tb
                FOREIGN KEY(client_id) 
                REFERENCES client(client_id)
                ON DELETE SET NULL ON UPDATE CASCADE
            );
        """
        await self.curs.execute(q)


    async def _create_table_client_passport(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client_passport(
                id SERIAL PRIMARY KEY,
                client_id uuid UNIQUE,
                seria VARCHAR(4),
                number VARCHAR(6),
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW(),
            CONSTRAINT fk_client_id_clients_tb
                FOREIGN KEY(client_id) 
                REFERENCES client(client_id)
                ON DELETE SET NULL ON UPDATE CASCADE
            );
        """
        await self.curs.execute(q)

    
    async def _create_table_client_wallet(self) -> None:
        q = """
            CREATE TABLE IF NOT EXISTS client_wallet(
                id SERIAL PRIMARY KEY,
                client_id uuid,
                wallet_id uuid DEFAULT uuid_generate_v4 () UNIQUE,
                balance FLOAT DEFAULT 0.0,
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW(),
            CONSTRAINT fk_client_id_clients_tb
                FOREIGN KEY(client_id) 
                REFERENCES client(client_id)
                ON DELETE SET NULL ON UPDATE CASCADE
            );
        """
        await self.curs.execute(q)

    async def create_db_tables(self) -> None:
        create_table_commands = [
            self._create_table_client_type,
            self._create_table_client,
            self._create_table_client_address,
            self._create_table_client_contact,
            self._create_table_client_passport,
            self._create_table_client_wallet,
        ]

        await self.curs.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')  # support for uuid

        # order of table matters, that's why "gather" is not used
        for create_table in create_table_commands:
            await create_table()
