import networkx as nx

from database.DAO import DAO
from model.Genre import Genre
from model.artist import Artist


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.map_weight = None
        self.map_artist = None

    def crea_grafo(self, genre: int):
        self._grafo.clear()
        # this is the part for the nodes
        self._grafo.add_nodes_from(DAO.get_all_artist_genre(genre))
        # this part is regard the map of artist
        self.map_artist = {}
        for a in DAO.get_all_artist_genre(genre):
            self.map_artist[a.ArtistId] = a

        # this part is related to the edges' weight
        self.map_weight = {}
        for e in DAO.get_all_weight():
            self.map_weight[e[0]] = e[1]

        # this is the part for the edges
        for e in DAO.get_all_edges():
            if e[0] in self.map_artist.keys() and e[1] in self.map_artist.keys():
                if not self._grafo.has_edge(self.map_artist[e[0]], self.map_artist[e[1]]):
                    weight = self.map_weight[e[0]] + self.map_weight[e[1]]
                    if self.map_weight[e[0]] > self.map_weight[e[1]]:
                        self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)
                    if self.map_weight[e[1]] < self.map_weight[e[0]]:
                        self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)
                    if self.map_weight[e[0]] == self.map_weight[e[1]]:
                        self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)
                        self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)

    def get_number_nodes(self):
        return self._grafo.number_of_nodes()

    def get_number_edges(self):
        return self._grafo.number_of_edges()

    def get_best_nodes(self):
        pass

    def get_top_5_nodes_weight(self):
        result = []
        for n in self._grafo.nodes():
            if n.ArtistId in self.map_weight.keys():
                importance = self.map_weight[n.ArtistId]
            else:
                importance = 0
            result.append((n, importance))
        result.sort(key=lambda x: x[1], reverse=True)
        return result[0:5]

    def get_all_artist(self) -> list[Artist]:
        return DAO.get_all_artist()

    def get_all_genre(self) -> list[Genre]:
        return DAO.get_all_generi()

