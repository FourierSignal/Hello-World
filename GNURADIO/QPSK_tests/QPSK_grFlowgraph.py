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
import ASK_grFlowgraph_epy_block_1 as epy_block_1  # embedded python block
import ASK_grFlowgraph_epy_block_4 as epy_block_4  # embedded python block
import numpy
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
        self.symbol_rate = symbol_rate = 2*50
        self.interpolation_factor = interpolation_factor = 256
        self.samp_rate = samp_rate = symbol_rate * interpolation_factor
        self.ntaps = ntaps = int(interpolation_factor*11)
        self.nbits = nbits = 2
        self.filelength = filelength = (1+594+2)
        self.fc = fc = 4000*1
        self.excess_bw = excess_bw = 0.8
        self.Mhz = Mhz = 1000*1000
        self.total_symbols = total_symbols = ((filelength*8)/nbits)/10
        self.rrc_taps = rrc_taps = numpy.array ( firdes.root_raised_cosine(1,samp_rate,symbol_rate, excess_bw,ntaps ))
        self.lpf_taps_upsampling = lpf_taps_upsampling = firdes.low_pass(1.0, samp_rate*64 , fc+300, 200, 1)
        self.lpf_taps_downsampling = lpf_taps_downsampling = firdes.low_pass(1.0, samp_rate*64 , samp_rate/(2*interpolation_factor), 200, 1)
        self.RF_BW = RF_BW = int(1.5*Mhz)
        self.N = N = 2**nbits

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_4_1_3 = qtgui.time_sink_c(
            (int((total_symbols/10) *256)), #size
            samp_rate, #samp_rate
            "QPSK before upsamling", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_3.set_update_time(10)
        self.qtgui_time_sink_x_4_1_3.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_3.enable_tags(True)
        self.qtgui_time_sink_x_4_1_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_3.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_3.enable_grid(True)
        self.qtgui_time_sink_x_4_1_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_3.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_3.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1_3.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_3.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_3_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_3.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_3_win)
        self.qtgui_time_sink_x_4_1_1 = qtgui.time_sink_c(
            int(total_symbols), #size
            symbol_rate , #samp_rate
            "symbols", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_1.set_update_time(1)
        self.qtgui_time_sink_x_4_1_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_1.enable_tags(False)
        self.qtgui_time_sink_x_4_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_1.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_1.enable_grid(True)
        self.qtgui_time_sink_x_4_1_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_1.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_1_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_1_win)
        self.qtgui_time_sink_x_4_1_0_0_1 = qtgui.time_sink_c(
            (int( total_symbols*256)), #size
            samp_rate, #samp_rate
            "mixer o/p after matched  ", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_0_0_1.set_update_time(10)
        self.qtgui_time_sink_x_4_1_0_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_0_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_0_0_1.enable_tags(False)
        self.qtgui_time_sink_x_4_1_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_0_0_1.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_0_0_1.enable_grid(True)
        self.qtgui_time_sink_x_4_1_0_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_0_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_0_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1_0_0_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_0_0_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_0_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_0_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_0_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_0_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_0_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_0_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_0_0_1_win)
        self.qtgui_time_sink_x_4_1_0_0_0 = qtgui.time_sink_c(
            int(total_symbols), #size
            samp_rate, #samp_rate
            "decimating FIR o/p Signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_0_0_0.set_update_time(10)
        self.qtgui_time_sink_x_4_1_0_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_0_0_0.enable_tags(False)
        self.qtgui_time_sink_x_4_1_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_0_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_0_0_0.enable_grid(True)
        self.qtgui_time_sink_x_4_1_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_0_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1_0_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_0_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_0_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_0_0_0_win)
        self.qtgui_time_sink_x_4_1_0_0 = qtgui.time_sink_c(
            (int( total_symbols *256)), #size
            samp_rate, #samp_rate
            "mixer o/p ", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_0_0.set_update_time(10)
        self.qtgui_time_sink_x_4_1_0_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_0_0.enable_tags(False)
        self.qtgui_time_sink_x_4_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_0_0.enable_grid(True)
        self.qtgui_time_sink_x_4_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_0_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_0_0_win)
        self.qtgui_time_sink_x_4_1 = qtgui.time_sink_c(
            (int(total_symbols*256)), #size
            samp_rate, #samp_rate
            "BaseBandSignal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1.set_update_time(1)
        self.qtgui_time_sink_x_4_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1.enable_tags(True)
        self.qtgui_time_sink_x_4_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1.enable_grid(True)
        self.qtgui_time_sink_x_4_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_4_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_win)
        self.qtgui_freq_sink_x_0_1 = qtgui.freq_sink_c(
            (1024*2), #size
            window.WIN_KAISER, #wintype
            0, #fc
            samp_rate , #bw
            "Freq Response of symbols", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_1.set_update_time(2)
        self.qtgui_freq_sink_x_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_1_win)
        self.qtgui_freq_sink_x_0_0_0_1_1 = qtgui.freq_sink_c(
            (1024*2), #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Freq Response of MatchedFilt o/p", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0_1_1.set_update_time(500)
        self.qtgui_freq_sink_x_0_0_0_1_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_0_1_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0_1_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0_1_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0_1_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_0_1_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0_1_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0_1_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0_1_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0_1_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0_1_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0_1_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0_1_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0_1_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_1_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0_1_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_1_1_win)
        self.qtgui_freq_sink_x_0_0_0_1 = qtgui.freq_sink_c(
            (1024*2), #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "Freq Response of mixer o/p", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0_1.set_update_time(500)
        self.qtgui_freq_sink_x_0_0_0_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0_0_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0_1.enable_grid(False)
        self.qtgui_freq_sink_x_0_0_0_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0_0_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0_1.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_1_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            (1024*2), #size
            window.WIN_KAISER, #wintype
            0, #fc
            samp_rate, #bw
            "Freq Response of QPSK", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(500)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            (1024*2), #size
            window.WIN_KAISER, #wintype
            0, #fc
            samp_rate , #bw
            "Freq Response of BaseBandSignal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(2)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.qtgui_eye_sink_x_0_0 = qtgui.eye_sink_c(
            (int( 10*256)), #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0_0.set_update_time(10)
        self.qtgui_eye_sink_x_0_0.set_samp_per_symbol(interpolation_factor)
        self.qtgui_eye_sink_x_0_0.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_0_0.set_y_label('Amplitude', "Eye After matchedFilter")

        self.qtgui_eye_sink_x_0_0.enable_tags(True)
        self.qtgui_eye_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0_0.enable_grid(False)
        self.qtgui_eye_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0_0.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_eye_sink_x_0_0_win)
        self.qtgui_eye_sink_x_0 = qtgui.eye_sink_c(
            (int(total_symbols*256)), #size
            samp_rate, #samp_rate
            1, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(interpolation_factor)
        self.qtgui_eye_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_eye_sink_x_0.set_y_label('Amplitude', "Eye After interpolator")

        self.qtgui_eye_sink_x_0.enable_tags(True)
        self.qtgui_eye_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0.enable_grid(False)
        self.qtgui_eye_sink_x_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0.enable_control_panel(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_eye_sink_x_0_win)
        self.qtgui_const_sink_x_0_1_0 = qtgui.const_sink_c(
            int( total_symbols), #size
            "After FIR", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1_0.set_update_time(2)
        self.qtgui_const_sink_x_0_1_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0_1_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0_1_0.enable_grid(True)
        self.qtgui_const_sink_x_0_1_0.enable_axis_labels(True)


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
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_1_0_win)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            (int( (total_symbols)*256)), #size
            "After Matched Filtering", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(2)
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
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            (int( (32/nbits))), #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(2)
        self.qtgui_const_sink_x_0.set_y_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_x_axis((-2), 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(True)
        self.qtgui_const_sink_x_0.enable_grid(True)
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
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                10,
                samp_rate,
                1000,
                1000,
                window.WIN_HAMMING,
                6.76))
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(interpolation_factor, rrc_taps)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fir_filter_xxx_1 = filter.fir_filter_ccf(1, rrc_taps)
        self.fir_filter_xxx_1.declare_sample_delay(0)
        self.fir_filter_xxx_0 = filter.fir_filter_ccf((samp_rate // symbol_rate), rrc_taps)
        self.fir_filter_xxx_0.declare_sample_delay(0)
        self.epy_block_4 = epy_block_4.file_with_postamble(filename='/media/linux1/600GB_EXT4/GNU_radio/GNURadio_src_dev_test_dir/03_flowgraphs/BPSK_tests/alice_excerpt.txt', postamble=0x0F00)
        self.epy_block_1 = epy_block_1.FramingPlusTagInserter(preamble=0xaa, postamble=0x0f)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((numpy.exp(1j*2*numpy.pi*numpy.arange(N)/N )), 1)
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_gr_complex*1, symbol_rate, True, 0 if "auto" == "auto" else max( int(float(2) * symbol_rate) if "auto" == "time" else int(2), 1) )
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(2) * samp_rate) if "auto" == "time" else int(2), 1) )
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(nbits, gr.GR_MSB_FIRST)
        self.blocks_null_sink_1 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(100)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(100)
        self.band_reject_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.band_reject(
                20,
                samp_rate,
                6800,
                9100,
                100,
                window.WIN_HAMMING,
                6.76))
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fc, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, fc, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.band_reject_filter_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_const_sink_x_0_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.qtgui_time_sink_x_4_1_0_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.qtgui_time_sink_x_4_1_3, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.band_reject_filter_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_eye_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.qtgui_time_sink_x_4_1, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.qtgui_freq_sink_x_0_1, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.qtgui_time_sink_x_4_1_1, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.epy_block_1, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.epy_block_4, 0), (self.epy_block_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.fir_filter_xxx_0, 0), (self.blocks_null_sink_1, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.qtgui_eye_sink_x_0_0, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.qtgui_freq_sink_x_0_0_0_1_1, 0))
        self.connect((self.fir_filter_xxx_1, 0), (self.qtgui_time_sink_x_4_1_0_0_1, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.fir_filter_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.fir_filter_xxx_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_time_sink_x_4_1_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "ASK_grFlowgraph")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))
        self.set_samp_rate(self.symbol_rate * self.interpolation_factor)
        self.blocks_throttle2_0_0.set_sample_rate(self.symbol_rate)
        self.qtgui_time_sink_x_4_1_1.set_samp_rate(self.symbol_rate )

    def get_interpolation_factor(self):
        return self.interpolation_factor

    def set_interpolation_factor(self, interpolation_factor):
        self.interpolation_factor = interpolation_factor
        self.set_lpf_taps_downsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.samp_rate/(2*self.interpolation_factor), 200, 1))
        self.set_ntaps(int(self.interpolation_factor*11))
        self.set_samp_rate(self.symbol_rate * self.interpolation_factor)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(self.interpolation_factor)
        self.qtgui_eye_sink_x_0_0.set_samp_per_symbol(self.interpolation_factor)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_lpf_taps_downsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.samp_rate/(2*self.interpolation_factor), 200, 1))
        self.set_lpf_taps_upsampling(firdes.low_pass(1.0, self.samp_rate*64 , self.fc+300, 200, 1))
        self.set_rrc_taps(numpy.array ( firdes.root_raised_cosine(1,self.samp_rate,self.symbol_rate, self.excess_bw,self.ntaps )))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.band_reject_filter_0.set_taps(firdes.band_reject(20, self.samp_rate, 6800, 9100, 100, window.WIN_HAMMING, 6.76))
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(10, self.samp_rate, 1000, 1000, window.WIN_HAMMING, 6.76))
        self.qtgui_eye_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_eye_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate )
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0_0_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0_0_1_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_1.set_frequency_range(0, self.samp_rate )
        self.qtgui_time_sink_x_4_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4_1_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4_1_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4_1_0_0_1.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4_1_3.set_samp_rate(self.samp_rate)

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
        self.analog_sig_source_x_0.set_frequency(self.fc)
        self.analog_sig_source_x_0_0.set_frequency(self.fc)

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
        self.fir_filter_xxx_0.set_taps(self.rrc_taps)
        self.fir_filter_xxx_1.set_taps(self.rrc_taps)
        self.interp_fir_filter_xxx_0.set_taps(self.rrc_taps)

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
        self.digital_chunks_to_symbols_xx_0_0.set_symbol_table((numpy.exp(1j*2*numpy.pi*numpy.arange(self.N)/self.N )))




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
