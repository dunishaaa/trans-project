from mesa import Agent 
from abc import abstractmethod 
from queue import Queue

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


class Street(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        self.direccion = 1

def get_direction(prev_pos, new_pos):
    #print(f"{prev_pos=}")
    #print(f"{new_pos=}")
    x1,y1 = prev_pos
    x2,y2 = new_pos 
    if x2 > x1: # der
        return 2
    elif x2 < x1: # izq
        return 3
    elif y2 > y1:
        return 0
    else:
        return 1

class Vehicle(Agent):
    def __init__(self, unique_id, model, position, destiny, direction):
        super().__init__(unique_id, model)
        self.show = True 
        self.position = position
        self.destiny = destiny
        self.direction = direction
        self.path = Queue() 
    
    
        
    def get_neighbors(self, pos):
        curr_cel = self.model.grid.get_cell_list_contents(pos)
        curr_street_dir = 1
        for elem in curr_cel:
            if type(elem) is Street:
                curr_street_dir = elem.direccion
        x,y = pos
        possible_steps = []        
        # 0 = arriba | 1 = abajo | 2 = derecha | 3 = izquierda
        if curr_street_dir == 0:
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
        width = self.model.grid.width
        heigth = self.model.grid.height
        valid_steps = [(px, py) for px,py in possible_steps
                       if px >= 0 and  px < width and
                       py >= 0 and py < heigth]
        street_steps = []
        for position in valid_steps:
            cell = self.model.grid.get_cell_list_contents(position)
            for value in cell:
                if type(value) is Street:
                    street_steps.append((position))
                    break

        return tuple(street_steps)

    def move(self):
        if not self.path.empty():
            new_position = self.path.get()
            self.model.grid.move_agent(self, new_position)
        else:
            self.show = False

    @abstractmethod
    def get_path(self):
        ...
    
class Car(Vehicle):
    def __init__(self, unique_id, model, position, destiny, direction):
        super().__init__(unique_id, model, position, destiny, direction)

    def get_path(self):
#        print(f"{self.position=}")
#        print(f"{self.destiny=}")
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

    def restore_path(self, path):
        x, y = self.destiny
        restored_path = [(x, y)]

        while path[x][y] != (-1, -1):
            x, y = path[x][y]
            restored_path.append((x, y))

        path_steps = restored_path[::-1]
        print(f"{path_steps=}")
        for step in path_steps:
            self.path.put(step)
        #self.path.get()
    
    
    def step(self):
        self.move()
    
    def advance(self):
        print("", end="")


