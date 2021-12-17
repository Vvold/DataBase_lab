import datetime
import time
import validator


class View:
    def __init__(self):
        self.valid = validator.Validator()

    def cannot_delete(self) -> None:
        print('this record is connected with another table, deleting will '
              'throw error')

    def sql_error(self, e) -> None:
        print("[INFO] Error while working with Postgresql", e)

    def insertion_error(self) -> None:
        print('Something went wrong (record with such id exists or inappropriate foreign key values)')

    def updation_error(self) -> None:
        print('Something went wrong (record with such id does not exist or inappropriate foreign key value)')

    def deletion_error(self) -> None:
        print('record with such id does not exist')

    def invalid_interval(self) -> None:
        print('invalid interval input')

    def print_time(self, start) -> None:
        print("--- %s seconds ---" % (time.time() - start))

    def print_search(self, result):
        print('search result:')
        for row in result:
            for i in range(0, len(row)):
                print(row[i])
            print('_________________________________________________________________________________________')

    def print_customer(self, table):
        print('customer table:')
        for row in table:
            print('id:', row[0], '\tname:', row[1], '\temail:', row[2], '\tsubscription:', row[3])
            print('_________________________________________________________________________________________')

    def print_customer_library(self, table):
        print('customer_library table:')
        for row in table:
            print('id:', row[0], '\tstart_date:', row[1], '\tcustomer_id:', row[2])
            print('_________________________________________________________________________________________')

    def print_customer_library_songs(self, table):
        print('customer_library_songs table:')
        for row in table:
            print('id:', row[0], '\tlibrary_id:', row[1], '\tsong_id:', row[2])
            print('_________________________________________________________________________________________')

    def print_song(self, table):
        print('song table:')
        for row in table:
            print('id:', row[0], '\tauthor:', row[1], '\talbum:', row[2], '\tname:', row[3], '\tduration:', row[4],
                  '\tyear_of_release:', row[5])
            print('_________________________________________________________________________________________')

    def print_song_photo(self, table):
        print('song_photo table:')
        for row in table:
            print('id:', row[0], '\turl:', row[1], '\tsong_id:', row[2])
            print('_________________________________________________________________________________________')

    # поміняти цю функцію
    def print_help(self):
        print('print_table - outputs the specified table \n\targument (table_name) is required')
        print('delete_record - deletes the specified record from table \n'
              '\targuments (table_name, key_name, key_value) are required')
        print('update_record - updates record with specified id in table\n'
              '\tcustomer args (table_name, id, name, email, subscription)\n'
              '\tcustomer_library args (table_name, id, start_date, customer_id)\n'
              '\tcustomer_library_songs args (table_name, id, library_id, song_id)\n'
              '\tsong args (table_name, id, author, album, name, duration, year_of_release)\n'
              '\tsong_photo args (table_name, id, url, song_id)')
        print('insert_record - inserts record into specified table \n'
              '\tcustomer args (table_name, id, name, email, subscription)\n'
              '\tcustomer_library args (table_name, id, start_date, customer_id)\n'
              '\tcustomer_library_songs args (table_name, id, library_id, song_id)\n'
              '\tsong args (table_name, id, author, album, name, duration, year_of_release)\n'
              '\tsong_photo args (table_name, id, url, song_id)')
        print('generate_randomly - generates n random records in table\n'
              '\targuments (table_name, n) are required')
        print('search_records - search for records in two or more tables using one or more keys \n'
              '\targuments\n')

    def proceed_search(self, search_num):
        search = ''
        for i in range(0, search_num):
            while True:
                search_type = input('specify the type of data you want to search for '
                                    '(numeric or string): ')
                if search_type == 'numeric' or search_type == 'string':
                    break
            key = input('specify the name of key by which you`d like to perform search '
                        'in form: table_number.key_name: ')

            if search_type == 'numeric':
                a = input('specify the left end of search interval: ')
                b = input('specify the right end of search interval: ')
                if search == '':
                    search = self.numeric_search(a, b, key)
                else:
                    search += ' and ' + self.numeric_search(a, b, key)

            elif search_type == 'string':
                string = input('specify the string you`d like to search for: ')
                if search == '':
                    search = self.string_search(string, key)
                else:
                    search += ' and ' + self.string_search(string, key)
        return search

    def numeric_search(self, a: str, b: str, key: str):
        try:
            a, b = int(a), int(b)
        except ValueError:
            self.invalid_interval()
        else:
            return f"{a}<{key} and {key}<{b}"

    def date_search(self, a: str, b: str, key: str):
        try:
            arr = [int(x) for x in a.split(sep='.')]
            brr = [int(x) for x in b.split(sep='.')]
        except Exception:
            print(Exception)
            self.invalid_interval()
        else:
            return f"{key} BETWEEN \'{datetime.datetime(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5])}\' " \
                   f"AND \'{datetime.datetime(brr[0], brr[1], brr[2], brr[3], brr[4], brr[5])}\'"

    def string_search(self, string: str, key: str):
        return f"{key} LIKE \'{string}\'"

    def get_search_num(self):
        return input('specify the number of attributes you`d like to search by: ')

    def invalid_search_num(self):
        print('should be number different from 0')

    def argument_error(self):
        print('no required arguments specified')

    def wrong_table(self):
        print('wrong table name')

    def no_command(self):
        print('no command name specified, type help to see possible commands')

    def wrong_command(self):
        print('unknown command name, type help to see possible commands')
