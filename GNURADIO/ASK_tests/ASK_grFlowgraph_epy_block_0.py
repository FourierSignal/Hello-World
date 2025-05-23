"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import ast

class ExtractPayLoad(gr.basic_block):
    """
    Forwards input data to output and simultaneously inspects and prints any tags.
    Input and output are streams of bit objects (numpy arrays of 0s and 1s).
    """

    def __init__(self):
        gr.basic_block.__init__(
            self,
            name='ExtractPayLoad',
            in_sig=[np.int8],  # Input is a stream of bits (0 or 1)
            out_sig=[np.int8]  # Output is a stream of bits (0 or 1)
        )
        self.payload_buffer = []
        self.in_payload = False

    def general_work(self, input_items, output_items):
        in_bits = input_items[0]
        out_bits = output_items[0]
        nread = self.nitems_read(0)
        tags = self.get_tags_in_window(0, 0, len(in_bits))
        tag_offsets = {tag.offset - nread: tag for tag in tags}

        # Directly forward the input to the output
        #out_bits[:] = in_bits
        print("----->in_bits=",in_bits)
        # Inspect and print tags present in the current input buffer
        for offset, tag in tag_offsets.items():
            key = pmt.to_python(tag.key)
            value = pmt.to_python(tag.value)
            print(f"Tag Debug: Offset: {tag.offset}, Relative Offset: {offset}, Key: {key}, Value: {value}")

        consumed = 0
        produced = 0
        i = 0


        # If packet_end is reached and entire buffer is not sent out in previous call, Flush the data is Remaining in Buffer.
        # Output remaining payload if it exists and we're no longer in payload collection
        if not self.in_payload and self.payload_buffer:
            output_len = min(len(self.payload_buffer), len(out_bits))
            #print("flushing:len(out_bits)=",len(out_bits), len(self.payload_buffer))
            if output_len > 0:
                out_bits[:output_len] = self.payload_buffer[:output_len]
                self.payload_buffer = self.payload_buffer[output_len:]  # remove outputted
                self.consume(0, 0)  # No new input consumed in this call
                return output_len

        while i < len(in_bits):
            if i in tag_offsets:
                tag = tag_offsets[i]
                key = pmt.to_python(tag.key)
                #print(key,"tag.offset=",tag.offset)

                if key == 'packet_start':
                    print("Detected packet_start.")
                    print(key,"tag.offset=",tag.offset)
                    self.in_payload = True
                    self.payload_buffer.clear()  

                elif key == 'packet_end':
                    if self.in_payload:
                        print("Detected packet_end.")
                        print(key,"tag.offset=",tag.offset)
                        self.in_payload = False
                        
                        #print("len(out_bits)=",len(out_bits), len(self.payload_buffer))
                        output_len = min(len(self.payload_buffer), len(out_bits)) # Output as much as fits
                        if output_len > 0:
                            produced = output_len
                            consumed = i+1
                            print("--->produced=",produced,[int(x) for x in self.payload_buffer],"consumed=",consumed)
                            out_bits[:output_len] = self.payload_buffer[:output_len]
                            self.payload_buffer = self.payload_buffer[output_len:]
                            self.consume(0, consumed) 
                            return produced
                        
            #print(i,in_bits[i]) 
            if self.in_payload == True:
                self.payload_buffer.append(in_bits[i])
            i += 1
            consumed = i
        
        print("produced=",produced,[int(x) for x in self.payload_buffer],"consumed=",consumed)
        self.consume(0,consumed)
        # The number of output items produced is the same as the number of input items consumed
        return produced
