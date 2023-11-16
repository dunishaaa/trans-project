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


class Vehicle(Agent):
    def __init__(self, unique_id, model, position, destiny):
        super().__init__(unique_id, model)
        self.show = True 
        self.position = position
        self.destiny = destiny
        self.direction = 1
        self.path = []
    
    def get_neighbors(self, pos):
        positions = self.model.grid.get_neighborhood(
            pos , moore=True, include_center=False
        )  # Get all neighbours

        possible_steps = [
                (px, py)
                for (px, py) in positions
                if abs(px - pos[0])+abs(py-pos[1]) <= 1 
            ]
        valid_steps = []        
        for position in possible_steps:
            cell = self.model.grid.get_cell_list_contents(position)
            if len(cell) == 1 and type(cell[0]) is Street:
                valid_steps.append((position))

        return tuple(possible_steps)

    @abstractmethod
    def get_path(self):
        ...
    @abstractmethod
    def move(self):
        ...
    
class Car(Vehicle):
    def __init__(self, unique_id, model, position, destiny):
        super().__init__(unique_id, model, position, destiny)

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
            #print(f"cur: {(x,y)}")
            #print(f"{possible_steps=}")
            for to_x, to_y in possible_steps:
                if not visited[to_x][to_y]:
                    path[to_x][to_y] = (x,y)
                    visited[to_x][to_y] = True
                    q.put((to_x, to_y))

        restored_path = self.restore_path(path)
        print(f"{restored_path}")
        return restored_path

    def restore_path(self, path):
        x, y = self.destiny
        restored_path = [(x, y)]

        while path[x][y] != (-1, -1):
            x, y = path[x][y]
            restored_path.append((x, y))

        return restored_path[::-1]

    
    def move(self):
        ...


