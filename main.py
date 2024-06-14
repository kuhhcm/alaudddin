import psycopg2


class Database_manager:
    def __init__(self, dbname, host, port, user, password):
        self.dbname: str = dbname
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password
        self.connection: psycopg2.extensions.connection = None
        self.cursor: psycopg2.extensions.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(dbname=self.dbname,
                                               host=self.host,
                                               port=self.port,
                                               user=self.user,
                                               password=self.password)
            print("Connected successfully")
        except Exception as e:
            print(f"Connection refused: {e}")
        else:
            self.cursor = self.connection.cursor()

    def insert(self, table_name, **kwargs):
        columns = ', '.join([column for column in kwargs.get('columns', [])])
        values = ', '.join([f"'{column}'" if type(column) == str else f"{column}" for column in kwargs.get('values', [])])
        query = f"INSERT INTO {table_name} ({columns}) values ({values})"
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as error:
            print(f"Something gone wrong: {error}")

    def select(self, table_name, **kwargs):
        if kwargs.get('columns', False):
            columns = ', '.join(
                [column for column in kwargs.get('columns', [])])
            query = f"SELECT {columns} from {table_name}"
        else:
            query = f"SELECT * from {table_name}"
        try:
            self.cursor.execute(query=query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Something gone wrong: {e}")

    def delete(self, table_name, id):
        if id:
            query = f"DELETE FROM {table_name} WHERE id={id}"
            try:
                self.cursor.execute(query)
                self.connection.commit()
            except Exception as e:
                print(f"Something gone wrong: {e}")
        else:
            print("You must provide id to delete something")

    def update(self, table_name, id, **kwargs):
        columns = kwargs.get('columns', [])
        values = kwargs.get('values', [])
        if len(columns) != len(values):
            print("Numberof columns and values must be equal")
        sub_query = ""
        for idx in range(len(columns)):
            sub_query += f"{columns[idx]} = '{values[idx]}'"
            if not (idx == (len(columns) - 1)):
                sub_query+=", "
            print(sub_query)
        query = f"UPDATE {table_name} SET {sub_query} WHERE id = {id}"
        try:
            self.cursor.execute(query=query)
            self.connection.commit()
        except Exception as error:
            print(f"Something gone wrong: {error}")


database = Database_manager("postgres", "localhost",
                            5432, "postgres", "postgres")
database.connect()
