from mesa import Agent
class StreetBus(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        self.direccion = 1