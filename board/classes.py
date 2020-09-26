import numpy as np
from hardware.utils import fetch_conductance, read_rfid
from database.utils import *

# TODO: add print debug statements for all events

class DummyCounter:
    def __init__(self):
        self.value = 0

    def update(self):
        self.value += 1

# numpy notes
# np.subtract(a, b) = a - b

# tests if the negative values in change matrix
# zero out all positive values in placement matrix
def should_remove_placement(placement_matrix, change_matrix):
    def basically_zeroed_out(before, neg_change):
        after = before + neg_change
        if after / before < 0.4:
            return True
        else:
            return False

    pm_size = 0
    zeroed_out = 0
    for i in range(15):
        for j in range(15):
            pm_square = placement_matrix[i][j]
            if pm_square > 0:
                pm_size += 1
                # check if the change amounts to removing
                # > 80% of this square's value in placement
                if basically_zeroed_out(pm_square, change_matrix[i][j]):
                    zeroed_out += 1

    # check if > 50% of this placement's were zeroed out
    if zeroed_out / pm_size > 0.5:
        return True
    else:
        return False

class Board:
    def __init__(self):
        self.placements = []
        self.matrix = np.zeros((15, 15))
        self.mode = "shopping"

        # get initial hardware values
        for i in range(15):
            for j in range(15):
                self.matrix[i][j] = fetch_conductance(i, j)

    def update(self, debug):
        if debug:
            print("LOG: UPDATING BOARD")
        tap = read_rfid()
        if tap:
            print(f"LOG: RFID TAG {tap} DETECTED")
            # post to tap transactions database
            post_tap_transaction(tap)

        new_board_state = np.zeros((15, 15))

        for i in range(15):
            for j in range(15):
                new_board_state[i][j] = fetch_conductance(i, j)

        change_matrix = np.subtract(new_board_state, self.matrix)
        # subtract old from new
        # if there is a positive change, it is a placement
        # if there is a negative change, it is a removal

        # removal
        if change_matrix.sum() < 0:
            if debug:
                print("LOG: REMOVAL")
            # customer removed a product
            if self.mode == "shopping":
                customer_id = most_recent_customer()
                # customer tapped their bracelet before removing product
                if customer_id:
                    for i in range(len(self.placements)):
                        (product_id, placement) = self.placements[i]
                        if should_remove_placement(placement_matrix=placement,
                                                   change_matrix=change_matrix):
                            self.placements[i] = -1
                            remove_one_from_inventory(product_id)
                            add_one_to_cart(customer_id, product_id)

                    while -1 in self.placements:
                        self.placements.remove(-1)

                # product removed, customer did not tap their bracelet
                else:
                    for i in range(len(self.placements)):
                        (product_id, placement) = self.placements[i]
                        if should_remove_placement(placement_matrix=placement,
                                                   change_matrix=change_matrix):
                            self.placements[i] = -1
                            remove_one_from_inventory(product_id)
                            print(f"LOG: PRODUCT {product_id} REMOVED WITH NO CUSTOMER TAP DETECTED")

                    while -1 in self.placements:
                        self.placements.remove(-1)

            # employee removed a product
            else:
                for i in range(len(self.placements)):
                    (product_id, placement) = self.placements[i]
                    if should_remove_placement(placement_matrix=placement,
                                               change_matrix=change_matrix):
                        self.placements[i] = -1
                        remove_one_from_inventory(product_id)

                while -1 in self.placements:
                    self.placements.remove(-1)

        # placement
        elif change_matrix.sum() > 0:
            if debug:
                print("LOG: PLACEMENT")
            # customer put something back
            if self.mode == "shopping":
                product_id = most_recent_product_tap()
                customer_id = most_recent_customer()
                self.placements.append((product_id, change_matrix))
                add_one_to_inventory(product_id)
                remove_one_from_cart(customer_id, product_id)
            # employee stocked a product
            else:
                product_id = most_recent_product_tap()
                self.placements.append((product_id, change_matrix))
                add_one_to_inventory(product_id)

    def set_mode_to_shopping(self):
        self.mode = "shopping"

    def set_mode_to_stocking(self):
        self.mode = "stocking"