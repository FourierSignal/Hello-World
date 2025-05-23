#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: QPSK
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from gnuradio import blocks
import numpy
from gnuradio import channels
from gnuradio.filter import firdes
from gnuradio import digital
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



class qpsk_simulation1(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "QPSK", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("QPSK")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_simulation1")

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
        self.sps = sps = 4
        self.nfilts = nfilts = 32
        self.timing_loop_bw = timing_loop_bw = 62.8e-3
        self.time_offset = time_offset = 1
        self.samp_rate = samp_rate = 32000
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 11*sps*nfilts)
        self.qpsk_constellation_0 = qpsk_constellation_0 = digital.constellation_qpsk().base()
        self.qpsk_constellation_0.set_npwr(1.0)
        self.noise_voltage = noise_voltage = 0
        self.freq_offset = freq_offset = 0

        ##################################################
        # Blocks
        ##################################################

        self._timing_loop_bw_range = qtgui.Range(0, 100, 1, 62.8e-3, 200)
        self._timing_loop_bw_win = qtgui.RangeWidget(self._timing_loop_bw_range, self.set_timing_loop_bw, "'timing_loop_bw'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._timing_loop_bw_win)
        self._time_offset_range = qtgui.Range(0, 1, 1e-5, 1, 200)
        self._time_offset_win = qtgui.RangeWidget(self._time_offset_range, self.set_time_offset, "'time_offset'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._time_offset_win)
        self._noise_voltage_range = qtgui.Range(0, 1, 1e-3, 0, 200)
        self._noise_voltage_win = qtgui.RangeWidget(self._noise_voltage_range, self.set_noise_voltage, "'noise_voltage'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._noise_voltage_win)
        self._freq_offset_range = qtgui.Range(0, 0.001, 0.00001, 0, 200)
        self._freq_offset_win = qtgui.RangeWidget(self._freq_offset_range, self.set_freq_offset, "'freq_offset'", "slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._freq_offset_win)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            1024, #size
            "channel i/p", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_1.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(True)
        self.qtgui_const_sink_x_0_1.enable_grid(True)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_1_win)
        self.qtgui_const_sink_x_0_0_0 = qtgui.const_sink_c(
            1024, #size
            "SyncBlockO/P", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0_0.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_0_win)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "channel o/p", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_0.enable_grid(True)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_0_win)
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(4, timing_loop_bw, rrc_taps, nfilts, (nfilts/2), 1.0, 1)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk_constellation_0,
            differential=False,
            samples_per_symbol=4,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.channels_channel_model_0 = channels.channel_model(
            noise_voltage=noise_voltage,
            frequency_offset=freq_offset,
            epsilon=time_offset,
            taps=[1],
            noise_seed=0,
            block_tags=False)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 1000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.channels_channel_model_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.channels_channel_model_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.channels_channel_model_0, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.qtgui_const_sink_x_0_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_simulation1")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_timing_loop_bw(self):
        return self.timing_loop_bw

    def set_timing_loop_bw(self, timing_loop_bw):
        self.timing_loop_bw = timing_loop_bw
        self.digital_pfb_clock_sync_xxx_0.set_loop_bandwidth(self.timing_loop_bw)

    def get_time_offset(self):
        return self.time_offset

    def set_time_offset(self, time_offset):
        self.time_offset = time_offset
        self.channels_channel_model_0.set_timing_offset(self.time_offset)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps(self.rrc_taps)

    def get_qpsk_constellation_0(self):
        return self.qpsk_constellation_0

    def set_qpsk_constellation_0(self, qpsk_constellation_0):
        self.qpsk_constellation_0 = qpsk_constellation_0

    def get_noise_voltage(self):
        return self.noise_voltage

    def set_noise_voltage(self, noise_voltage):
        self.noise_voltage = noise_voltage
        self.channels_channel_model_0.set_noise_voltage(self.noise_voltage)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self.channels_channel_model_0.set_frequency_offset(self.freq_offset)




def main(top_block_cls=qpsk_simulation1, options=None):

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
