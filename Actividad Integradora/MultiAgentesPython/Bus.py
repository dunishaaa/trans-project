from mesa import Agent 
from BusStop import BusStop
from StreetBus import StreetBus

class Bus(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = None
        
    def move(self):
        cell = self.model.grid.get_cell_list_contents(self.pos)
        for value in cell:
            if type(value) is StreetBus:
                diretion = value.direccion
                if diretion == 0:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
                elif diretion == 1:
                    self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
                elif diretion == 2:
                    self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
                elif diretion == 3:
                    self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
                else:
                    print("Error")
            
        ...
        
    def step(self) -> None:
        self.move()
    
    def advance(self) -> None:
        print("", end="")