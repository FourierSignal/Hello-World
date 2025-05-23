#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: qpsk_rrc_rolloff
# Author: Barry Duggan
# GNU Radio version: 3.10.11.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import sip
import threading



class qpsk_rrc_rolloff(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "qpsk_rrc_rolloff", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("qpsk_rrc_rolloff")
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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_rrc_rolloff")

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
        self.samp_rate = samp_rate = 32000
        self.qpsk = qpsk = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.excess_bw = excess_bw = 0.35

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            'QT GUI Plot', #name
            5,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['0.1', '0.22', '0.35', '0.5', '1.0',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(5):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.digital_constellation_modulator_0_1 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.35,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_0_0_0_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=1.0,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_0_0_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.5,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_0_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.22,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=0.1,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 256, 10000))), True)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.digital_constellation_modulator_0_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.digital_constellation_modulator_0_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.digital_constellation_modulator_0_0_0, 0), (self.qtgui_freq_sink_x_0, 3))
        self.connect((self.digital_constellation_modulator_0_0_0_0, 0), (self.qtgui_freq_sink_x_0, 4))
        self.connect((self.digital_constellation_modulator_0_1, 0), (self.qtgui_freq_sink_x_0, 2))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "qpsk_rrc_rolloff")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw




def main(top_block_cls=qpsk_rrc_rolloff, options=None):

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
