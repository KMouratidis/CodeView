# ############################## #
# DEFINE YOUR IMPORTS HERE.      #
# SOME MODULES ARE NOT AVAILABLE #
# ############################## #
import numpy as np
import pandas as pd


# ######################################## #
# DEFINE FUNCTIONS, CLASSES, OR OTHER HERE #
# ######################################## #

class MyModel:
    """Create a simple doubler model.

    Although you probably don't need to write documentation,
    you can. We suggest the Google style but anything goes.
    Remember:

        Documentation is like sex. When it's good it's great.
        When it's bad it's still better than nothing. -pdoc3

    Args:
        arg1 (int, float, str. list): A number that we can
                                      multiply by 2!

    Methods:
        print_args: Takes no arguments, returns nothing,
                    and just prints stuff.
    """

    def __init__(self, arg1):
        self.array = np.array([arg1, arg1])
        self.twice = arg1 * 2

    def print_args(self):
        print(self.array, self.twice)
        
        
        
        
        


def submission():
    # ####################################################### #
    # DON'T CHANGE THE NAME OR ARGUMENTS OF THIS FUNCTION !!! #
    # CODE THAT NEEDS TIME TO RUN, DOES COMPUTATIONS, OR      #
    # IS PART OF THE WORKFLOW SHOULD BE WRITTEN AND EXECUTED  #
    # HERE, WITHIN THE FUNCTION BODY.                         #
    # ####################################################### #
    mc3 = MyModel(3)
    mca = MyModel("A")

    # ############################################### #
    # YOU CAN PRINT FREELY, EITHER FOR DEBUG PURPOSES #
    # OR SIMPLY FOR SHARING INFORMATION WITH US.      #
    # ############################################### #
    mc3.print_args()
    mca.print_args()

    # ########################################## #
    # RETURN YOUR FINAL RESULTS AS A DICTIONARY. #
    # DON'T CHANGE THE KEYS!                     #
    # ########################################## #
    return {
        "Task_1_result": f"{mc3.array} ***** {mca.array}",
        "Task_2_result": 42 * 69 * 3.14,
        "Task_3_result": "To be filled by you...",
    }
