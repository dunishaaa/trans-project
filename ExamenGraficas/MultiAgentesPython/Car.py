from Vehicle import Vehicle
from Parking import Parking
from Street import Street

class Car(Vehicle):
    def __init__(self, unique_id, model, position, destiny):
        super().__init__(unique_id, model, position, destiny)

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
                #print(f"{position=} - {type(value)=}")
                if type(value) is Street or type(value) is Parking:
                    street_steps.append((position))

        return tuple(street_steps)

    def step(self) -> None:
        self.move()
    
    def advance(self) -> None:
        print("", end="")

