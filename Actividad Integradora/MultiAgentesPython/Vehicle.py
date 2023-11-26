from mesa import Agent 
from abc import abstractmethod
from queue import Queue
from Parking import Parking
from Street import Street
from TrafficLight import TrafficLight
import Car
import Parking
from Crosswalk import Crosswalk

class Vehicle(Agent):
    def __init__(self, unique_id, model, position, destiny) -> None:
        super().__init__(unique_id, model)
        self.show = True 
        self.position = position
        self.destiny = destiny
        self.direccion = None
        self.path = Queue() 
    
    @abstractmethod
    def prune_neighbors(self, possible_steps):
        ...

    @classmethod
    def get_direction(self, prev_pos, new_pos):
        #print(f"{prev_pos=}")
        #print(f"{new_pos=}")
        x1,y1 = prev_pos
        x2,y2 = new_pos 
        if x2 > x1: # der
            self.direccion = 2
            return 2
        
        elif x2 < x1: # izq
            self.direccion = 3
            return 3
        elif y2 > y1:
            self.direccion = 0
            return 0
        else:
            self.direccion = 1
            return 1
        
    def get_initial_position(self, position):
        x, y = position
        possible_steps = []
        possible_steps.append((x, y+1))    
        possible_steps.append((x, y-1))
        possible_steps.append((x+1, y))    
        possible_steps.append((x-1, y))
        for step in possible_steps:
            cell = self.model.grid.get_cell_list_contents(step)
            for value in cell:
                if type(value) is Street:
                    print(f"{self.get_direction(position, step)}")
                    return self.get_direction(position, step)
                
                
                
    def get_neighbors(self, pos):
        curr_cel = self.model.grid.get_cell_list_contents(pos)
        curr_street_dir = None
        parking = False
        for elem in curr_cel:
            if type(elem) is Street:
                curr_street_dir = elem.direccion
            if type(elem) is Parking.Parking:
                parking = True
        x,y = pos
        possible_steps = []        
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        if parking or curr_street_dir == 4:
            #print("adentro del if")
            possible_steps.append((x, y+1))    
            possible_steps.append((x, y-1))
            possible_steps.append((x+1, y))    
            possible_steps.append((x-1, y))
        elif curr_street_dir == 0:
            possible_steps.append((x, y+1))    
            possible_steps.append((x+1, y))    
            possible_steps.append((x-1, y))    
        elif curr_street_dir == 1:
            possible_steps.append((x, y-1))    
            possible_steps.append((x+1, y))    
            possible_steps.append((x-1, y))    
        elif curr_street_dir == 2:
            possible_steps.append((x+1, y))    
            possible_steps.append((x, y-1))    
            possible_steps.append((x, y+1))    
        else:
            possible_steps.append((x-1, y))    
            possible_steps.append((x, y-1))    
            possible_steps.append((x, y+1))    
  
            
        #print(f"get_neigh {possible_steps=}")

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
            print(f"{new_position}")
            # print(f"{self.path.queue[1]}")
            next_cell = self.model.grid.get_cell_list_contents(new_position)
            #print(f"{next_cell}")
            trafficLight = None
            carNext = None
            parkingNext = None
            crosswalk = None

            for elem in next_cell:
                if type(elem) is TrafficLight:
                    trafficLight = elem
                if type(elem) is Parking.Parking:
                    parkingNext = elem
                if type(elem) is Car.Car:
                    carNext = elem
                if type(elem) is Crosswalk:
                    crosswalk = elem
                if type(elem) is Street:
                    self.direccion = self.get_direction(self.position, new_position)


            if trafficLight:
                # 0 = verde | 1 = amarillo | 2 = Rojo
                #print(f"{trafficLight.color=}")
                if trafficLight.color == 0:
                    self.model.grid.move_agent(self, new_position)
                    self.path.get()
            elif carNext is None:
                self.model.grid.move_agent(self, new_position)
                self.path.get()
            elif carNext and parkingNext:
                self.model.grid.move_agent(self, new_position)
                self.path.get()
            elif crosswalk:
                ...
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
            #print(f"{x=}, {y=}, {possible_steps=}")
            for to_x, to_y in possible_steps:
                if not visited[to_x][to_y]:
                    path[to_x][to_y] = (x,y)
                    visited[to_x][to_y] = True
                    q.put((to_x, to_y))

        self.restore_path(path)

    