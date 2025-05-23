"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""


import numpy as np
from gnuradio import gr

class byte_display_block(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Byte Display Block",
            in_sig=[np.uint8],
            out_sig=None)
        self.item_counter = 0  # Initialize item counter

    def work(self, input_items, output_items):
        for i, val in enumerate(input_items[0]):
            print(f"Byte[{i}]: {val:02X} ({val})")
            self.item_counter += 1
        print(f"Total bytes printed: {self.item_counter}")
        return len(input_items[0])  # Consume all input items