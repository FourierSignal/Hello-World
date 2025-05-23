"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr

class complex_display_block(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Complex Display Block",
            in_sig=[np.complex64],
            out_sig=None)
        self.item_counter = 0  # Initialize item counter

    def work(self, input_items, output_items):
        for i, val in enumerate(input_items[0]):
            print(f"1.Complex[{i}]: {val.real:.4f} + {val.imag:.4f}j")
            self.item_counter += 1
        print(f"Total items printed: {self.item_counter}")
        return len(input_items[0])  # Consume all input items

