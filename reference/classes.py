# request product info from user
# fetch product info from inventory
def request_product():
    return Product("cat", "cat", 1.0)

class Indentation:
    def __init__(self, coordinates: set):
        # a set of Squares that compose a continuous region
        # and are indented for a given product
        self.coords = coordinates

    # indentation is no longer present on mat
    def gone(self, switch_list: set):
        # see if majority of this indentation is no longer indented
        # via presence in switch_list
        switched = 0
        for coord in self.coords:
            if coord in switch_list:
                switched += 1

        if switched/len(self.coords) > 0.8:
            return True
        else:
            return False

    # given indentation is within this indentation
    def contains(self, switch_list: set):
        return switch_list in self.coords

class Product:
    def __init__(self, name: str, description: str, price: float):
        self.name = name
        self.description = description
        self.price = price

class Square:
    def __init__(self, indented: bool):
        self.indented = indented

    # fetch new resistance data
    def update(self):
        ...

class Board:
    def __init__(self):
        self.array = []
        self.placements = []  # a list of (product, indentation) placements
        self.recently_removed = []  # a list of Products
        self.recently_added = [] # a list of Indentations
        self.shopping_mode = True

        # initialize board state
        # 15 x 15 sensor array
        for i in range(15):
            row = []
            for i in range(15):
                square = Square(indented=False)
                row.append(square)
            self.array.append(row)

    # refresh board one square at a time
    def update(self):
        switched_on = 0
        switched_off = 0
        switch_list = set()
        for i in range(15):
            for j in range(15):
                square = self.array[i][j]
                before = square.indented
                square.update()
                after = square.indented
                if before != after:
                    switch_list.add(square)

                    # detect what kind of change this is
                    if before and not after:
                        switched_off += 1
                    if after and not before:
                        switched_on += 1
        if len(switch_list) > 0:
            if switched_on > switched_off:
                removing = False
            else:
                removing = True

            if self.shopping_mode:
                if removing:
                    past_indentations = []
                    # check all placements if still present
                    for product, indentation in self.placements:
                        if indentation.gone(switch_list):
                            past_indentations.append((product, indentation))

                    # remove if no longer placed
                    for product, indentation in past_indentations:
                        # record recently placed product in case user puts back
                        if len(self.recently_removed) > 9:
                            self.recently_removed.pop(0)
                        self.recently_removed.append(product)
                        self.placements.remove((product, indentation))
                else:  # adding, customer has put back a product
                    new_positive_indented = set([x for x in switch_list if x.indented])
                    new_placement = Indentation(new_positive_indented)
                    product = self.recently_removed.pop()
                    self.placements.append((product, new_placement))

            else:
                # handle detecting if is an adding or a removal
                # handle the fact that when placing things, the points of first contact may not be the full image(?)
                if self.is_new_placement(switch_list):
                    new_positive_indented = set([x for x in switch_list if x.indented])
                    new_placement = Indentation(new_positive_indented)
                    product = request_product()
                    self.placements.append((product, new_placement))

    # set mode to shopping
    def set_to_shopping(self):
        self.shopping_mode = True

    # set to stocking mode
    def set_to_stocking(self):
        self.shopping_mode = False

    def is_new_placement(self, new_indentation):
        for product, indentation in self.placements:
            if indentation.contains(new_indentation):
                return False
        return True

