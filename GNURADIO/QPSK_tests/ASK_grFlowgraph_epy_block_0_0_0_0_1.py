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
            name="Byte + ASCII Display Block",
            in_sig=[np.uint8],
            out_sig=None)
        self.item_counter = 0  # Initialize item counter

    def work(self, input_items, output_items):
        data = input_items[0]
        for i, byte_val in enumerate(data):
            try:
                ascii_char = chr(byte_val) if 32 <= byte_val <= 126 else '.'
            except:
                ascii_char = '?'
            print(f"[{i}] Byte: {byte_val}, ASCII: '{ascii_char}'")
            self.item_counter += 1
        print(f"Total items printed: {self.item_counter}")
        return len(data)  # Consume all input items
