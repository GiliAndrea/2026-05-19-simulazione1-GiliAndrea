from copy import deepcopy

import networkx as nx

from database.DAO import DAO
from model import artist
from model.Genre import Genre
from model.artist import Artist


class Model:
    def __init__(self):

        # these are things related to the graph
        self._grafo = nx.DiGraph()
        self.map_weight = None
        self.map_artist = None

        # these are things related to the recursive function
        self.final_path = None
        self.length_path = None


    def find_path(self, first_Artist: artist):
        self.length_path = 1
        self.final_path = [first_Artist]
        path = [first_Artist]
        successors = self._grafo.successors(path[-1])
        for s in successors:
            if s not in path:
                path.append(s)
                self.recursive_function(path)
                path.pop()

    def recursive_function(self, path: list[Artist]):
        if self.potential_successors(path[-1], path):
            if len(path) > self.length_path:
                self.length_path = len(path)
                self.final_path = deepcopy(path)
        else:
            successors = self._grafo.successors(path[-1])
            for s in successors:
                if s not in path and self._grafo.edges[path[-1], s]["weight"] > self._grafo.edges[path[-2], path[-1]]["weight"]:
                    path.append(s)
                    self.recursive_function(path)
                    path.pop()

    def potential_successors(self, artist: artist, path: list[Artist]):
        result = True
        successors = self._grafo.successors(artist)
        for s in successors:
            if s not in path and self._grafo.edges[path[-1], s]["weight"] > self._grafo.edges[path[-2], path[-1]]["weight"]:
                result = False
        return result


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
        for e in DAO.get_all_weight(genre):
            self.map_weight[e[0]] = e[1]

        # this is the part for the edges
        for e in DAO.get_all_edges(genre):
            weight = self.map_weight[e[0]] + self.map_weight[e[1]]
            if self.map_weight[e[0]] > self.map_weight[e[1]]:
                self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)
            if self.map_weight[e[1]] > self.map_weight[e[0]]:
                self._grafo.add_edge(self.map_artist[e[1]], self.map_artist[e[0]], weight=weight)
            if self.map_weight[e[0]] == self.map_weight[e[1]]:
                self._grafo.add_edge(self.map_artist[e[0]], self.map_artist[e[1]], weight=weight)
                self._grafo.add_edge(self.map_artist[e[1]], self.map_artist[e[0]], weight=weight)


    def get_number_nodes(self):
        return self._grafo.number_of_nodes()

    def get_number_edges(self):
        return self._grafo.number_of_edges()

    def get_best_nodes(self):
        values = []
        for n in self._grafo.nodes():
            value = [n, 0]
            for s in self._grafo.successors(n):
                value[1] += self._grafo.edges[n, s]["weight"]
            for p in self._grafo.predecessors(n):
                value[1] -= self._grafo.edges[p, n]["weight"]
            values.append(value)

        result = max(values, key=lambda x : x[1])
        return result

    def get_top_5_edges_weight(self):
        result = sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)[:5]
        return result

    def get_all_artist(self) -> list[Artist]:
        return DAO.get_all_artist()

    def get_all_genre(self) -> list[Genre]:
        return DAO.get_all_generi()

    def get_all_artist_by_genre(self, genre: int):
        return DAO.get_all_artist_genre(genre)