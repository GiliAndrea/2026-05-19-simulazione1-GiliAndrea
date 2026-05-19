from database.DB_connect import DBConnect

import mysql.connector

from model.Genre import Genre
from model.artist import Artist


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_artist() -> list[Artist]:
        cn = DBConnect.get_connection()
        cursor = cn.cursor(dictionary=True)

        query = """select *
                from artist a """
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        cn.close()
        return result

    @staticmethod
    def get_all_generi() -> list[Genre]:
        cn = DBConnect.get_connection()
        cursor = cn.cursor(dictionary=True)

        query = """select *
                from genre g """
        cursor.execute(query)

        result = []
        for row in cursor:
            result.append(Genre(**row))

        cursor.close()
        cn.close()
        return result

    @staticmethod
    def get_all_artist_genre(genere: int) -> list[Artist]:
        cn = DBConnect.get_connection()
        cursor = cn.cursor(dictionary=True)

        query = """select a.ArtistId, a.Name 
                from (select a.ArtistId as ArtistId
                from album a, track t
                where a.AlbumId = t.AlbumId and t.GenreId = %s
                group by a.ArtistId ) as v, artist as a
                where v.ArtistId = a.ArtistId """
        cursor.execute(query, (genere, ))

        result = []
        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        cn.close()
        return result
