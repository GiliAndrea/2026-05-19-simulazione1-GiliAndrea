import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # value from the user
        self.genre = None


    def fillDDGenre(self):
        for g in self._model.get_all_genre():
            self._view._ddGenre.options.append(
                ft.dropdown.Option( key = g.Name , data = g, on_click = self.take_genre)
        )

    def handleCreaGrafo(self, e):
        self._model.crea_grafo(self.genre.GenreId)
        # this is the part for the graphic result
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(value = "The graph was crated correctly", color="green")
        )

        self._view.txt_result.controls.append(
            ft.Text(value = f"The number of nodes is {self._model.get_number_nodes()}", color="blue")
        )

        self._view.txt_result.controls.append(
            ft.Text(value = f"The number of edges is {self._model.get_number_edges()}", color="blue")
        )

        best_artist = self._model.get_best_nodes()
        self._view.txt_result.controls.append(
            ft.Text(value = f"The best artist is ... whit number of importance ...")
        )

        top_5_edges = self._model.get_top_5_nodes_weight()
        self._view.txt_result.controls.append(
            ft.Text(value = "Top five edges:", color = "blue")
        )

        for e in top_5_edges:
            self._view.txt_result.controls.append(
                ft.Text(value = f"Artist {e[0]} - weight {e[1]}")
            )

        self._view.update_page()


    def handleCammino(self,e):
        pass

    def take_genre(self, e):
        self.genre = e.control.data
        print(self.genre)
