from psycopg2 import Error
import model
import view


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

    def delete(self, table_name, value):
        t_name = self.v.valid.check_table_name(table_name)
        if t_name:
            k_val = self.v.valid.check_pk(value)
            count = 0
            if t_name == 'customer' and k_val:
                count = self.m.find_pk_customer(k_val)
            elif t_name == 'customer_library' and k_val:
                count = self.m.find_pk_customer_library(k_val)
            elif t_name == 'customer_library_songs' and k_val:
                count = self.m.find_pk_customer_library_songs(k_val)
            elif t_name == 'song' and k_val:
                count = self.m.find_pk_song(k_val)
            elif t_name == 'song_photo' and k_val:
                count = self.m.find_pk_song_photo(k_val)

            if count:
                if t_name == 'customer_library' or t_name == 'song':
                    count_p = self.m.find_fk_customer_library_songs(k_val, t_name)
                    if count_p:
                        self.v.cannot_delete()
                    else:
                        try:
                            if t_name == 'customer_library':
                                self.m.delete_data_customer_library(k_val)
                            elif t_name == 'song':
                                self.m.delete_data_song(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'customer':
                    count_c = self.m.find_fk_customer_library(k_val)
                    if count_c:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_customer(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                elif t_name == 'song':
                    count_c = self.m.find_fk_song_photo(k_val)
                    if count_c:
                        self.v.cannot_delete()
                    else:
                        try:
                            self.m.delete_data_song(k_val)
                        except (Exception, Error) as _ex:
                            self.v.sql_error(_ex)
                else:
                    try:
                        self.m.delete_data_customer_library_songs(k_val)
                    except (Exception, Error) as _ex:
                        self.v.sql_error(_ex)

            else:
                self.v.deletion_error()


    def update_customer(self, key: int, name: str, email: str, subscription: bool):
        if self.v.valid.check_possible_keys('customer', 'id', key):
            count_c = self.m.find_pk_customer(key)
            c_val = self.v.valid.check_pk(key)

        if count_c and c_val:
            try:
                self.m.update_data_customer(c_val, name, email, subscription)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_customer_library(self, key: int, start_date: int, customer_id: int):
        if self.v.valid.check_possible_keys('customer_library', 'id', key):
            count_cl = self.m.find_fk_customer_library(key)
            cl_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('customer', 'id', customer_id):
            count_c = self.m.find_pk_customer(customer_id)
            c_val = self.v.valid.check_pk(customer_id)

        if count_cl and cl_val and count_c and c_val:
            try:
                self.m.update_data_customer_library(cl_val, start_date, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_customer_library_songs(self, key: int, library_id: int, song_id: int):
        if self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            count_cls = self.m.find_pk_customer_library_songs(key)
            cls_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('customer_library', 'id', library_id):
            count_cl = self.m.find_pk_customer_library('customer_library', 'id', library_id)
            cl_val = self.v.valid.check_pk(library_id)
        if self.v.valid.check_possible_keys('song_id', 'id', song_id):
            count_s = self.m.find_pk_song(song_id)
            s_val = self.v.valid.check_pk(song_id)

        if count_cls and cls_val and count_cl and cl_val and count_s and s_val:
            try:
                self.m.update_data_customer_library_songs(cls_val, cl_val, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_song(self, key: int, author: str, album: str, name: str, duration: int, year_of_release: str):
        if self.v.valid.check_possible_keys('song', 'id', key):
            count_s = self.m.find_pk_song(key)
            s_val = self.v.valid.check_pk(key)

        if count_s and s_val:
            try:
                self.m.update_data_song(s_val, author, album, name, duration, year_of_release)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def update_song_photo(self, key: int, url: str, song_id: int):
        if self.v.valid.check_possible_keys('song_photo', 'id', key):
            count_sp = self.m.find_pk_song_photo(key)
            sp_val = self.v.valid.check_pk(key)
        if self.v.valid.check_possible_keys('song', 'id', song_id):
            count_s = self.m.find_pk_song(song_id)
            s_val = self.v.valid.check_pk(song_id)

        if count_sp and sp_val and count_s and s_val:
            try:
                self.m.update_data_song_photo(sp_val, url, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.updation_error()

    def insert_customer(self, key: str, name: str, email: str, subscription: str):
        if self.v.valid.check_possible_keys('customer', 'id', key):
            count_c = self.m.find_pk_customer(int(key))

        if (not count_c) and self.v.valid.check_possible_keys('customer', 'id', key):
            try:
                self.m.insert_data_customer(int(key), name, email, bool(subscription))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()


    def insert_customer_library(self, key: int, start_date: int, customer_id: int):
        if self.v.valid.check_possible_keys('customer_library', 'id', key):
            count_cl = self.m.find_pk_customer_library(key)
        if self.v.valid.check_possible_keys('customer', 'customer_id', customer_id):
            count_c = self.m.find_pk_customer(customer_id)
            c_val = self.v.valid.check_pk(customer_id)

        if (not count_cl) and count_c and c_val and self.v.valid.check_possible_keys('customer_library',
                                                                                             'library_id_', key):
            try:
                self.m.insert_data_customer_library(key, start_date, c_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_customer_library_songs(self, key: int, library_id: int, song_id: int):
        if self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            count_cls = self.m.find_pk_customer_library_songs(key)
        if self.v.valid.check_possible_keys('customer_library', 'library_id', library_id):
            count_cl = self.m.find_pk_customer_library(library_id)
            cl_val = self.v.valid.check_pk(library_id)
        if self.v.valid.check_possible_keys('song_id', 'id', song_id):
            count_s = self.m.find_pk_song(song_id)
            s_val = self.v.valid.check_pk(song_id)

        if (not count_cls) and count_cl and cl_val and count_s and s_val \
                and self.v.valid.check_possible_keys('customer_library_songs', 'id', key):
            try:
                self.m.insert_data_customer_library_songs(key, cl_val, s_val)
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_song(self, key: str, author: str, album: str, name: str, duration: str, year_of_release: str):
        if self.v.valid.check_possible_keys('song', 'id', key):
            count_s = self.m.find_pk_song(int(key))

        if (not count_s) and self.v.valid.check_possible_keys('song', 'id', key):
            try:
                self.m.insert_data_song(int(key), author, album, name, int(duration), int(year_of_release))
            except (Exception, Error) as _ex:
                self.v.sql_error(_ex)
        else:
            self.v.insertion_error()

    def insert_song_photo(self, key: int, url: str, song_id: int):
        if self.v.valid.check_possible_keys('song_photo', 'id', key):
            count_sp = self.m.find_pk_song_photo(key)
        if self.v.valid.check_possible_keys('song', 'id', song_id):
            count_s = self.m.find_pk_song(song_id)
            s_val = self.v.valid.check_pk(song_id, count_s)
        if (not count_sp) and count_s and s_val and self.v.valid.check_possible_keys('song_photo', 'id', key):
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

    def search_two(self):
        result = self.m.search_data_two_tables()
        self.v.print_search(result)

    def search_three(self):
        result = self.m.search_data_three_tables()
        self.v.print_search(result)

    def search_four(self):
        result = self.m.search_data_four_tables()
        self.v.print_search(result)
