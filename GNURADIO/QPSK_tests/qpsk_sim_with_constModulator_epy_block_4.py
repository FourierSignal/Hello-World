"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr

class file_with_postamble(gr.sync_block):
    def __init__(self, filename='/tmp/sample.txt', postamble=0xEEFF1122):
        gr.sync_block.__init__(self,
            name="file_with_postamble",
            in_sig=None,
            out_sig=[np.uint8])

        # Convert integer postamble to byte list
        self.postamble = list(postamble.to_bytes((postamble.bit_length() + 7) // 8, byteorder='big'))

        try:
            with open(filename, 'rb') as f:
                raw = np.frombuffer(f.read(), dtype=np.uint8)
        except IOError:
            raw = np.array([], dtype=np.uint8)

        print("raw=",raw)
        # No bit unpacking, just concatenate bytes
        self.data = np.concatenate([raw, np.array(self.postamble, dtype=np.uint8)])
        self.offset = 0

    def work(self, input_items, output_items):
        out = output_items[0]
        n = min(len(out), len(self.data) - self.offset)
        if n > 0:
            out[:n] = self.data[self.offset:self.offset + n]
            self.offset += n
        return n

