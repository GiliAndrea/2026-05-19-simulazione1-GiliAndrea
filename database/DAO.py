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


    # it is possible to use this function to fill the map_artist, however I decided to do not use that
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
    def get_all_artist_genre(genre: int) -> list[Artist]:
        cn = DBConnect.get_connection()
        cursor = cn.cursor(dictionary=True)

        query = """select a.ArtistId, a.Name 
                from (select a.ArtistId as ArtistId
                from album a, track t
                where a.AlbumId = t.AlbumId and t.GenreId = %s
                group by a.ArtistId ) as v, artist as a
                where v.ArtistId = a.ArtistId """
        cursor.execute(query, (genre, ))

        result = []
        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        cn.close()
        return result

    @staticmethod
    def get_all_weight(genre : int ):
        cn = DBConnect.get_connection()
        cursor = cn.cursor()

        query = """select a.ArtistId, sum(i.Quantity) as totVendite
                from album a 
                inner join track t on t.AlbumId = a.AlbumId
                inner join invoiceline i on i.TrackId = t.TrackId
                where t.GenreId = %s
                group by a.ArtistId"""
        cursor.execute(query, (genre, ))

        result = []
        for row in cursor:
            # tuple whit artist_id and popularity
            result.append((row[0], row[1]))

        cursor.close()
        cn.close()
        return result

    @staticmethod
    def get_all_edges(genre: int):
        cn = DBConnect.get_connection()
        cursor = cn.cursor()

        query = """select distinct t1.artistid as artista1, t2.artistid as artista2 
                from (select distinct(a.ArtistId) as artistId, i2.CustomerId 
                from artist a
                join album a2 on a2.ArtistId = a.ArtistId
                join track t on t.AlbumId = a2.AlbumId
                join invoiceline i on i.TrackId = t.TrackId
                join invoice i2 on i2.InvoiceId = i.InvoiceId
                where t.GenreId = %s
                order by i2.CustomerId) as t1
                join (select distinct(a.ArtistId) as artistId, i2.CustomerId 
                from artist a
                join album a2 on a2.ArtistId = a.ArtistId
                join track t on t.AlbumId = a2.AlbumId
                join invoiceline i on i.TrackId = t.TrackId
                join invoice i2 on i2.InvoiceId = i.InvoiceId
                where t.GenreId = %s
                order by i2.CustomerId) as t2 on t1.customerid = t2.customerid 
                where t1.artistid > t2.artistid
                order by t1.artistid, t2.artistid """
        cursor.execute(query, (genre, genre))

        result = []
        for row in cursor:
            # tuple with artist_1 and artist_2
            result.append((row[0], row[1]))

        cursor.close()
        cn.close()
        return result
