from mesa import Agent 
from abc import abstractmethod
from queue import Queue
from TrafficLight import TrafficLight
from Crosswalk import Crosswalk
from Sidewalk import Sidewalk
import Car

class Pedestrians(Agent):
    def __init__(self, unique_id, model, position, destiny) -> None:
        super().__init__(unique_id, model)
        self.show = True 
        self.position = position
        self.destiny = destiny
        self.path = Queue()
        self.pasito_a_pasito = 0
    
    
    def prune_neighbors(self, possible_steps):
        width = self.model.grid.width
        heigth = self.model.grid.height
        valid_steps = [(px, py) for px,py in possible_steps
                       if px >= 0 and  px < width and
                       py >= 0 and py < heigth]
        street_steps = []
        for position in valid_steps:
            cell = self.model.grid.get_cell_list_contents(position)
            for value in cell:
                if type(value) is Sidewalk or type(value) is Crosswalk:
                    street_steps.append((position))
                    break
        return tuple(street_steps)
                
    def get_neighbors(self, pos):
        curr_cel = self.model.grid.get_cell_list_contents(pos)
        curr_street_dir = None
        for elem in curr_cel:
            if type(elem) is Sidewalk:
                curr_street_dir = elem.direccion
            if type(elem) is Crosswalk:
                curr_street_dir = elem.direccion
        x,y = pos
        possible_steps = []       
        # 4 == any direction
        
        possible_steps.append((x, y+1))    
        possible_steps.append((x, y-1))
        possible_steps.append((x+1, y))    
        possible_steps.append((x-1, y))
    
        return self.prune_neighbors(possible_steps)

    def restore_path(self, path) -> None:
        x, y = self.destiny
        restored_path = [(x, y)]

        while path[x][y] != (-1, -1):
            x, y = path[x][y]
            restored_path.append((x, y))

        path_steps = restored_path[::-1]
        #print(f"{path_steps=}")
        for step in path_steps:
            self.path.put(step)

    
    def move(self) -> None:
    
        if not self.path.empty():
            if self.position == self.path.queue[0]:
                self.path.get()
            new_position = self.path.queue[0]

            #print(f"{new_position}")
            # print(f"{self.path.queue[1]}")
            next_cell = self.model.grid.get_cell_list_contents(new_position)
            trafficLight = None
            crosswalk = None
            banquetita = None
            CarNext = None

            for elem in next_cell:
                if type(elem) is TrafficLight:
                    trafficLight = elem
                if type(elem) is Crosswalk:
                    crosswalk = elem
                if type(elem) is Sidewalk:
                    banquetita = elem
                    self.direccion = elem.direccion
                if type(elem) is Car.Car:
                    CarNext = elem
                    
            if trafficLight:
                # 0 = verde | 1 = amarillo | 2 = Rojo
                if trafficLight.color == 1 or trafficLight.color == 2:
                    self.model.grid.move_agent(self, new_position)
                    self.path.get()

            # elif banquetita:
            #     self.model.grid.move_agent(self, new_position)
            #     self.path.get()
            elif CarNext is None:
                self.model.grid.move_agent(self, new_position)
                self.path.get()
        else:
            self.show = False

    def get_path(self) -> None:
        width = self.model.grid.width
        heigth = self.model.grid.height
        visited = [[False for _ in range(heigth)] for _ in range(width)]
        path = [[(-1,-1) for _ in range(heigth)] for _ in range(width)]
        q = Queue()
        q.put(self.position)
        x,y = self.position
        visited[x][y] = True
        while not q.empty():
            x, y= q.get()
            possible_steps = self.get_neighbors((x, y))
            for to_x, to_y in possible_steps:
                if not visited[to_x][to_y]:
                    path[to_x][to_y] = (x,y)
                    visited[to_x][to_y] = True
                    q.put((to_x, to_y))

        self.restore_path(path)
        
    def step(self) -> None:
        if self.pasito_a_pasito > 4: 
            self.move()
            self.pasito_a_pasito = 0
        else:
            self.pasito_a_pasito += 1

    def advance(self) -> None:
        print("", end="")

    