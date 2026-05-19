import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # value from the user
        self.genere = None


    def fillDDGenre(self):
        for g in self._model.get_all_genre():
            self._view._ddGenre.options.append(
                ft.dropdown.Option( key = g.Name , data = g, on_click = self.take_genere)
        )

    def handleCreaGrafo(self, e):
        pass

    def handleCreaGrafo(self,e):
        pass

    def handleCammino(self,e):
        pass

    def take_genere(self, e):
        self.genere = e.control.data
        print(self.genere)
