from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, select, and_
from sqlalchemy.orm import relationship
from db import Library, Session, engine


def recreate_database():
    Library.metadata.drop_all(engine)
    Library.metadata.create_all(engine)


class Customer(Library):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    subscription = Column(Boolean)
    libraries = relationship("Customer_library")

    def __init__(self, id, name, email, subscription):
        self.id = id
        self.name = name
        self.email = email
        self.subscription = subscription

    def __repr__(self):
        return "{:>10}{:>35}{:>35}{:>20}" \
            .format(self.id, self.name, self.email, self.subscription)


class Customer_library(Library):
    __tablename__ = 'customer_library'
    id = Column(Integer, primary_key=True)
    start_date = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customers = relationship("Customer_library_songs")

    def __init__(self, id, start_date, customer_id):
        self.id = id
        self.start_date = start_date
        self.customer_id = customer_id

    def __repr__(self):
        return "{:>10}{:>20}{:>20}" \
            .format(self.id, self.start_date, self.customer_id)


class Customer_library_songs(Library):
    __tablename__ = 'customer_library_songs'
    id = Column(Integer, primary_key=True)
    library_id = Column(Integer, ForeignKey('customer_library.id'))
    song_id = Column(Integer, ForeignKey('song.id'))

    def __init__(self, id, library_id, song_id):
        self.id = id
        self.library_id = library_id
        self.song_id = song_id

    def __repr__(self):
        return "{:>10}{:>15}{:>10}" \
            .format(self.id, self.library_id, self.song_id)


class Song(Library):
    __tablename__ = 'song'
    id = Column(Integer, primary_key=True)
    author = Column(String)
    album = Column(String)
    name = Column(String)
    duration = Column(Integer)
    year_of_release = Column(Integer)
    song_photos = relationship("Song_photo")
    customer_library_songs = relationship("Customer_library_songs")

    def __init__(self, id, author, album, name, duration, year_of_release):
        self.id = id
        self.author = author
        self.album = album
        self.name = name
        self.duration = duration
        self.year_of_release = year_of_release

    def __repr__(self):
        return "{:>10}{:>25}{:>20}{:>20}{:>20}{:>20}" \
            .format(self.id, self.author, self.album, self.name, self.duration, self.year_of_release)


class Song_photo(Library):
    __tablename__ = 'song_photo'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    song_id = Column(Integer, ForeignKey('song.id'))

    def __init__(self, id, url, song_id):
        self.id_product = id
        self.url = url
        self.song_id = song_id

    def __repr__(self):
        return "{:>10}{:>30}{:>10}" \
            .format(self.id, self.url, self.song_id)


class Model:
    def __init__(self):
        self.session = Session()
        self.connection = engine.connect()

    def find_pk_customer(self, key_value: int):
        return self.session.query(Customer).filter_by(id=key_value).first()

    def find_pk_customer_library(self, key_value: int):
        return self.session.query(Customer_library).filter_by(id=key_value).first()

    def find_fk_customer_library(self, key_value: int):
        return self.session.query(Customer_library).filter_by(customer_id=key_value).first()

    def find_pk_customer_library_songs(self, key_value: int):
        return self.session.query(Customer_library_songs).filter_by(id=key_value).first()

    def find_fk_customer_library_songs(self, key_value: int, table_name: str):
        if table_name == "customer_library":
            return self.session.query(Customer_library_songs).filter_by(library_id=key_value).first()
        elif table_name == "song":
            return self.session.query(Customer_library_songs).filter_by(song_id=key_value).first()

    def find_pk_song(self, key_value: int):
        return self.session.query(Song).filter_by(id=key_value).first()

    def find_pk_song_photo(self, key_value: int):
        return self.session.query(Song_photo).filter_by(id=key_value).first()

    def find_fk_song_photo(self, key_value: int):
        return self.session.query(Song_photo).filter_by(song_id=key_value).first()

    def print_customer(self):
        return self.session.query(Customer).order_by(Customer.id.asc()).all()

    def print_customer_library(self):
        return self.session.query(Customer_library).order_by(Customer_library.id.asc()).all()

    def print_customer_library_songs(self):
        return self.session.query(Customer_library_songs).order_by(Customer_library_songs.id.asc()).all()

    def print_song(self):
        return self.session.query(Song).order_by(Song.id.asc()).all()

    def print_song_photo(self):
        return self.session.query(Song_photo).order_by(Song_photo.id.asc()).all()

    def delete_data_customer(self, id) -> None:
        self.session.query(Customer).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_customer_library(self, id) -> None:
        self.session.query(Customer_library).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_customer_library_songs(self, id) -> None:
        self.session.query(Customer_library_songs).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_song(self, id) -> None:
        self.session.query(Song).filter_by(id=id).delete()
        self.session.commit()

    def delete_data_song_photo(self, id) -> None:
        self.session.query(Song_photo).filter_by(id=id).delete()
        self.session.commit()

    def update_data_customer(self, id: int, name: str, email: str, subscription: bool) -> None:
        self.session.query(Customer).filter_by(id=id) \
            .update({Customer.name: name, Customer.email: email, Customer.subscription: subscription})
        self.session.commit()

    def update_data_customer_library(self, id: int, start_date: int, customer_id: int) -> None:
        self.session.query(Customer_library).filter_by(id=id) \
            .update({Customer_library.start_date: start_date, Customer_library.customer_id: customer_id})
        self.session.commit()

    def update_data_customer_library_songs(self, id: int, library_id: int, song_id: int) -> None:
        self.session.query(Customer_library_songs).filter_by(id=id) \
            .update({Customer_library_songs.library_id: library_id, Customer_library_songs.song_id: song_id})
        self.session.commit()

    def update_data_song(self, id: int, author: str, album: str, name: str, duration: int,
                         year_of_release: str) -> None:
        self.session.query(Song).filter_by(id=id) \
            .update({Song.author: author, Song.album: album, Song.name: name, Song.duration: duration,
                     Song.year_of_release: year_of_release})
        self.session.commit()

    def update_data_song_photo(self, id: int, url: str, song_id: int) -> None:
        self.session.query(Song_photo).filter_by(id=id) \
            .update({Song_photo.url: url, Song.song_id: song_id})
        self.session.commit()

    def insert_data_customer(self, id: int, name: str, email: str, subscription: bool) -> None:
        customer = Customer(id=id, name=name, email=email, subscription=subscription)
        self.session.add(customer)
        self.session.commit()

    def insert_data_customer_library(self, id: int, start_date: int, customer_id: int) -> None:
        customer_library = Customer_library(id=id, start_date=start_date, customer_id=customer_id)
        self.session.add(customer_library)
        self.session.commit()

    def insert_data_customer_library_songs(self, id: int, library_id: int, song_id: int) -> None:
        customer_library_songs = Customer_library_songs(id=id, library_id=library_id, song_id=song_id)
        self.session.add(customer_library_songs)
        self.session.commit()

    def insert_data_song(self, id: int, author: str, album: str, name: str, duration: int,
                         year_of_release: int) -> None:
        song = Song(id=id, author=author, album=album, name=name, duration=duration, year_of_release=year_of_release)
        self.session.add(song)
        self.session.commit()

    def insert_data_song_photo(self, id: int, url: str, song_id: str) -> None:
        song_photo = Song_photo(id=id, url=url, song_id=song_id)
        self.session.add(song_photo)
        self.session.commit()

    def customer_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.customer select (SELECT (MAX(id)+1) FROM public.customer), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "(SELECT TRUE  or FALSE );")

    def customer_library_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.customer_library select (SELECT MAX(id)+1 FROM public.customer_library), "
                         "FLOOR(RANDOM()*(200000-1)+1),"
                         "(SELECT id FROM public.customer LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.customer)-1))));")

    def customer_library_songs_data_generator(self, times: int) -> None:
        for i in range(times):
            sself.connection.execute(
                "insert into public.customer_library_songs select (SELECT MAX(id)+1 FROM public.customer_library_songs), "
                "(SELECT id FROM public.customer_library LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.customer_library)-1)))), "
                "(SELECT id FROM public.song LIMIT 1 OFFSET "
                "(round(random() *((SELECT COUNT(id) FROM public.song)-1))));")

    def song_data_generator(self, times: int) -> None:
        for i in range(times):
            self.connection.execute("insert into public.song select (SELECT (MAX(id)+1) FROM public.song), "
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
            self.connection.execute("insert into public.song_photo select (SELECT MAX(id)+1 FROM public.song_photo), "
                         "array_to_string(ARRAY(SELECT chr((97 + round(random() * 25)) :: integer) "
                         "FROM generate_series(1, FLOOR(RANDOM()*(10-3)+3):: integer)), ''),"
                         "(SELECT id FROM public.song LIMIT 1 OFFSET "
                         "(round(random() *((SELECT COUNT(id) FROM public.song)-1))));")

    def search_data_two_tables(self):
        return self.session.query(Customer) \
            .join(Customer_library) \
            .filter(and_(
            Customer.id.between(0, 5),
            Customer_library.id.between(0, 5)
        )) \
            .all()

    def search_data_three_tables(self):
        return self.session.query(Customer) \
            .join(Customer_library).join(Customer_library_songs) \
            .filter(and_(
            Customer.id.between(0, 5),
            Customer_library.id.between(0, 5),
            Customer_library_songs.id.between(0, 5)
        )) \
            .all()

    def search_data_four_tables(self):
        return self.session.query(Customer) \
            .join(Customer_library).join(Customer_library_songs).join(Song) \
            .filter(and_(
            Customer.id.between(0, 5),
            Customer_library.id.between(0, 5),
            Customer_library_songs.id.between(0, 5),
            Song.duration.between(0, 260)
        )) \
            .all()
