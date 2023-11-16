from mesa import Agent, Model
from mesa.time import SimultaneousActivation 
from mesa.space import MultiGrid
from Vehicle import *


class MapModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        self.steps = 0

        


        size = 1
        self.lol1 = [[(4*size, 7*size), (4*size, 8*size)], [(4*size, 16*size), (4*size, 17*size)], [(19*size, 3*size), (19*size,
                                                                                                                        1*size), (19*size, 2*size)], [(13*size, 20*size), (13*size, 21*size)], [(19*size, 20*size), (19*size, 21*size)]]
        self.lol2 = [[(1*size, 9*size), (2*size, 9*size), (3*size, 9*size)], [(1*size, 18*size), (2*size, 18*size), (3*size, 18*size)], [(14*size, 22*size), (15*size, 22*size)], [
            (20*size, 22*size), (21*size, 22*size)], [(20*size, 4*size), (21*size, 4*size)], [(24*size, 7*size), (25*size, 7*size), (26*size, 7*size)]]

        self.create_building(
            (4*size, 4*size), (7*size, 6*size), [(6*size, 6*size)])
        self.create_building((4*size, 9*size), (7*size, 13*size),
                             [(4*size, 10*size), (6*size, 13*size)])
        self.create_building((4*size, 18*size), (13*size, 19*size),
                             [(5*size, 19*size), (12*size, 18*size)])
        self.create_building((4*size, 22*size), (13*size, 23*size),
                             [(6*size, 22*size), (11*size, 23*size)])
        self.create_building((10*size, 4*size), (13*size, 13*size), [
                            (11*size, 4*size), (13*size, 8*size), (10*size, 11*size), (12*size, 13*size)])
        self.create_building(
            (18*size, 4*size), (19*size, 7*size), [(19*size, 4*size)])
        self.create_building(
            (22*size, 4*size), (23*size, 7*size), [(22*size, 7*size)])
        self.create_building((18*size, 10*size), (23*size, 13*size),
                             [(22*size, 10*size), (20*size, 13*size)])
        self.create_building((18*size, 18*size),
                             (19*size, 19*size), [(19*size, 17*size)])
        self.create_building((22*size, 18*size), (23*size, 19*size), [])
        self.create_building((22*size, 22*size),
                             (23*size, 23*size), [(23*size, 22*size)])
        self.create_building((18*size, 22*size), (19*size, 23*size), [])

        # Glorieta
        self.create_building((15*size, 15*size), (16*size, 16*size), [])

        # Semaforos
        self.create_traffic(self.lol1)
        self.create_traffic(self.lol2)

    # Calle
        # Bordes
        #   blanco      gris        rojo            magenta
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        self.create_street((4, 0), (23, 3), 2)
        self.create_street((24, 0), (27, 27), 0)
        self.create_street((4, 24), (23, 27), 3)
        self.create_street((0, 0), (3, 27), 1)
        # Dentro
        self.create_street((4, 14), (13, 15), 2)#
        self.create_street((8, 4), (9, 13), 1)#
        self.create_street((4,7),(7,8), 3)#
        self.create_street((4,16),(13,17),3)#
        self.create_street((4,20),(13,21),2)#
        self.create_street((14,4),(15,13), 1) #
        self.create_street((16,4),(17,13), 0) #
        self.create_street((18,8),(23,9),2) #
        self.create_street((20,4),(21,7),1) #
        self.create_street((18,14),(23,15),2)#
        self.create_street((18,16),(23,17),3)#
        self.create_street((20,18),(21,23),1)#

        self.create_street((22,20),(23,21),3)#
        self.create_street((14,18),(15,23),1)#

        self.create_street((16,18),(17,23),0)#
        self.create_street((18,20),(19,21),2)#
        
        #Glorieta
        self.create_street((14,17),(17,17),3)#
        self.create_street((14,14),(17,14),2)
        self.create_street((14,15),(14,16),1)
        self.create_street((17,15),(17,16),0)

        carAg = Car(1, self, (6,7), (12,14), 1)
        self.grid.place_agent(carAg, (6,7))
        self.schedule.add(carAg)
        carAg.get_path()
        
    def create_street(self, cell, last_cell, direccion):
        actual_cell = (0, 0)
        initial_x, initial_y = cell

        while actual_cell != last_cell:
            actual_cell = cell
            x, y = cell
            last_x, last_y = last_cell

            if (y <= last_y and x <= last_x):
                street = Street((actual_cell), self)
                street.direccion = direccion
                self.grid.place_agent(street, (actual_cell))
                cell = (x, y + 1)
            else:
                cell = (x + 1, initial_y)

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
                traffic = Traffic_light(i, self)
                self.grid.place_agent(traffic, (j))

    def manage_traffic(self, loc, num_steps, color):
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
            self.manage_traffic(self.lol2, self.steps, 2)
        elif self.steps < 15 and self.steps > 10:
            self.manage_traffic(self.lol1, self.steps, 1)
            self.manage_traffic(self.lol2, self.steps, 2)
        elif self.steps >= 15 and self.steps <= 25:
            self.manage_traffic(self.lol1, self.steps, 2)
            self.manage_traffic(self.lol2, self.steps, 0)
        elif self.steps > 25 and self.steps <= 30:
            self.manage_traffic(self.lol1, self.steps, 2)
            self.manage_traffic(self.lol2, self.steps, 1)
        else:
            self.manage_traffic(self.lol1, self.steps, 0)
            self.manage_traffic(self.lol2, self.steps, 2)
            self.steps = 0
        
        self.schedule.step()


