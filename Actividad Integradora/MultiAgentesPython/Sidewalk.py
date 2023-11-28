from mesa import Agent
class Sidewalk(Agent):
    # Class that models the building
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.direccion = 4