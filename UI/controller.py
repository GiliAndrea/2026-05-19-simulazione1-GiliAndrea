import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # value from the user
        self.genre = None
        self.artist = None


    def fillDDGenre(self):
        for g in self._model.get_all_genre():
            self._view._ddGenre.options.append(
                ft.dropdown.Option( key = g.Name , data = g, on_click = self.take_genre)
        )

    def fillDDArtist(self):
        for a in self._model.get_all_artist_by_genre(self.genre.GenreId):
            self._view._ddArtist.options.append(
                ft.dropdown.Option( key = a.Name , data = a, on_click = self.take_artist)
        )

    def handleCreaGrafo(self, e):
        self._model.crea_grafo(self.genre.GenreId)
        # this is the part for the graphic result
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(value = "The graph was crated correctly", color="green")
        )

        self._view.txt_result.controls.append(
            ft.Text(value = f"The number of nodes is {self._model.get_number_nodes()}")
        )

        self._view.txt_result.controls.append(
            ft.Text(value = f"The number of edges is {self._model.get_number_edges()}")
        )

        best_artist = self._model.get_best_nodes()
        self._view.txt_result.controls.append(
            ft.Text(value = f"The best artist is {best_artist[0]} whit number of importance {best_artist[1]}",
                    color = "blue")
        )

        top_5_edges = self._model.get_top_5_edges_weight()
        self._view.txt_result.controls.append(
            ft.Text(value = "Top five edges:", color = "blue")
        )

        for e in top_5_edges:
            self._view.txt_result.controls.append(
                ft.Text(value = f"{e[0]} -> {e[1]}  weight: {e[2]["weight"]}")
            )

        self._view._ddArtist.disabled = False
        self._view._ddArtist.options.clear()
        self.fillDDArtist()
        self._view._btnTrovaCammino.disabled = False

        self._view.update_page()

    def handleCammino(self,e):
        if not self.artist:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text(value = "No artist selected" , color = "red")
            )
            self._view.update_page()
            return

        self._model.find_path(self.artist)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(value = f"Path with {self._model.length_path} Artist:")
        )

        for a in self._model.final_path:
            self._view.txt_result.controls.append(
                ft.Text(value = f"{a}")
            )

        self._view.update_page()

    def take_genre(self, e):
        self.genre = e.control.data

    def take_artist(self, e):
        self.artist = e.control.data