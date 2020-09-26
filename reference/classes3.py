import numpy as np
from db_utils import add_one_to_inventory, remove_one_from_inventory
from hardware_utils import fetch_conductance, read_RFID
from request_utils import what_did_customer_put_back, what_product_is_being_stocked

# numpy notes
# np.subtract(a, b) = a - b

# tests if the negative values in change matrix
# zero out all positive values in placement matrix
def should_remove_placement(placement_matrix, change_matrix):
    def basically_zeroed_out(before, neg_change):
        after = before + neg_change
        if after / before < 0.2:
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
        self.placements = []  # [(product_id, placement_matrix)]
        self.matrix = np.zeros((15, 15))
        self.active_user = None
        self.mode = "shopping"

        for i in range(15):
            for j in range(15):
                self.matrix[i][j] = fetch_conductance(i, j)

    def update(self):
        self.active_user = read_RFID()

        new_board_state = np.zeros((15, 15))

        for i in range(15):
            for j in range(15):
                new_board_state[i][j] = fetch_conductance(i, j)

        change_matrix = np.subtract(new_board_state, self.matrix)
        # subtract old from new
        # if there is a positive change, its a placement
        # if there is a negative change, its a removal

        # removal
        if change_matrix.sum() < 0:
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
            # customer put something back
            if self.mode == "shopping":
                if self.active_user:
                    product_id = what_did_customer_put_back(self.active_user)
                    if product_id:
                        self.placements.append((product_id, change_matrix))
                        add_one_to_inventory(product_id)
                    else:
                        # customer did not respond to request
                        print(f"ALERT: PRODUCT PUT BACK BY CUSTOMER {self.active_user} BUT NO RESPONSE")
                else:
                    print("ALERT: REMOVAL DURING SHOPPING MODE BUT NO CUSTOMER DETECTED BY RFID")

            # employee stocked a product
            else:
                product_id = what_product_is_being_stocked()
                self.placements.append((product_id, change_matrix))
                add_one_to_inventory(product_id)



