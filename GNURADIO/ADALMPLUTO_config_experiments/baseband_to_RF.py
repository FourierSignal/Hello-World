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
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import iio
import numpy
import sip
import threading



class baseband_to_RF(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "baseband_to_RF")

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
        self.Mhz = Mhz = 1000*1000
        self.Khz = Khz = 1000
        self.samp_rate = samp_rate = 2*Mhz
        self.fm = fm = 100*Khz
        self.RF_BW = RF_BW = 2*Mhz

        ##################################################
        # Blocks
        ##################################################

        self.qtgui_time_sink_x_4_1_1_0 = qtgui.time_sink_c(
            (10*(int((1/fm)*samp_rate))), #size
            samp_rate, #samp_rate
            "sine signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_4_1_1_0.set_update_time(500)
        self.qtgui_time_sink_x_4_1_1_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_4_1_1_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_4_1_1_0.enable_tags(True)
        self.qtgui_time_sink_x_4_1_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_4_1_1_0.enable_autoscale(True)
        self.qtgui_time_sink_x_4_1_1_0.enable_grid(True)
        self.qtgui_time_sink_x_4_1_1_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_4_1_1_0.enable_control_panel(False)
        self.qtgui_time_sink_x_4_1_1_0.enable_stem_plot(False)


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
                    self.qtgui_time_sink_x_4_1_1_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_4_1_1_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_4_1_1_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_4_1_1_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_4_1_1_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_4_1_1_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_4_1_1_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_4_1_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_4_1_1_0_win = sip.wrapinstance(self.qtgui_time_sink_x_4_1_1_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_4_1_1_0_win)
        self.qtgui_time_sink_x_1_0_0 = qtgui.time_sink_f(
            100, #size
            samp_rate, #samp_rate
            "RXmodulated Signal", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1_0_0.set_update_time(500)
        self.qtgui_time_sink_x_1_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_1_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1_0_0.enable_tags(True)
        self.qtgui_time_sink_x_1_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1_0_0.enable_autoscale(True)
        self.qtgui_time_sink_x_1_0_0.enable_grid(True)
        self.qtgui_time_sink_x_1_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_1_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_1_0_0.enable_stem_plot(False)


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


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_1_0_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_0_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_f(
            (1024*2*8*2), #size
            window.WIN_RECTANGULAR, #wintype
            (500*Mhz), #fc
            (RF_BW*100), #bw
            "Freq Response of  RF signal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(2)
        self.qtgui_freq_sink_x_0_0.set_y_axis((-2.5), (-1.5))
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(True)


        self.qtgui_freq_sink_x_0_0.set_plot_pos_half(not True)

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
            (1024*2*8*2), #size
            window.WIN_RECTANGULAR, #wintype
            0, #fc
            (fm*2), #bw
            "Freq Response of BaseBandSignal", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(2)
        self.qtgui_freq_sink_x_0.set_y_axis((-2.5), (-1.5))
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(True)



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
        self.iio_pluto_source_0 = iio.fmcomms2_source_fc32('' if '' else iio.get_pluto_uri(), [True, True], 32768)
        self.iio_pluto_source_0.set_len_tag_key('packet_len')
        self.iio_pluto_source_0.set_frequency((500*Mhz))
        self.iio_pluto_source_0.set_samplerate(samp_rate)
        self.iio_pluto_source_0.set_gain_mode(0, 'manual')
        self.iio_pluto_source_0.set_gain(0, 40)
        self.iio_pluto_source_0.set_quadrature(True)
        self.iio_pluto_source_0.set_rfdc(True)
        self.iio_pluto_source_0.set_bbdc(True)
        self.iio_pluto_source_0.set_filter_params('Auto', '', 0, 0)
        self.iio_pluto_sink_0 = iio.fmcomms2_sink_fc32('' if '' else iio.get_pluto_uri(), [True, True], 32768, False)
        self.iio_pluto_sink_0.set_len_tag_key('')
        self.iio_pluto_sink_0.set_bandwidth(RF_BW)
        self.iio_pluto_sink_0.set_frequency((500*Mhz))
        self.iio_pluto_sink_0.set_samplerate(samp_rate)
        self.iio_pluto_sink_0.set_attenuation(0, 30)
        self.iio_pluto_sink_0.set_filter_params('Auto', '', 0, 0)
        self.blocks_skiphead_0 = blocks.skiphead(gr.sizeof_float*1, 20000)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, fm, 0.5, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_skiphead_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.iio_pluto_sink_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.qtgui_time_sink_x_4_1_1_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.blocks_skiphead_0, 0), (self.qtgui_time_sink_x_1_0_0, 0))
        self.connect((self.iio_pluto_source_0, 0), (self.blocks_complex_to_real_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "baseband_to_RF")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_Mhz(self):
        return self.Mhz

    def set_Mhz(self, Mhz):
        self.Mhz = Mhz
        self.set_RF_BW(2*self.Mhz)
        self.set_samp_rate(2*self.Mhz)
        self.iio_pluto_sink_0.set_frequency((500*self.Mhz))
        self.iio_pluto_source_0.set_frequency((500*self.Mhz))
        self.qtgui_freq_sink_x_0_0.set_frequency_range((500*self.Mhz), (self.RF_BW*100))

    def get_Khz(self):
        return self.Khz

    def set_Khz(self, Khz):
        self.Khz = Khz
        self.set_fm(100*self.Khz)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.iio_pluto_sink_0.set_samplerate(self.samp_rate)
        self.iio_pluto_source_0.set_samplerate(self.samp_rate)
        self.qtgui_time_sink_x_1_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_4_1_1_0.set_samp_rate(self.samp_rate)

    def get_fm(self):
        return self.fm

    def set_fm(self, fm):
        self.fm = fm
        self.analog_sig_source_x_0.set_frequency(self.fm)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, (self.fm*2))

    def get_RF_BW(self):
        return self.RF_BW

    def set_RF_BW(self, RF_BW):
        self.RF_BW = RF_BW
        self.iio_pluto_sink_0.set_bandwidth(self.RF_BW)
        self.qtgui_freq_sink_x_0_0.set_frequency_range((500*self.Mhz), (self.RF_BW*100))




def main(top_block_cls=baseband_to_RF, options=None):

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
