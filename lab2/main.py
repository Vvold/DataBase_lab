import controller as con
from psycopg2 import Error
import sys

c = con.Controller()

try:
    command = sys.argv[1]
except IndexError:
    c.v.no_command()
else:
    if command == 'print_table':
        try:
            name = sys.argv[2]
        except IndexError:
            c.v.argument_error()
        else:
            c.print(name)

    elif command == 'delete_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3], "val": sys.argv[4]}
        except IndexError:
            c.v.argument_error()
        else:
            c.delete(args["name"], args["key"], args["val"])

    elif command == 'update_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'customer':
                args["name"], args["email"], args["subscription"] = sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'customer_library':
                args["start_date"], args["customer_id"] = sys.argv[4], sys.argv[5]
            elif args["name"] == 'customer_library_songs':
                args["library_id"], args["song_id"] = sys.argv[4], sys.argv[5]
            elif args["name"] == 'song':
                args["author"], args["album"], args["name"], args["duration"], args["year_of_release"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
            elif args["name"] == 'song_photo':
                args["url"], args["song_id"] = sys.argv[4], sys.argv[5]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'customer':
                c.update_customer(args["key"], args["name"], args["email"], args["subscription"])
            elif args["name"] == 'customer_library':
                c.update_customer_library(args["key"], args["start_date"], args["customer_id"])
            elif args["name"] == 'customer_library_songs':
                c.update_customer_library_songs(args["key"], args["library_id"], args["song_id"])
            elif args["name"] == 'song':
                c.update_song(args["key"], args["author"], args["album"], args["name"], args["duration"], args["year_of_release"])
            elif args["name"] == 'song_photo':
                c.update_song_photo(args["key"], args["url"], args["song_id"])

    elif command == 'insert_record':
        try:
            args = {"name": sys.argv[2], "key": sys.argv[3]}
            if args["name"] == 'customer':
                args["name"], args["email"], args["subscription"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6]
            elif args["name"] == 'customer_library':
                args["start_date"], args["customer_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["name"] == 'customer_library_songs':
                args["library_id"], args["song_id"] = \
                    sys.argv[4], sys.argv[5]
            elif args["name"] == 'song':
                args["author"], args["album"], args["name"], args["duration"], args["year_of_release"] = \
                    sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]
            elif args["name"] == 'song_photo':
                args["url"], args["song_id"] = \
                    sys.argv[4], sys.argv[5]
            else:
                c.v.wrong_table()
        except IndexError:
            c.v.argument_error()
        else:
            if args["name"] == 'customer':
                c.insert_customer(args["key"], args["name"], args["email"], args["subscription"])
            elif args["name"] == 'customer_library':
                c.insert_customer_library(args["key"], args["start_date"], args["customer_id"])
            elif args["name"] == 'customer_library_songs':
                c.insert_customer_library_songs(args["key"], args["library_id"], args["song_id"])
            elif args["name"] == 'song':
                c.insert_song(args["key"], args["author"], args["album"], args["name"], args["duration"], args["year_of_release"])
            elif args["name"] == 'song_photo':
                c.insert_song_photo(args["key"], args["url"], args["song_id"])

    elif command == 'generate_randomly':
        try:
            args = {"name": sys.argv[2], "n": int(sys.argv[3])}
        except (IndexError, Exception):
            print(Exception, IndexError)
        else:
            c.generate(args["name"], args["n"])

    elif command == 'search_records':
        if len(sys.argv) in [6, 9, 12]:
            search_num = c.v.get_search_num()
            try:
                search_num = int(search_num)
            except ValueError:
                c.v.invalid_search_num()
            else:
                if search_num > 0:
                    if len(sys.argv) == 6:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3],
                                "key1_name": sys.argv[4], "key2_name": sys.argv[5]}
                        c.search_two(args["table1_name"], args["table2_name"], args["key1_name"], args["key2_name"],
                                     c.v.proceed_search(search_num))
                    elif len(sys.argv) == 9:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3], "table3_name": sys.argv[4],
                                "key1_name": sys.argv[5], "key2_name": sys.argv[6], "key3_name": sys.argv[7],
                                "key13_name": sys.argv[8]}
                        c.search_three(args["table1_name"], args["table2_name"], args["table3_name"],
                                       args["key1_name"], args["key2_name"], args["key3_name"], args["key13_name"],
                                       c.v.proceed_search(search_num))
                    elif len(sys.argv) == 12:
                        args = {"table1_name": sys.argv[2], "table2_name": sys.argv[3], "table3_name": sys.argv[4],
                                "table4_name": sys.argv[5],
                                "key1_name": sys.argv[6], "key2_name": sys.argv[7], "key3_name": sys.argv[8],
                                "key13_name": sys.argv[9], "key4_name": sys.argv[10], "key24_name": sys.argv[11]}
                        c.search_four(args["table1_name"], args["table2_name"], args["table3_name"],
                                      args["table4_name"],
                                      args["key1_name"], args["key2_name"], args["key3_name"], args["key13_name"],
                                      args["key4_name"], args["key24_name"], c.v.proceed_search(search_num))
                else:
                    c.v.invalid_search_num()
        else:
            c.v.argument_error()

    elif command == 'help':
        c.v.print_help()
    else:
        c.v.wrong_command()
