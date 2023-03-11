from aiopg import Cursor


class InitTables:
    def __init__(self, curs: Cursor) -> None:
        self.curs = curs

    @staticmethod
    def _create_table_client() -> str:
        return """
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                client_id uuid DEFAULT uuid_generate_v4 () UNIQUE,
                fio VARCHAR(120),
                birthdate VARCHAR(10),
                deleted BOOLEAN DEFAULT FALSE,
                created_time TIMESTAMP DEFAULT NOW()
            );
        """

    @staticmethod
    def _create_table_contact() -> str:
        return """
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

    @staticmethod
    def _create_table_address() -> str:
        return """
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

    @staticmethod
    def _create_table_passport() -> str:
        return """
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

    @staticmethod
    def _create_table_wallet() -> str:
        return """
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

    async def create_db_tables(self) -> None:
        create_table_commands = []

        for func in self.__class__.__dict__:
            if func.startswith("_create_table_"):
                create_table_commands.append(self.__getattribute__(func))

        await self.curs.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')  # support for uuid

        for create_table in create_table_commands:
            creat_table_query = create_table()
            # order of table matters, that's why "gather" is not used
            await self.curs.execute(creat_table_query)
