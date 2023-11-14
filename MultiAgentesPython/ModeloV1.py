from mesa import Agent, Model
from mesa.time import BaseScheduler, SimultaneousActivation, StagedActivation
from mesa.space import MultiGrid
# from time import sleep, time, process_time
# # import numpy as np
# # import random
# # import sys
# # import matplotlib.pyplot as plt


class MapModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.steps = 0
        self.lol1 = [[(5,8),(5,9)],[(5,17),(5,18)], [(20,1),(20,2),(20,3),(20,4)], [(14,21),(14,22)],[(20,21),(20,22)]]

        self.create_building((5, 5), (8, 7), [(7, 7)])
        self.create_building((5, 10), (8, 14), [(5, 11), (7, 14)])
        self.create_building((5, 19), (14, 20), [(6, 20), (13, 19)])
        self.create_building((5, 23), (14, 24), [(7, 23), (12, 24)])
        self.create_building((11, 5), (14, 14), [
                             (12, 5), (14, 9), (11, 12), (13, 14)])
        self.create_building((19, 5), (20, 8), [(20, 5)])
        self.create_building((23, 5), (24, 8), [(23, 8)])
        self.create_building((19, 11), (24, 14), [(23, 11), (21, 14)])
        self.create_building((19, 19), (20, 20), [(20, 20)])
        self.create_building((23, 19), (24, 20), [])
        self.create_building((23, 23), (24, 24), [(24, 23)])
        self.create_building((19, 23), (20, 24), [])
        
        #Glorieta
        self.create_building((16, 16), (17, 17), [])
        
        #Semaforos
        self.create_traffic(self.lol1)
        #self.manage_traffic(self.lol1, self.steps)

    def create_building(self, cell, last_cell, parking_list):
        # This function creates a new building, well I think so
        actual_cell = (0, 0)
        initial_x, initial_y = cell

        while actual_cell != last_cell:
            actual_cell = cell
            x, y = cell
            last_x, last_y = last_cell
            # check_cell = self.model.grid.get_cell_list_contents(actual_cell)

            if (y <= last_y and x <= last_x):
                building = Building((actual_cell), self)
                self.grid.place_agent(building, (actual_cell))
                cell = (x, y + 1)
            else:
                cell = (x + 1, initial_y)

        for i in parking_list:
            check_cell = self.grid.get_cell_list_contents(i)
            for value in check_cell:
                if type(value) is Building:
                    self.grid.remove_agent(value)
                    parking = Parking(i, self)
                    self.grid.place_agent(parking, i)
                    
                    
    def create_traffic(self, loc):
        for i in loc:
            for j in i:
                check_cell = self.grid.get_cell_list_contents(j)
                traffic =Traffic_light(i, self)
                self.grid.place_agent(traffic, (j))
    
    def manage_traffic(self, loc, num_steps):
        for i in loc:
            for j in i:
                check_cell = self.grid.get_cell_list_contents(j)
                for value in check_cell:
                    if type(value) is Traffic_light:
                        if self.steps <= 10:
                            value.color = 0
                        elif self.steps < 15 and self.steps > 10:
                            value.color = 1
                        elif self.steps >= 15 and self.steps <= 25:
                            value.color = 2
                        else:
                            value.color = 0
                            self.steps = 0
                
    def step(self):
        self.steps += 1
        self.manage_traffic(self.lol1, self.steps)
        
        
        



class Building(Agent):
    # Class that models the building
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)


class Parking(Agent):
    # Class that models the parking
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class Traffic_light(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 0 = verde | 1 = amarillo | 2 = Rojo
        self.color = 1
    
