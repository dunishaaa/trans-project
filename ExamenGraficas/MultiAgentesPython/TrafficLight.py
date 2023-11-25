from mesa import Agent

class TrafficLight(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 0 = verde | 1 = amarillo | 2 = Rojo
        self.color = 1
