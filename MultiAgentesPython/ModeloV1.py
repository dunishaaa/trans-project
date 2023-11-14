from mesa import Agent, Model
from mesa.time import BaseScheduler, SimultaneousActivation, StagedActivation
from mesa.space import MultiGrid



class MapModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.steps = 0
        self.lol1 = [[(4,7),(4,8)],[(4,16),(4,17)], [(19,3),(19,1),(19,2)], [(13,20),(13,21)],[(19,20),(19,21)]]
        self.lol2 = [[(1,9),(2,9),(3,9)],[(1,18),(2,18),(3,18)],[(14,22),(15,22)],[(20,22),(21,22)],[(20,4),(21,4)],[(24,7),(25,7),(26,7)]]

        self.create_building((4, 4), (7, 6), [(6, 6)])
        self.create_building((4, 9), (7, 13), [(4, 10), (6, 13)])
        self.create_building((4, 18), (13, 19), [(5, 19), (12, 18)])
        self.create_building((4, 22), (13, 23), [(6, 22), (11, 23)])
        self.create_building((10, 4), (13, 13), [
                             (11, 4), (13, 8), (10, 11), (12, 13)])
        self.create_building((18, 4), (19, 7), [(19, 4)])
        self.create_building((22, 4), (23, 7), [(22, 7)])
        self.create_building((18, 10), (23, 13), [(22, 10), (20, 13)])
        self.create_building((18, 18), (19, 19), [(19, 17)])
        self.create_building((22, 18), (23, 19), [])
        self.create_building((22, 22), (23, 23), [(23, 22)])
        self.create_building((18, 22), (19, 23), [])
        
        #Glorieta
        self.create_building((15, 15), (16, 16), [])
        
        #Semaforos
        self.create_traffic(self.lol1)
        self.create_traffic(self.lol2)
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
    
    def manage_traffic(self, loc, num_steps,color):
        for i in loc:
            for j in i:
                check_cell = self.grid.get_cell_list_contents(j)
                for value in check_cell:
                    if type(value) is Traffic_light:
                        if color == 0:
                            value.color = color
                        elif color == 1:
                            value.color = color
                        elif color == 2:
                            value.color = color
                        else:
                            value.color = color
                
    def step(self):
        self.steps += 1
        
        if self.steps <= 10:
            self.manage_traffic(self.lol1, self.steps, 0)
            self.manage_traffic(self.lol2, self.steps,2)
        elif self.steps < 15 and self.steps > 10:
            self.manage_traffic(self.lol1, self.steps, 1)
            self.manage_traffic(self.lol2, self.steps,2)
        elif self.steps >= 15 and self.steps <= 25:
            self.manage_traffic(self.lol1, self.steps, 2)
            self.manage_traffic(self.lol2, self.steps,0)
        elif self.steps > 25 and self.steps <= 30:
            self.manage_traffic(self.lol1, self.steps, 2)
            self.manage_traffic(self.lol2, self.steps,1)
        else:
            self.manage_traffic(self.lol1, self.steps, 0)
            self.manage_traffic(self.lol2, self.steps,2)
            self.steps = 0
        
        
        
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
    
