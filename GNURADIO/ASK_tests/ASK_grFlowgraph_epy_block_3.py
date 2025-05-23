"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class tag_delay_block(gr.sync_block):
    def __init__(self, delay_samples = 1):
        gr.sync_block.__init__(self,
            name="tag_delay_block",
            in_sig=[np.uint8],
            out_sig=[np.uint8])
        self.delay_samples = delay_samples

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        n = len(in0)

        # Copy samples
        for i in range(n):
            out0[i] = in0[i]


        tags = self.get_tags_in_range(0, self.nitems_read(0), self.nitems_read(0) + n)

        
        for tag in tags:
            print("tag.key=",tag.key)
            key = pmt.symbol_to_string(tag.key)
            if key in ['packet_start', 'packet_end']: 
                relative_offset = tag.offset - self.nitems_read(0)
                new_offset = self.nitems_written(0) + relative_offset
                output_sample_index = (new_offset + self.delay_samples)
                print(output_sample_index)
                self.add_item_tag(0, output_sample_index, tag.key, tag.value)

        #self.consume(0, n)
        return n