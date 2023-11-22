from mesa import Agent, Model
from mesa.time import StagedActivation
from mesa.space import MultiGrid
from random import randint
from Car import Car
from Parking import Parking
from Street import Street
from TrafficLight import TrafficLight
from Building import Building
from Sidewalk import Sidewalk


class MapModel(Model):
    def __init__(self, width, height, number_cars):
        self.grid = MultiGrid(width, height, True)
        self.number_cars = number_cars
        self.schedule = StagedActivation(self)
        self.running = True
        self.steps = 0
        size = 1
        self.parking_lots = [(7, 7), (5, 13), (7, 16), (6, 24), (14, 25), (7, 30), (12, 31), (14, 5), (
            16, 9), (15, 16), (13, 14), (25, 5), (30, 8), (30, 13), (28, 16), (25, 25), (31, 30)]
        
        self.lol1 = [[(4*size, 9*size), (4*size, 10*size)], [(4*size, 22*size), (4*size, 21*size)], [(25*size, 3*size), (25*size,
                    1*size), (25*size, 2*size)], [(32*size, 10*size), (32*size, 11*size)], [(17*size, 27*size), (17*size, 28*size)], 
                     [(26*size, 27*size), (26*size, 28*size)], [(23*size, 33*size), (23*size, 34*size), (23*size, 35*size)],
                     [(4*size, 33*size), (4*size, 34*size), (4*size, 35*size)], [(12*size, 3*size), (12*size, 1*size), (12*size, 2*size)]]
        
        
        self.lol2 = [[(1*size, 11*size), (2*size, 11*size), (3*size, 11*size)], [(1*size, 23*size), (2*size, 23*size), (3*size, 23*size)], 
                     [(18*size, 29*size), (19*size, 29*size)], [(27*size, 29*size), (28*size, 29*size)],
                     [(27*size, 4*size), (28*size, 4*size)], [(33*size, 9*size), (34*size, 9*size), (35*size, 9*size)],
                     [(33*size, 23*size), (34*size, 23*size), (35*size, 23*size)]]
        # 1
        self.create_building(
            (5*size, 5*size), (8*size, 7*size), [(7*size, 7*size)])
        self.create_sidewalk((4*size, 4*size), (9*size, 8*size))
        # 2
        self.create_building((5*size, 12*size), (8*size, 16*size),
                             [(5*size, 13*size), (7*size, 16*size)])
        self.create_sidewalk((4*size, 11*size), (9*size, 17*size))
        # 3
        self.create_building((5*size, 24*size), (16*size, 25*size),
                             [(6*size, 24*size), (14*size, 25*size)])
        self.create_sidewalk((4*size, 23*size), (17*size, 26*size))
        # 4
        self.create_building((5*size, 30*size), (16*size, 31*size),
                             [(7*size, 30*size), (12*size, 31*size)])
        self.create_sidewalk((4*size, 29*size), (17*size, 32*size))
        # 5
        self.create_building((13*size, 5*size), (16*size, 16*size), [
                            (14*size, 5*size), (16*size, 9*size), (15*size, 16*size), (13*size, 14*size)])
        self.create_sidewalk((12*size, 4*size), (17*size, 17*size))
        # 6
        self.create_building(
            (24*size, 5*size), (25*size, 8*size), [(25*size, 5*size)])
        self.create_sidewalk((23*size, 4*size), (26*size, 9*size))
        # 7
        self.create_building(
            (30*size, 5*size), (31*size, 8*size), [(30*size, 8*size)])
        self.create_sidewalk((29*size, 4*size), (32*size, 9*size))
        # 8
        self.create_building((24*size, 13*size), (31*size, 16*size),
                             [(30*size, 13*size), (28*size, 16*size)])
        self.create_sidewalk((23*size, 12*size), (32*size, 17*size))
        # 9
        self.create_building((24*size, 24*size),
                             (25*size, 25*size), [(25*size, 25*size)])
        self.create_sidewalk((23*size, 23*size), (26*size, 26*size))
        # 10
        self.create_building((24*size, 30*size), (25*size, 31*size), [])
        self.create_sidewalk((23*size, 29*size), (26*size, 32*size))
        # 11
        self.create_building((30*size, 30*size),
                             (31*size, 31*size), [(31*size, 30*size)])
        self.create_sidewalk((29*size, 29*size), (32*size, 32*size))
        # 12
        self.create_building((30*size, 24*size),
                             (31*size, 25*size), [])
        self.create_sidewalk((29*size, 23*size), (32*size, 26*size))

        # Glorieta
        self.create_building((19*size, 19*size), (21*size, 21*size), [])

        # Camellon
        self.create_building((20*size, 4*size), (20*size, 17*size), [])
        self.create_building((4*size, 20*size), (17*size, 20*size), [])
        self.create_building((20*size, 23*size), (20*size, 32*size), [])
        self.create_building((23*size, 20*size), (32*size, 20*size), [])
        # # Semaforos
        self.create_traffic(self.lol1)
        self.create_traffic(self.lol2)

    # Calle
        # Bordes
        #   blanco      gris        rojo            magenta
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        self.create_street((4, 0), (32, 3), 2)
        self.create_street((33, 0), (36, 36), 0)
        self.create_street((4, 33), (32, 36), 3)
        self.create_street((0, 0), (3, 36), 1)
        # Dentro
        self.create_street((4, 18), (17, 19), 2)
        self.create_street((10, 4), (11, 17), 1)
        self.create_street((4, 9), (9, 10), 3)
        self.create_street((4, 21), (17, 22), 3)
        self.create_street((4, 27), (17, 28), 2)
        self.create_street((18, 4), (19, 17), 1)
        self.create_street((21, 4), (22, 17), 0)
        self.create_street((23, 10), (32, 11), 2)
        self.create_street((27, 4), (28, 9), 1)
        self.create_street((23, 18), (32, 19), 2)
        self.create_street((23, 21), (32, 22), 3)
        self.create_street((27, 23), (28, 32), 1)

        self.create_street((23, 27), (26, 28), 3)
        self.create_street((21, 23), (22, 32), 1)

        self.create_street((18, 23), (19, 32), 0)
        self.create_street((29, 27), (32, 28), 2)

    #     #Glorieta
        self.create_street((18, 22), (22, 22), 3)
        self.create_street((18, 18), (22, 18), 2)
        self.create_street((18, 19), (18, 21), 1)
        self.create_street((22, 19), (22, 21), 0)
        self.create_cars_in_lots()
    
    # self.parking_lots = [(7, 7), (5, 13), (7, 16), (6, 24), (14, 25), (7, 30), (12, 31), (14, 5), (
            #16, 9), (15, 16), (13, 14), (25, 5), (30, 8), (30, 13), (28, 16), (25, 25), (31, 30)]
        self.spls = [(7, 8), (4, 13), (7, 17), (6, 23), (14, 26), (7, 29), (12, 32), (14, 4), (17, 9), (15, 17), (12, 14), (26, 5), (25, 4), (29, 8),(30, 9), (30, 12), (28, 17), (25, 26),(26, 25), (32, 30)]

        # for i in self.spls:
        #     calle = Street(i, self)
        #     calle.direccion = 4
        self.create_pkl(self.spls)
        #     self.grid.place_agent(calle, i)
        
        
    def create_pkl(self, spls):
        for i in spls:
            print(i)
            calle = Street(i, self)
            #calle.direccion = 4
            self.grid.place_agent(calle,(i))
    def create_cars_in_lots(self):
        pini = (6, 6)
        pdest = (23, 22)
        for i in range(self.number_cars):
            ini = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            dest = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            while ini == dest:
                dest = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            carAg = Car(i, self, ini, dest)
            self.grid.place_agent(carAg, ini)
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

    def create_sidewalk(self, cell, last_cell):
        actual_cell = (0, 0)
        initial_x, initial_y = cell

        while actual_cell != last_cell:
            actual_cell = cell
            x, y = cell
            last_x, last_y = last_cell

            if (y <= last_y and x <= last_x):
                sidewalk = Sidewalk((actual_cell), self)
                self.grid.place_agent(sidewalk, (actual_cell))
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
                    #self.parking_lots.append(i)
                    self.grid.remove_agent(value)
                    parking = Parking(i, self)
                    self.grid.place_agent(parking, i)

    def create_traffic(self, loc):
        for i in loc:
            for j in i:
                check_cell = self.grid.get_cell_list_contents(j)
                traffic = TrafficLight(i, self)
                self.grid.place_agent(traffic, (j))

    def manage_traffic(self, loc, num_steps, color):
        for i in loc:
            for j in i:
                check_cell = self.grid.get_cell_list_contents(j)
                for value in check_cell:
                    if type(value) is TrafficLight:
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
        #print(self.parking_lots)
        self.schedule.step()
