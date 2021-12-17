import datetime
import psycopg2 as ps


class Model:
    def __init__(self):
        self.conn = None
        try:
            self.conn = ps.connect(
                database="music_service",
                user='postgres',
                password="Vb09gh54ty12",
                host='127.0.0.1',
                port="5432",
            )
        except(Exception, ps.DatabaseError) as error:
            print("[INFO] Error while working with Postgresql", error)

    def request(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return True
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchall()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def get_el(self, req: str):
        try:
            cursor = self.conn.cursor()
            print(req)
            cursor.execute(req)
            self.conn.commit()
            return cursor.fetchone()
        except(Exception, ps.DatabaseError, ps.ProgrammingError) as error:
            print(error)
            self.conn.rollback()
            return False

    def count(self, table_name: str):
        return self.get_el(f"select count(*) from public.\"{table_name}\"")

    def find(self, table_name: str, key_name: str, key_value: int):
        return self.get_el(f"select count(*) from public.\"{table_name}\" where {key_name}={key_value}")

    def max(self, table_name: str, key_name: str):
        return self.get_el(f"select max({key_name}) from public.\"{table_name}\"")

    def min(self, table_name: str, key_name: str):
        return self.get_el(f"select min({key_name}) from public.\"{table_name}\"")

    def print_customer(self) -> None:
        return self.get(f"SELECT * FROM public.\"customer\"")

    def print_customer_library(self) -> None:
        return self.get(f"SELECT * FROM public.\"customer_library\"")

    def print_customer_library_songs(self) -> None:
        return self.get(f"SELECT * FROM public.\"customer_library_songs\"")

    def print_song(self) -> None:
        return self.get(f"SELECT * FROM public.\"song\"")

    def print_song_photo(self) -> None:
        return self.get(f"SELECT * FROM public.\"song_photo\"")

    def delete_data(self, table_name: str, key_name: str, key_value) -> None:
        self.request(f"DELETE FROM public.\"{table_name}\" WHERE {key_name}={key_value};")

    def update_data_customer(self, key_value: int, name: str, email: str, subscription: bool) -> None:
        self.request(
            f"UPDATE public.\"customer\" SET name=\'{name}\', email=\'{email}\', subscription={subscription} WHERE id ={key_value};")

    def update_data_customer_library(self, key_value: int, start_date: int, customer_id: int) -> None:
        self.request(f"UPDATE public.\"customer_library\" SET start_date= {start_date}, customer_id={customer_id}"
                     f"WHERE id ={key_value};")

    def update_data_customer_library_songs(self, key_value: int, library_id: int, song_id: int) -> None:
        self.request(f"UPDATE public.\"customer_library_songs\" SET library_id={library_id}, song_id={song_id}"
                     f"WHERE id={key_value};")

    def update_data_song(self, key_value: int, author: str, album: str, name: str, duration: int,
                         year_of_release: str) -> None:
        self.request(
            f"UPDATE public.\"song\" SET author=\'{author}\', album=\'{album}\', name=\'{name}\', duration= {duration},"
            f"year_of_release = \'{year_of_release}\' WHERE id={key_value};")

    def update_data_song_photo(self, key_value: int, url: str, song_id: int) -> None:
        self.request(f"UPDATE public.\"song_photo\" SET url=\'{url}\', song_id={song_id} WHERE id={key_value};")

    def insert_data_customer(self, id: int, name: str, email: str, subscription: str) -> None:
        self.request(f"insert into public.\"customer\" (id, name, email, subscription) "
                     f"VALUES ({id}, \'{name}\', \'{email}\', \'{subscription})\';")

    def insert_data_customer_library(self, id: int, start_date: int, customer_id: int) -> None:
        self.request(f"insert into public.\"customer_library\" (id, start_date, customer_id) "
                     f"VALUES ({id}, {start_date}, {customer_id});")

    def insert_data_customer_library_songs(self, id: int, library_id: int, song_id: int) -> None:
        self.request(f"insert into public.\"customer_library_songs\" (id, library_id, song_id) "
                     f"VALUES ({id}, {library_id}, {song_id});")

    def insert_data_song(self, id: int, author: str, album: str, name: str, duration: int,
                         year_of_release: int) -> None:
        self.request(f"insert into public.\"song\" (id, author, album, name, duration, year_of_release) "
                     f"VALUES ({id}, \'{author}\', \'{album}\', \'{name}\', {duration}, {year_of_release});")

    def insert_data_song_photo(self, id: int, url: str, song_id: str) -> None:
        self.request(f"insert into public.\"song_photo\" (id, url, song_id) "
                     f"VALUES ({id}, \'{url}\', \'{song_id}\');")

    # поміняти цю функцію
    def customer_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.customer select (SELECT (MAX(id)+1) FROM public.customer), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "(SELECT TRUE  or FALSE );")

    def customer_library_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.customer_library select (SELECT MAX(id)+1 FROM public.customer_library), "
                         "FLOOR(RANDOM()*(200000-1)+1),"
                         "(SELECT id FROM public.customer LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.customer)-1))));")

    def customer_library_songs_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request(
                "insert into public.customer_library_songs select (SELECT MAX(id)+1 FROM public.customer_library_songs), "
                "(SELECT id FROM public.customer_library LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.customer_library)-1)))), "
                "(SELECT id FROM public.song LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.song)-1))));")

    def song_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.song select (SELECT (MAX(id)+1) FROM public.song), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''), "
                         "FLOOR(RANDOM()*(200000-1)+1),"
                         "FLOOR(RANDOM()*(2021-1)+1); ")

    def song_photo_data_generator(self, times: int) -> None:
        for i in range(times):
            self.request("insert into public.song_photo select (SELECT MAX(id)+1 FROM public.song_photo), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "(SELECT id FROM public.song LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.song)-1))));")

    def search_data_two_tables(self, table1_name: str, table2_name: str, table1_key, table2_key,
                               search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} "
                        f"where {search}")

    def search_data_three_tables(self, table1_name: str, table2_name: str, table3_name: str,
                                 table1_key, table2_key, table3_key, table13_key,
                                 search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} inner join public.{table3_name} as three "
                        f"on three.{table3_key}=one.{table13_key} "
                        f"where {search}")

    def search_data_four_tables(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                               table1_key, table2_key, table3_key, table13_key,
                               table4_key, table24_key,
                               search: str):
        return self.get(f"select * from public.{table1_name} as one inner join public.{table2_name} as two "
                        f"on one.{table1_key}=two.{table2_key} inner join public.{table3_name} as three "
                        f"on three.{table3_key}=one.{table13_key} inner join public.{table4_name} as four "
                        f"on four.{table4_key}=two.{table24_key} "
                        f"where {search}")

