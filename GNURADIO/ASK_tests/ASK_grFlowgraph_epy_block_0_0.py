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

    def work(self, input_items, output_items):
        for byte in input_items[0]:
            print(f"Byte: {byte:08b}")  # Display as 8-bit binary
        return len(input_items[0])
