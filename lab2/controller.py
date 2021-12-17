import psycopg2
from psycopg2 import Error
import model
import view
import datetime
import time


class Controller:
    def __init__(self):
        self.v = view.View()
        self.m = model.Model()

    def print(self, table_name):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'customer':
                self.v.print_customer(self.m.print_customer())
            elif t_name == 'customer_library':
                self.v.print_customer_library(self.m.print_customer_library())
            elif t_name == 'customer_library_songs':
                self.v.print_customer_library_songs(self.m.print_customer_library_songs())
            elif t_name == 'song':
                self.v.print_song(self.m.print_song())
            elif t_name == 'song_photo':
                self.v.print_song_photo(self.m.print_song_photo())

    def delete(self, table_name, key_name, value):
        t_name = self.v.valid.check_table_name(table_name).upper()
        k_name = self.v.valid.check_pk_name(table_name, key_name).upper()
        if t_name and k_name:
            count = self.m.find(t_name, k_name, value)
            k_val = self.v.valid.check_pk(value, count)
            if k_val:
                if t_name == 'customer_library' or t_name == 'song':
                    if t_name == 'customer_library':
                        count_p = self.m.find('customer_library_songs', 'library_id', value)[0]
                    if t_name == 'song':
                        count_p = self.m.find('customer_library_songs', 'song_id', value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'customer':
                    count_p = self.m.find('customer_library', 'customer_id', value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'song':
                    count_p = self.m.find('song_photo', 'song_id', value)[0]
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data(table_name, key_name, k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data(table_name, key_name, k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)
            else:
                self.v.deletion_error()

    def update_customer(self, key: int, name: str, email: str, subscription: bool):
        if self.v.valid.check_possible_keys('customer', 'id', key):
            count_c = self.m.find('customer', 'id', key)
            c_val = self.v.valid.check_pk(key, count_c)

        if c_val:
            try:
                self.m.update_data_customer(c_val, name, email, subscription)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_customer_library(self, key: int, start_date: int, customer_id: int):
        if self.v.valid.check_possible_keys('customer_library', 'id', key):
            count_cl = self.m.find('customer_library', 'id', key)
            cl_val = self.v.valid.check_pk(key, count_cl)
        if self.v.valid.check_possible_keys('customer', 'id', customer_id):
            count_c = self.m.find('customer', 'id', customer_id)
            c_val = self.v.valid.check_pk(customer_id, count_c)

        if cl_val and c_val:
            try:
                self.m.update_data_customer_library(cl_val, start_date, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_customer_library_songs(self, key: int, library_id: int, song_id: int):
        if self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            count_cls = self.m.find('customer_library_songs', 'id', key)
            cls_val = self.v.valid.check_pk(key, count_cls)
        if self.v.valid.check_possible_keys('customer_library', 'id', library_id):
            count_cl = self.m.find('customer_library', 'id', library_id)
            cl_val = self.v.valid.check_pk(library_id, count_cl)
        if self.v.valid.check_possible_keys('song_id', 'id', song_id):
            count_s = self.m.find('song', 'id', song_id)
            s_val = self.v.valid.check_pk(song_id, count_s)

        if cls_val and cl_val and s_val:
            try:
                self.m.update_data_customer_library_songs(cls_val, cl_val, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_song(self, key: int, author: str, album: str, name: str, duration: int, year_of_release: str):
        if self.v.valid.check_possible_keys('song', 'id', key):
            count_s = self.m.find('song', 'id', key)
            s_val = self.v.valid.check_pk(key, count_s)

        if s_val:
            try:
                self.m.update_data_song(s_val, author, album, name, duration, year_of_release)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_song_photo(self, key: int, url: str, song_id: int):
        if self.v.valid.check_possible_keys('song_photo', 'id', key):
            count_sp = self.m.find('song_photo', 'id', key)
            sp_val = self.v.valid.check_pk(key, count_sp)
        if self.v.valid.check_possible_keys('song', 'id', song_id):
            count_s = self.m.find('song', 'id', song_id)
            s_val = self.v.valid.check_pk(song_id, count_s)

        if sp_val and s_val:
            try:
                self.m.update_data_song_photo(sp_val, url, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_customer(self, key: int, name: str, email: str, subcription: bool):
        if self.v.valid.check_possible_keys('customer', 'id', key):
            count_c = self.m.find('customer', 'id', key)[0]

        if (not count_c or count_c == (0,)) and self.v.valid.check_possible_keys('customer', 'id', key):
            try:
                self.m.insert_data_customer(key, name, email, subcription)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_customer_library(self, key: int, start_date: int, customer_id: int):
        if self.v.valid.check_possible_keys('customer_library', 'id', key):
            count_cl = self.m.find('customer_library', 'id', key)[0]
        if self.v.valid.check_possible_keys('customer', 'customer_id', customer_id):
            count_c = self.m.find('customer', 'customer_id', customer_id)
            c_val = self.v.valid.check_pk(customer_id, count_c)

        if (not count_cl or count_cl == (0,)) and self.v.valid.check_possible_keys('customer_library',
                                                                                             'library_id_', key):
            try:
                self.m.insert_data_customer_library(key, start_date, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_customer_library_songs(self, key: int, library_id: int, song_id: int):
        if self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            count_cls = self.m.find('customer_library_songs', 'id', key)[0]
        if self.v.valid.check_possible_keys('customer_library', 'library_id', library_id):
            count_cl = self.m.find('customer_library', 'library_id', library_id)
            cl_val = self.v.valid.check_pk(library_id, count_cl)
        if self.v.valid.check_possible_keys('song_id', 'id', song_id):
            count_s = self.m.find('song', 'song_id', song_id)
            s_val = self.v.valid.check_pk(song_id, count_s)

        if (not count_cls or count_cls == (0,)) and cl_val and s_val \
                and self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            try:
                self.m.insert_data_customer_library_songs(key, cl_val, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_song(self, key: int, author: str, album: str, name: str, duration: int, year_of_release: str):
        if self.v.valid.check_possible_keys('song', 'id', key):
            count_s = self.m.find('song', 'id', key)[0]

        if (not count_s or count_s == (0,)) and self.v.valid.check_possible_keys('song', 'id', key):
            try:
                self.m.insert_data_song(key, author, album, name, duration, year_of_release)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_song_photo(self, key: int, url: str, song_id: int):
        if self.v.valid.check_possible_keys('song_photo', 'id', key):
            count_sp = self.m.find('song_photo', 'id', key)[0]
        if self.v.valid.check_possible_keys('song', 'id', song_id):
            count_s = self.m.find('song', 'id', song_id)
            s_val = self.v.valid.check_pk(song_id, count_s)
        if (not count_sp or count_sp == (0,)) and self.v.valid.check_possible_keys('song_photo', 'id', key):
            try:
                self.m.insert_data_song_photo(key, url, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def generate(self, table_name: str, n: int):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            if t_name == 'customer':
                self.m.customer_data_generator(n)
            elif t_name == 'customer_library':
                self.m.customer_library_data_generator(n)
            elif t_name == 'customer_library_songs':
                self.m.customer_library_songs_data_generator(n)
            elif t_name == 'song':
                self.m.song_data_generator(n)
            elif t_name == 'song_photo':
                self.m.song_photo_data_generator(n)

    def search_two(self, table1_name: str, table2_name: str, table1_key: str, table2_key: str, search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and t2_n \
                and self.v.valid.check_key_names(t2_n, table2_key):
            start_time = time.time()
            result = self.m.search_data_two_tables(table1_name, table2_name, table1_key, table2_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_three(self, table1_name: str, table2_name: str, table3_name: str,
                     table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                     search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key):
            start_time = time.time()
            result = self.m.search_data_three_tables(table1_name, table2_name, table3_name,
                                                     table1_key, table2_key, table3_key, table13_key,
                                                     search)
            self.v.print_time(start_time)
            self.v.print_search(result)

    def search_four(self, table1_name: str, table2_name: str, table3_name: str, table4_name: str,
                    table1_key: str, table2_key: str, table3_key: str, table13_key: str,
                    table4_key: str, table24_key: str,
                    search: str):
        t1_n = self.v.valid.check_table_name(table1_name)
        t2_n = self.v.valid.check_table_name(table2_name)
        t3_n = self.v.valid.check_table_name(table3_name)
        t4_n = self.v.valid.check_table_name(table2_name)
        if t1_n and self.v.valid.check_key_names(t1_n, table1_key) and self.v.valid.check_key_names(t1_n, table13_key) \
                and t2_n and self.v.valid.check_key_names(t2_n, table2_key) \
                and self.v.valid.check_key_names(t2_n, table24_key) \
                and t3_n and self.v.valid.check_key_names(t3_n, table3_key) \
                and self.v.valid.check_key_names(t3_n, table13_key) \
                and t4_n and self.v.valid.check_key_names(t4_n, table4_key) \
                and self.v.valid.check_key_names(t4_n, table24_key):
            start_time = time.time()
            result = self.m.search_data_four_tables(table1_name, table2_name, table3_name, table4_name,
                                                   table1_key, table2_key, table3_key, table13_key,
                                                   table4_key, table24_key,
                                                   search)
            self.v.print_time(start_time)
            self.v.print_search(result)
