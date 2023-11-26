from mesa import Agent 
from BusStop import BusStop
from StreetBus import StreetBus
from TrafficLight import TrafficLight
from Crosswalk import Crosswalk

class Bus(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.pos = None
        self.wait = 0
        self.wait4passengers = 0
        
    def wait4passengers(self):
        ...
        
    def check_traffic_ligh(self, cell):
        trafficLight = None
        car = None
        crosswalk = None
        busstop = None
        for value in cell:
            if type(value) is TrafficLight:
                trafficLight = value
            elif type(value) is Bus:
                car = value
            elif type(value) is Crosswalk:
                crosswalk = value
            elif type(value) is BusStop:
                busstop = value
            # elif type(value) is Crosswalk and :
            #     return True
        if trafficLight:
            if trafficLight.color == 1 or trafficLight.color == 2:
                return False
            else:
                return True
        elif car:
            return False
        elif crosswalk:
            if self.wait < 6:
                self.wait += 1
                return False
            else:
                self.wait = 0
                return True
        # elif busstop:
        #     if self.wait4passengers < 10:
        #         self.wait4passengers += 1
        #         return False
        #     else:
        #         self.wait4passengers = 0
        #         return True
        else:
            return True
            
        
    def move(self):
        cell = self.model.grid.get_cell_list_contents(self.pos)
        
        for value in cell:
            if type(value) is StreetBus:
                diretion = value.direccion
                if diretion == 0 and self.pos[1]+1 != 36:
                    next_cell = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] + 1))
                    if self.check_traffic_ligh(next_cell):
                        self.model.grid.move_agent(self, (self.pos[0], self.pos[1] + 1))
                elif diretion == 1 and self.pos[1]-1 != 0:
                    next_cell = self.model.grid.get_cell_list_contents((self.pos[0], self.pos[1] - 1))
                    if self.check_traffic_ligh(next_cell):
                        self.model.grid.move_agent(self, (self.pos[0], self.pos[1] - 1))
                elif diretion == 2 and self.pos[0]+1 != 36:
                    next_cell = self.model.grid.get_cell_list_contents((self.pos[0] + 1, self.pos[1]))
                    if self.check_traffic_ligh(next_cell):
                        self.model.grid.move_agent(self, (self.pos[0] + 1, self.pos[1]))
                elif diretion == 3 and self.pos[0]-1 != 0:
                    next_cell = self.model.grid.get_cell_list_contents((self.pos[0] - 1, self.pos[1]))
                    if self.check_traffic_ligh(next_cell):
                        self.model.grid.move_agent(self, (self.pos[0] - 1, self.pos[1]))
                else:
                    print("Error")
            
        ...
        
    def step(self) -> None:
        self.move()
    
    def advance(self) -> None:
        print("", end="")