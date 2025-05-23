#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class ASK_grFlowgraph(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ASK_grFlowgraph")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Variables
        ##################################################
        self.interpolation_factor = interpolation_factor = int(24)
        self.symbol_rate = symbol_rate = 2*50
        self.samp_rate = samp_rate = 192*1000
        self.ntaps = ntaps = int(interpolation_factor*11)
        self.nbits = nbits = 2
        self.filelength = filelength = (1+594+2)
        self.fc = fc = 32000*1
        self.excess_bw = excess_bw = 0.8
        self.Mhz = Mhz = 1000*1000
        self.total_symbols = total_symbols = ((filelength*8)/nbits)/10
        self.rrc_taps = rrc_taps = numpy.array ( firdes.root_raised_cosine(1,samp_rate,symbol_rate, excess_bw,ntaps ))
        self.qpsk_constellation = qpsk_constellation = digital.constellation_calcdist([-1-1j, -1+1j, 1+1j, 1-1j], [0, 1, 3, 2],
        4, 1, digital.constellation.AMPLITUDE_NORMALIZATION).base()
        self.qpsk_constellation.set_npwr(1.0)
        self.lpf_taps_upsampling = lpf_taps_upsampling = firdes.low_pass(1.0, samp_rate*64 , fc+300, 200, 1)
        self.lpf_taps_downsampling = lpf_taps_downsampling = firdes.low_pass(1.0, samp_rate*64 , samp_rate/(2*interpolation_factor), 200, 1)
        self.RF_BW = RF_BW = int(1.5*Mhz)
        self.N = N = 2**nbits

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.low_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (32*1000),
                (1*1000),
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (32*1000),
                (1*1000),
                window.WIN_HAMMING,
                6.76))
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccf(interpolation_factor, rrc_taps)
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccc(1, )
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_constellation_encoder_bc_0 = digital.constellation_encoder_bc(qpsk_constellation)
        self.blocks_throttle2_0_1 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_multiply_xx_2 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, fc, 1.414, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, fc, 1.414, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 1000, 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 100))), True)
        self.analog_noise_source_x_0 = analog.noise_source_f(analog.GR_GAUSSIAN, 1, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_encoder_bc_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_throttle2_0_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.digital_constellation_encoder_bc_0, 0), (self.blocks_throttle2_0_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_float_to_complex_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ASK_grFlowgraph")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_interpolation_factor(self):
        return self.interpolation_factor

    def set_interpolation_factor(self, interpolation_factor):
        self.interpolation_factor = interpolation_factor
        self.set_lpf_taps_downsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.samp_rate/(2*self.interpolation_factor), 200, 1))
        self.set_ntaps(int(self.interpolation_factor*11))

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_lpf_taps_downsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.samp_rate/(2*self.interpolation_factor), 200, 1))
        self.set_lpf_taps_upsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.fc+300, 200, 1))
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle2_0_1.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (32*1000), (1*1000), window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, (32*1000), (1*1000), window.WIN_HAMMING, 6.76))

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))

    def get_nbits(self):
        return self.nbits

    def set_nbits(self, nbits):
        self.nbits = nbits
        self.set_N(2**self.nbits)
        self.set_total_symbols(((self.filelength*8)/self.nbits)/10)

    def get_filelength(self):
        return self.filelength

    def set_filelength(self, filelength):
        self.filelength = filelength
        self.set_total_symbols(((self.filelength*8)/self.nbits)/10)

    def get_fc(self):
        return self.fc

    def set_fc(self, fc):
        self.fc = fc
        self.set_lpf_taps_upsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.fc+300, 200, 1))
        self.analog_sig_source_x_0_0.set_frequency(self.fc)
        self.analog_sig_source_x_0_0_0.set_frequency(self.fc)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))

    def get_Mhz(self):
        return self.Mhz

    def set_Mhz(self, Mhz):
        self.Mhz = Mhz
        self.set_RF_BW(int(1.5*self.Mhz))

    def get_total_symbols(self):
        return self.total_symbols

    def set_total_symbols(self, total_symbols):
        self.total_symbols = total_symbols

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.interp_fir_filter_xxx_0_0.set_taps(self.rrc_taps)

    def get_qpsk_constellation(self):
        return self.qpsk_constellation

    def set_qpsk_constellation(self, qpsk_constellation):
        self.qpsk_constellation = qpsk_constellation
        self.digital_constellation_encoder_bc_0.set_constellation(self.qpsk_constellation)

    def get_lpf_taps_upsampling(self):
        return self.lpf_taps_upsampling

    def set_lpf_taps_upsampling(self, lpf_taps_upsampling):
        self.lpf_taps_upsampling = lpf_taps_upsampling

    def get_lpf_taps_downsampling(self):
        return self.lpf_taps_downsampling

    def set_lpf_taps_downsampling(self, lpf_taps_downsampling):
        self.lpf_taps_downsampling = lpf_taps_downsampling

    def get_RF_BW(self):
        return self.RF_BW

    def set_RF_BW(self, RF_BW):
        self.RF_BW = RF_BW

    def get_N(self):
        return self.N

    def set_N(self, N):
        self.N = N




def main(top_block_cls=ASK_grFlowgraph, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
