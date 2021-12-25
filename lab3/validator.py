
class Validator:
    def __init__(self):
        self.error = ''
        self.er_flag = False

    def check_table_name(self, arg: str):
        if arg in ['customer', 'customer_library', 'customer_library_songs', 'song', 'song_photo']:
            return arg
        else:
            self.er_flag = True
            self.error = f'table {arg} does not exist in the database'
            print(self.error)
            return False

    def check_pkey_value(self, arg: str, min_val: int, max_val: int):
        try:
            value = int(arg)
        except ValueError:
            self.er_flag = True
            self.error = f'{arg} is not correct primary key value'
            print(self.error)
            return 0
        else:
            if min_val <= value <= max_val:
                return value
            else:
                self.er_flag = True
                self.error = f'{arg} is not existing primary key value'
                print(self.error)
                return 0

    def check_pk_name(self, table_name: str, key_name: str):
        if table_name == 'customer' and key_name == 'id' \
                or table_name == 'customer_library' and key_name == 'id' \
                or table_name == 'customer_library_songs' and key_name == 'id' \
                or table_name == 'song' and key_name == 'id' \
                or table_name == 'song_photo' and key_name == 'id':
            return key_name
        else:
            self.er_flag = True
            self.error = f'key {key_name} is not a primary key of table {table_name}'
            print(self.error)
            return False

    def check_pk(self, val):
        try:
            value = int(val)
            return value
        except ValueError:
            self.er_flag = True
            self.error = f'{val} is not correct primary key value'
            print(self.error)
            return 0

    def check_key_names(self, table_name: str, key: str):
        if table_name == 'customer' and key in ['id', 'name', 'email', 'subscription']:
            return True
        elif table_name == 'customer_library' and key in ['id', 'start_date', 'customer_id']:
            return True
        elif table_name == 'customer_library_songs' and key in ['id', 'library_id', 'song_id']:
            return True
        elif table_name == 'song' and key in ['id', 'author', 'album', 'name', 'duration', 'year_of_release']:
            return True
        elif table_name == 'song_photo' and key in ['id', 'url', 'song_id']:
            return True
        else:
            self.er_flag = True
            self.error = f'{key} is not correct name for {table_name} table'
            print(self.error)
            return False

    def check_possible_keys(self, table_name: str, key: str, val):
        if table_name == 'customer':
            if key in ['id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['name', 'email', 'subscription']:
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for customer table'
                print(self.error)
                return False
        elif table_name == 'customer_library':
            if key in ['id', 'customer_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'date':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct date value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for customer_library table'
                print(self.error)
                return False
        elif table_name == 'customer_library_songs':
            if key in ['id', 'library_id', 'song_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for customer_library_songs table'
                print(self.error)
                return False
        elif table_name == 'song':
            if key == 'id':
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key in ['author', 'album', 'name']:
                return True
            elif key in ['duration', 'year_of_release']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct duration or year_of_release value'
                    print(self.error)
                    return False
                else:
                    return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for song table'
                print(self.error)
                return False

        elif table_name == 'song_photo':
            if key in ['id', 'song_id']:
                try:
                    value = int(val)
                except ValueError:
                    self.er_flag = True
                    self.error = f'{val} is not correct key value'
                    print(self.error)
                    return False
                else:
                    return True
            elif key == 'url':
                return True
            else:
                self.er_flag = True
                self.error = f'{key} is not correct name for song_photo table'
                print(self.error)
                return False
