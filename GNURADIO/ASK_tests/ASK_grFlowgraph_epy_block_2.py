"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import numpy as np
from gnuradio import gr
import pmt

class extract_payload_block(gr.basic_block):
    def __init__(self, postamble_pattern=None):
        gr.basic_block.__init__(
            self,
            name="extract_payload_block",
            in_sig=[np.uint8],   # unpacked bits: 0 or 1
            out_sig=[np.uint8]   # output same type
        )
        self.in_payload = False
        self.buffer = []

        # Ensure postamble_pattern is a numpy array or list
        self.postamble_pattern = postamble_pattern




    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        nread = self.nitems_read(0)

        tags = self.get_tags_in_window(0, 0, len(in0))
        tag_offsets = {tag.offset - nread: tag for tag in tags}

        i = 0
        packet_start_idx = None
        packet_end_idx = None

        # Step 1: Detect start and end tags (packet_start and packet_end)
        while i < len(in0):
            if i in tag_offsets and tag_offsets[i].key == pmt.intern("packet_start"):
                self.in_payload = True
                self.buffer.clear()
                packet_start_idx = i

            if i in tag_offsets and tag_offsets[i].key == pmt.intern("packet_end"):
                packet_end_idx = i
                if self.in_payload:
                    self.in_payload = False
                    break  # Stop once packet_end is found

            if self.in_payload:
                self.buffer.append(in0[i])

            i += 1

        print("packet_end_idx=",packet_end_idx)

        if not isinstance(self.postamble_pattern, (int, list, np.ndarray)):
            print(f"Error: postamble_pattern has incorrect type: {type(self.postamble_pattern)}")
            return -1

        # Step 2: If packet_end found, remove postamble
        if packet_end_idx is not None:
            # Check and remove postamble before packet_end
            payload_end_idx = self._remove_postamble(packet_end_idx)
            self.buffer = self.buffer[:payload_end_idx]

        # Step 3: Output the extracted payload (without postamble)
        num_to_output = min(len(out), len(self.buffer))
        out[:num_to_output] = self.buffer[:num_to_output]
        self.buffer = self.buffer[num_to_output:]

        self.consume(0, i)
        return num_to_output

    def _remove_postamble(self, packet_end_idx):
        """Detect and remove postamble before the packet_end tag"""

                # --- Normalize postamble_pattern to a list of ints ---

        if isinstance(postamble_pattern, int):

            postamble_pattern = [postamble_pattern]

        elif isinstance(postamble_pattern, np.ndarray):

            postamble_pattern = postamble_pattern.tolist()

        elif not isinstance(postamble_pattern, list):

            raise TypeError("postamble_pattern must be int, list, or numpy array")

        self.postamble_pattern = np.array(postamble_pattern, dtype=np.uint8) 

        print("self.postamble_pattern",self.postamble_pattern,type(self.postamble_pattern))


        print( type(self.postamble_pattern), type(self.buffer) )
        if self.postamble_pattern is not None and len(self.postamble_pattern) > 0:
            # Try to detect the postamble pattern before the packet_end
            postamble_len = len(self.postamble_pattern)
            end_idx = len(self.buffer)

            # Search for the postamble pattern before the packet_end in the buffer
            for j in range(end_idx - postamble_len, end_idx):
                if self.buffer[j:j + postamble_len] == self.postamble_pattern:
                    return j  # Trim the buffer at the point postamble starts

        return len(self.buffer)  # No postamble detected, return full buffer length


