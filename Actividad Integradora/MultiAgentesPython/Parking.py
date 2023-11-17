from mesa import Agent

class Parking(Agent):
    # Class that models the parking
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)