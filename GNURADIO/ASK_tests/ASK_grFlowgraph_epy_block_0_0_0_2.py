"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


import numpy as np
from gnuradio import gr

class float_display_block(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Float Display Block",
            in_sig=[np.float32],
            out_sig=None)
        self.item_counter = 0  # Initialize item counter

    def work(self, input_items, output_items):
        for i, val in enumerate(input_items[0]):  
            print(f"1.Float[{i}]: {val:.4f}")
            self.item_counter += 1 
        print(f"Total items printed: {self.item_counter}")
        return len(input_items[0])  # Consume all input items
