"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt

class FramingPlusTagInserter(gr.basic_block):
    """
    A sync block that generates a framed packet by adding a preamble and postamble
    to the input bit stream and tags the start and end with 'packet_start' and 'packet_end'.
    """

    def __init__(self, preamble=0xAABBCCDD, postamble=0xEEFF1122):
        gr.basic_block.__init__(
            self,
            name="frame_generator",
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )

        self.preamble= list(preamble.to_bytes((preamble.bit_length() + 7) // 8, byteorder='big'))
        self.postamble = list(postamble.to_bytes((postamble.bit_length() + 7) // 8, byteorder='big'))

        self.state = 'preamble'
        self.preamble_index = 0
        self.payload = []
        self.payload_index = 0
        self.postamble_index = 0
        self.packet_start_tagged = False
        self.packet_end_tagged = False
        self.eof_detected = False
        self.transmission_ended = False
        print(self.preamble)

    def find_subsequence(self, data, pattern):
        for i in range(len(data) - len(pattern) + 1):
            if np.array_equal(data[i:i+len(pattern)], pattern):
                return i
        return -1  # Not found

    def general_work(self, input_items, output_items):
        inp = input_items[0]
        out = output_items[0]


        noutput_items = len(out)
        in0_length = len(inp)
        space_left_in_out = noutput_items
        produced = 0
        consumed = 0


        print("\n------>inp=",inp)

        print("in0_length=",in0_length,"noutput_items=",noutput_items)



        if in0_length ==0 and self.state == 'payload' and not self.eof_detected:
            self.eof_detected = True
            self.state = 'postamble'
            print("\n--Entered postamble state")

        if  self.state == 'postamble' and self.transmission_ended == False:

            while self.postamble_index < len(self.postamble):
                remaining_postamble = len(self.postamble) - self.postamble_index
                print("noutput_items=",noutput_items, remaining_postamble)
                to_copy = min(noutput_items - produced, remaining_postamble)
                print("to_copy=",to_copy)
                if to_copy == 0:
                    break
                print(self.postamble[self.postamble_index:self.postamble_index + to_copy])
                out[produced:produced + to_copy] = self.postamble[self.postamble_index:self.postamble_index + to_copy]
                self.postamble_index += to_copy

                if self.postamble_index == len(self.postamble):
                    self.transmission_ended = True
                
                produced += to_copy
                print("produced=",produced, to_copy)
                space_left_in_out = noutput_items - produced
                print("space_left_in_out=",space_left_in_out)
                if space_left_in_out == 0:
                    self.consume(0, 0)
                    return produced


        elif  self.state == 'postamble' and self.transmission_ended == True:
            return 0


        while  consumed < len(inp):

           if self.state == 'preamble':
                print(self.state)
                print("len(out)=",len(out))
                while self.preamble_index < len(self.preamble):

                    remaining_preamble = len(self.preamble) - self.preamble_index
                    print("noutput_items=",noutput_items, remaining_preamble)
                    to_copy = min(noutput_items - produced, remaining_preamble)
                    print("to_copy=",to_copy)
                    if to_copy == 0:
                        break
                    print(self.preamble[self.preamble_index:self.preamble_index + to_copy])
                    out[produced:produced + to_copy] = self.preamble[self.preamble_index:self.preamble_index + to_copy]
                    self.preamble_index += to_copy
                    produced += to_copy
                    print("produced=",produced, to_copy)
                    space_left_in_out = noutput_items - produced
                    print("space_left_in_out=",space_left_in_out)
                    self.consume(0, 0)
                    return produced


                if self.preamble_index >= len(self.preamble):
                    self.state = 'payload'
                    self.packet_start_tagged = False  # Reset for new frame
                    produced = 0

           elif self.state == 'payload':

                print(self.state)

                remaining_payload = len(inp) - consumed
                if remaining_payload == 0:
                    break
                to_copy = min(space_left_in_out, remaining_payload)
                print("to_copy=",to_copy,"consumed,produced=",consumed,produced)
                if not self.packet_start_tagged:
                    # Add tag at the start of payload
                    self.add_item_tag(0, self.nitems_written(0) + produced,
                                      pmt.intern("packet_start"), pmt.PMT_NIL)
                    self.packet_start_tagged = True

                print("will output->",inp[consumed:consumed + to_copy])


                if not self.packet_end_tagged:
                    data_slice = inp[consumed:consumed + to_copy]
                    match_index = self.find_subsequence(data_slice, self.postamble)
                    if match_index != -1:
                        tag_position = self.nitems_written(0) + consumed + match_index
                        # one extra bit to accomodate FIR filters tail loss i.e tag at 2nd bit of preamble 
                        self.add_item_tag(0, tag_position,pmt.intern('packet_end'),pmt.PMT_NIL)
                        self.packet_end_tagged = True





                out[produced:produced + to_copy] = inp[consumed:consumed + to_copy]
                self.payload.extend(inp[consumed:consumed + to_copy])
                consumed += to_copy
                produced += to_copy
                print("----->",consumed,produced)
                self.consume(0, consumed)
                return consumed

        print("in while,consumed= ",consumed)
