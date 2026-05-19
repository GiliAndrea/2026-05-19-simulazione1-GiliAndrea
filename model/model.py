import networkx as nx

from database.DAO import DAO
from model.Genre import Genre
from model.artist import Artist


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph


    def crea_grafo(self, genere: int):

        self._grafo.add_edges_from(DAO.get_all_artist_genre(genere))







    def get_all_artist(self) -> list[Artist]:
        return DAO.get_all_artist()

    def get_all_genre(self) -> list[Genre]:
        return DAO.get_all_generi()


