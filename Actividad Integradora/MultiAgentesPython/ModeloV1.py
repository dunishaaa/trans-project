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
from Crosswalk import Crosswalk
from StreetBus import StreetBus
from BusStop import BusStop
from Bus import Bus


class MapModel(Model):
    def __init__(self, width, height, number_cars, number_buses):
        self.grid = MultiGrid(width, height, True)
        self.number_cars = number_cars
        self.number_buses = number_buses
        self.schedule = StagedActivation(self)
        self.running = True
        self.steps = 0
        self.current_id = 0
        size = 1
        self.parking_lots = [(7, 7), (5, 13), (7, 16), (6, 24), (14, 25), (7, 30), (12, 31), (14, 5), (
            16, 9), (15, 16), (13, 14), (25, 5), (30, 8), (30, 13), (28, 16), (25, 25), (31, 30)]

        self.lol1 = [[(4*size, 9*size), (4*size, 10*size)], [(4*size, 22*size), (4*size, 21*size)], [(25*size, 3*size), (25*size, 2*size)],
                     [(32*size, 10*size), (32*size, 11*size)
                      ], [(17*size, 27*size), (17*size, 28*size)],
                     [(26*size, 27*size), (26*size, 28*size)
                      ], [(23*size, 33*size), (23*size, 34*size)],
                     [(4*size, 33*size), (4*size, 34*size)], [(12*size, 3*size), (12*size, 2*size)]]

        self.lol2 = [[(2*size, 11*size), (3*size, 11*size)], [(2*size, 23*size), (3*size, 23*size)],
                     [(18*size, 29*size), (19*size, 29*size)
                      ], [(27*size, 29*size), (28*size, 29*size)],
                     [(27*size, 4*size), (28*size, 4*size)
                      ], [(33*size, 9*size), (34*size, 9*size)],
                     [(33*size, 23*size), (34*size, 23*size)]]

        self.crosswalk_list = [(1, 23), (2, 23), (3, 23), (1, 11), (2, 11), (3, 11), (4, 35), (4, 34), (
                                4, 33), (4, 28), (4, 27), (4, 22), (4, 21), (4, 19), (4, 18), (4, 10), (4, 9), (4, 3), (4, 2), (
                                4, 1),(10,17),(11,17),(10,8),(11,8),(12,1),(12,2),(12,3),(17,35),(17,34),(17,33),(17,28),(
                                17,27),(17,22),(17,21),(17,19),(17,18),(17,3),(17,2),(17,1),(18,29),(19,29),(21,29),(22 ,29),(18,17),(
                                19,17),(21,17),(22,17),(18,4),(19,4),(21,4),(22,4),(23,35),(23,34),(23,33),(26,28),(26,27),(26,3),(26,2),(
                                26,1),(27,29),(28,29),(27,23),(28,23),(27,4),(28,4),(32,28),(32,27),(32,22),(32,21),(32,19),(32,18),(32,11),(
                                32,10),(33,9),(34,9),(35,9),(33,23),(34,23),(35,23)]
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
        self.create_sidewalk((20*size, 4*size), (20*size, 17*size))
        self.create_sidewalk((4*size, 20*size), (17*size, 20*size))
        self.create_sidewalk((20*size, 23*size), (20*size, 32*size))
        self.create_sidewalk((23*size, 20*size), (32*size, 20*size))
        # # Semaforos
        self.create_traffic(self.lol1)
        self.create_traffic(self.lol2)

        # # Cruces peatonales
        self.create_crosswalk(self.crosswalk_list)

    # Calle
        # Bordes
        #   cafe          gris        rojo            magenta
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        self.create_street((4, 2), (32, 3), 2)
        self.create_sidewalk((0, 0), (36, 0))
        self.create_street((33, 2), (34, 34), 0)
        self.create_sidewalk((36, 1), (36, 36))
        self.create_street((4, 33), (32, 34), 3)
        self.create_sidewalk((0, 36), (35, 36))
        self.create_street((2, 2), (3, 34), 1)
        self.create_sidewalk((0, 1), (0, 35))

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

        self.create_street((23, 27), (26, 28), 2)
        self.create_street((21, 23), (22, 32), 0)

        self.create_street((18, 23), (19, 32), 1)
        self.create_street((29, 27), (32, 28), 3)

    # #     #Glorieta
        self.create_street((18, 22), (22, 22), 3)
        self.create_street((18, 18), (22, 18), 2)
        self.create_street((18, 19), (18, 21), 1)
        self.create_street((22, 19), (22, 21), 0)
        
    # #     #MetroBus
        self.create_streetbus((1,1),(1,35),1)
        self.create_streetbus((1,1),(35,1),2)
        self.create_streetbus((35,1),(35,35),0)
        self.create_streetbus((1,35),(35,35),3)
        self.bustops = [(0,23),(0,11),(12,0),(25,0),(36,9),(36,23),(23,36),(4,36)]
        self.create_busstop(self.bustops)
        
        
        self.spls = [(7, 8), (4, 13), (7, 17), (6, 23), (14, 26), (7, 29), (12, 32), (14, 4), (17, 9), (15, 17),
                     (12, 14), (25, 4), (29, 8), (30, 12), (28, 17), (26, 25), (32, 30)]

        
        self.create_pkl(self.spls)
        self.create_cars_in_lots()
        self.create_crosswalk(self.crosswalk_list)
        self.ubication((0,0),(36,36))

        self.create_buses()

        #     self.grid.place_agent(calle, i)
        
    def get_direction(self, cell):
        x,y = cell
        left = (x-1,y)
        right = (x+1,y)
        up = (x,y-1)
        down = (x,y+1)
        cell_content_left = self.grid.get_cell_list_contents(left)
        cell_content_right = self.grid.get_cell_list_contents(right)
        cell_content_up = self.grid.get_cell_list_contents(up)
        cell_content_down = self.grid.get_cell_list_contents(down)
        
        if Street in cell_content_left:
            return 3
        elif Street in cell_content_right:
            return 2    
        elif Street in cell_content_up: 
            return 0
        elif Street in cell_content_down:
            return 1
        
        
        
        
    def ubication(self, cell, last_cell):
        dict = {}
        dict["gridSize"] = (36, 36)
        dict["cars"] = []
        dict["metrobuses"] = []
        dict["pedestrians"] = []
        actual_cell = (0, 0)
        initial_x, initial_y = actual_cell
        
        while actual_cell != last_cell:
            actual_cell = cell
            x, y = cell
            last_x, last_y = last_cell
            if (y <= last_y and x <= last_x):
                cell_content = self.grid.get_cell_list_contents((x, y))
                for value in cell_content:
                    dic = {}
                    if type(value) is Car:
                        dic["id"] = value.unique_id
                        dic["x"] = x
                        dic["y"] = y
                        dict["cars"].append(dic)

                        
                cell = (x, y + 1)
            else:
                cell = (x + 1, initial_y)

        return dict
        
    
        
        
    def create_busstop(self, spls):
        for i in spls:
            busstop = BusStop(i, self)
            self.grid.place_agent(busstop, (i))

    def create_pkl(self, spls):
        for i in spls:
            calle = Street(i, self)
            calle.direccion = 4
            self.grid.place_agent(calle, (i))

    def create_crosswalk(self, splw):
        for i in splw:
            crosswalk = Crosswalk(i, self)
            self.grid.place_agent(crosswalk, (i))
              
    def create_cars_in_lots(self):
        pini = (2, 2)
        pdest = (31, 30)
        for i in range(self.number_cars):
            ini = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            dest = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            while ini == dest:
                dest = self.parking_lots[randint(0, len(self.parking_lots)-1)]
            x,y = ini

            carAg = Car(self.current_id, self, ini, dest)
            self.current_id += 1
            carAg.pos = ini
            self.grid.place_agent(carAg, ini)
            self.schedule.add(carAg)
            carAg.get_path()
            
    def create_buses(self):
        pini = (1,23)

        for i in range(self.number_buses):
            x,y = pini
            busAg = Bus(self.current_id, self)
            self.current_id += 1
            busAg.pos = pini
            self.grid.place_agent(busAg, pini)
            self.schedule.add(busAg)
            # self.schedule.add(busAg)

    
    def create_streetbus(self, cell, last_cell, direccion):
        actual_cell = (0, 0)
        initial_x, initial_y = cell

        while actual_cell != last_cell:
            actual_cell = cell
            x, y = cell
            last_x, last_y = last_cell

            if (y <= last_y and x <= last_x):
                street = StreetBus((actual_cell), self)
                street.direccion = direccion
                self.grid.place_agent(street, (actual_cell))
                cell = (x, y + 1)
            else:
                cell = (x + 1, initial_y)

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
            #cell_content = self.grid.get_cell_list_contents((x, y))
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
                    # self.parking_lots.append(i)
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
        self.ubication((0,0),(36,36))
        self.schedule.step()
        


if __name__ == "__main__":
    model = MapModel(37, 37, 10, 1)
    while model.running:
        model.step()
