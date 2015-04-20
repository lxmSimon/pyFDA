# -*- coding: utf-8 -*-
"""
Created on Wed Nov 26 15:48:44 2014

@author: Christian Muenker
http://matplotlib.1069221.n5.nabble.com/Figure-with-pyQt-td19095.html
"""
from __future__ import print_function, division, unicode_literals

from PyQt4 import QtGui, QtCore

from PyQt4.QtGui import QSizePolicy, QLabel, QInputDialog
#from PyQt4.QtCore import QSize

#import matplotlib as mpl
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backend_bases import cursors as mplCursors
from matplotlib.figure import Figure
#from mpl_toolkits.mplot3d.axes3d import Axes3D
import six

try:
    import matplotlib.backends.qt_editor.figureoptions as figureoptions
except ImportError:
    figureoptions = None
#from .qt_compat import QtCore, QtGui, QtWidgets, _getSaveFileName, __version__

from matplotlib import rcParams
rcParams['font.size'] = 12

import os
#import numpy as np
# import scipy.signal as sig

DEBUG = True

#------------------------------------------------------------------------------
#class MplWidgetBut(QtGui.QWidget):
#    """
#    Construct a subwidget with Matplotlib canvas, NavigationToolbar
#    and some buttons
#    """
#
#    def __init__(self, parent = None):
#        super(MplWidget, self).__init__() # initialize QWidget Base Class
#        # Create the mpl figure and subplot (5x4 inches, 100 dots-per-inch).
#        # Construct the canvas with the figure
#        #
#        self.dpi = 100
#        self.fig = Figure(dpi=self.dpi,facecolor = '#FFFFFF')
#        self.ax = self.fig.add_subplot(111)
#
#        self.pltCanv = FigureCanvas(self.fig)
#
#
#        self.pltCanv.setSizePolicy(QSizePolicy.Expanding,
#                                   QSizePolicy.Expanding)
#        self.pltCanv.updateGeometry()
#
#        # Create the navigation toolbar, tied to the canvas
#        #
#        self.mpl_toolbar = self.MyMplToolbar(self.pltCanv, self)
#
#        self.butDraw = QtGui.QPushButton("&Redraw")
#        self.butDraw.clicked.connect(self.redraw)
#
#        self.cboxGrid = QtGui.QCheckBox("Show &Grid")
#        self.cboxGrid.setChecked(True)
#        # Attention: passes unwanted clicked bool argument:
#        self.cboxGrid.clicked.connect(self.redraw)
#
#        #=============================================
#        # Slider for line width
#        #=============================================
#        lblLw = QtGui.QLabel('Line width:')
#        self.sldLw = QtGui.QSlider(QtCore.Qt.Horizontal)
#        self.sldLw.setRange(1, 10)
#        self.sldLw.setValue(5)
#        self.sldLw.setTracking(True)
#        self.sldLw.setTickPosition(QtGui.QSlider.NoTicks)
##        self.sldLw.valueChanged.connect(self.redraw)
#
#        #=============================================
#        # Widget layout with QHBox / QVBox
#        #=============================================
#
#        self.hbox1 = QtGui.QHBoxLayout()
#        for w in [self.butDraw, self.cboxGrid, lblLw, self.sldLw]:
#            self.hbox1.addWidget(w)
#            self.hbox1.setAlignment(w, QtCore.Qt.AlignVCenter)
#
#        self.layVMainMpl = QtGui.QVBoxLayout()
#        self.layVMainMpl.addWidget(self.mpl_toolbar)
#        self.layVMainMpl.addWidget(self.pltCanv)
#        self.layVMainMpl.addLayout(self.hbox1)
#        self.setLayout(self.layVMainMpl)
#
#    def redraw(self):
#        """
#        Redraw the figure with new properties (grid, linewidth)
#        """
#        self.ax.grid(self.cboxGrid.isChecked())
##        plt.artist.setp(self.pltPlt, linewidth = self.sldLw.value()/5.)
#        self.fig.tight_layout(pad = 0.5)
#        self.pltCanv.draw()
#        self.pltCanv.updateGeometry()


#------------------------------------------------------------------------------
class MplWidget(QtGui.QWidget):
    """
    Construct a subwidget with Matplotlib canvas and NavigationToolbar
    """

    def __init__(self, parent = None):
        super(MplWidget, self).__init__() # initialize QWidget Base Class
        # Create the mpl figure and subplot (white bg, 100 dots-per-inch).
        # Construct the canvas with the figure
        #
        self.plt_lim = [] # x,y plot limits
        self.dpi = 100
        self.fig = Figure(dpi=self.dpi,facecolor = '#FFFFFF')
#        self.mpl = self.fig.add_subplot(111) # self.fig.add_axes([.1,.1,.9,.9])#
#        self.mpl21 = self.fig.add_subplot(211)

        self.pltCanv = FigureCanvas(self.fig)
        self.pltCanv.setSizePolicy(QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)

        self.pltCanv.updateGeometry()

        # Create the custom navigation toolbar, tied to the canvas
        #
        #self.mplToolbar = NavigationToolbar(self.pltCanv, self) # original
        self.mplToolbar = MyMplToolbar(self.pltCanv, self)
        self.mplToolbar.grid = True
        self.mplToolbar.enable_update = True

        #=============================================
        # Widget layout with QHBox / QVBox
        #=============================================

#        self.hbox = QtGui.QHBoxLayout()
#
#        for w in [self.mpl_toolbar, self.butDraw, self.cboxGrid]:
#            self.hbox.addWidget(w)
#            self.hbox.setAlignment(w, QtCore.Qt.AlignVCenter)
#        self.hbox.setSizeConstraint(QtGui.QLayout.SetFixedSize)

        self.layVMainMpl = QtGui.QVBoxLayout()
#        self.layVMainMpl.addLayout(self.hbox)
        self.layVMainMpl.addWidget(self.mplToolbar)
        self.layVMainMpl.addWidget(self.pltCanv)


        self.setLayout(self.layVMainMpl)

    def redraw(self):
        """
        Redraw the figure with new properties (grid, linewidth)
        """
#        self.ax.grid(self.mplToolbar.grid)
        for ax in self.fig.axes:
            ax.grid(self.mplToolbar.grid) # collect axes objects and toggle grid
#        plt.artist.setp(self.pltPlt, linewidth = self.sldLw.value()/5.)
        self.fig.tight_layout(pad = 0.5)
        self.pltCanv.draw()
        self.pltCanv.updateGeometry()
        
    def redraw3D(self):
        """
        Redraw the figure with new properties (grid, linewidth)
        """
        self.pltCanv.draw()
        self.pltCanv.updateGeometry()

    def pltFullView(self):
        """
        Full zoom
        """
        for ax in self.fig.axes:
            ax.autoscale()
        self.redraw()

#------------------------------------------------------------------------------

class MyMplToolbar(NavigationToolbar):
    """
    Custom Matplotlib Navigationtoolbar, derived (sublassed) from
    Navigationtoolbar with the following changes:
    - new icon set
    - new functions and icons grid, full view
    - removed buttons for configuring subplots and editing curves
    - added an x,y location widget and icon


    derived from http://www.python-forum.de/viewtopic.php?f=24&t=26437
    
    http://pydoc.net/Python/pyQPCR/0.7/pyQPCR.widgets.matplotlibWidget/  !!
    http://matplotlib.org/users/navigation_toolbar.html !!
    
    see also http://stackoverflow.com/questions/17711099/programmatically-change-matplotlib-toolbar-mode-in-qt4
             http://matplotlib-users.narkive.com/C8XwIXah/need-help-with-darren-dale-qt-example-of-extending-toolbar
             https://sukhbinder.wordpress.com/2013/12/16/simple-pyqt-and-matplotlib-example-with-zoompan/
    """
    
#    toolitems = (
#        ('Home', 'Reset original view', 'home', 'home'),
#        ('Back', 'Back to  previous view', 'action-undo', 'back'),
#        ('Forward', 'Forward to next view', 'action-redo', 'forward'),
#        (None, None, None, None),
#        ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
#        ('Zoom', 'Zoom to rectangle', 'magnifying-glass', 'zoom'),
#        (None, None, None, None),
#        ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
#        ('Save', 'Save the figure', 'file', 'save_figure'),
#      )
    
# subclass NavigationToolbar, passing through arguments:
    #def __init__(self, canvas, parent, coordinates=True):
    def __init__(self, *args, **kwargs):
        NavigationToolbar.__init__(self, *args, **kwargs)
        
#        QtWidgets.QToolBar.__init__(self, parent)

#    def _icon(self, name):
#        return QtGui.QIcon(os.path.join(self.basedir, name))
#        
    def _init_toolbar(self):
#        self.basedir = os.path.join(rcParams[ 'datapath' ], 'images/icons')
        iconDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
           '..','images','icons', '')

# org        self.basedir = os.path.join(rcParams['datapath'], 'images')
        self.basedir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
           '..','images', 'icons', '')
           
#        # Pan, Zoom
#        for text, tooltip_text, image_file, callback in self.toolitems:
#            if text is None:
#                self.addSeparator()
#            else:
#                a = self.addAction(self._icon(image_file + '.svg'),
#                                         text, getattr(self, callback))
#                self._actions[callback] = a
#                if callback in ['zoom', 'pan']:
#                    a.setCheckable(True)
#                if tooltip_text is not None:
#                    a.setToolTip(tooltip_text)

           
#---------------- Construct Toolbar ---------------------------------------           

        # ENABLE:
        a = self.addAction(QtGui.QIcon(iconDir + 'circle-check.svg'), \
                           'Enable Plot', self.enable_update)
        a.setToolTip('Enable plot update.')
        a.setCheckable(True)
        a.setChecked(True)
#        a.setEnabled(False) 
        
        self.addSeparator() #---------------------------------------------
        
        # HOME:
        self.a_ho = self.addAction(QtGui.QIcon(iconDir + 'home.svg'), \
                           'Home', self.home)
        self.a_ho.setToolTip('Reset original view')
        # BACK:
        self.a_ba = self.addAction(QtGui.QIcon(iconDir + 'action-undo.svg'), \
                           'Back', self.back)
        self.a_ba.setToolTip('Back to previous view')
        # FORWARD:
        self.a_fw = self.addAction(QtGui.QIcon(iconDir + 'action-redo.svg'), \
                           'Forward', self.forward)
        self.a_fw.setToolTip('Forward to next view')

        self.addSeparator() #---------------------------------------------
        
        # PAN:
        self.a_pa = self.addAction(QtGui.QIcon(iconDir + 'move.svg'), \
                           'Pan', self.pan)
        self.a_pa.setToolTip('Pan axes with left mouse button, zoom with right')
        self._actions['pan'] = self.a_pa
        self.a_pa.setCheckable(True)
        
        # ZOOM RECTANGLE:
        self.a_zo = self.addAction(QtGui.QIcon(iconDir + 'magnifying-glass.svg'), \
                           'Zoom', self.zoom)
        self.a_zo.setToolTip('Zoom in / out to rectangle with left / right mouse button.')
        self._actions['zoom'] = self.a_zo
        self.a_zo.setCheckable(True)

        # FULL VIEW:
        self.a_fv = self.addAction(QtGui.QIcon(iconDir + 'fullscreen-enter.svg'), \
            'Full View', self.parent.pltFullView)
        self.a_fv.setToolTip('Full view')
        
        self.addSeparator()
        
        # GRID:
        self.a_gr = self.addAction(QtGui.QIcon(iconDir + 'grid-four-up.svg'), \
                           'Grid', self.toggle_grid)
        self.a_gr.setToolTip('Toggle Grid')
        self.a_gr.setCheckable(True)
        self.a_gr.setChecked(True)
        
        # REDRAW:
        self.a_rd = self.addAction(QtGui.QIcon(iconDir + 'brush.svg'), \
                           'Redraw', self.parent.redraw)
        self.a_rd.setToolTip('Redraw Plot')
        
        # SAVE:
        self.a_sv = self.addAction(QtGui.QIcon(iconDir + 'file.svg'), \
                           'Save', self.save_figure)
        self.a_sv.setToolTip('Save the figure')

        
        if figureoptions is not None:
            self.a_op = self.addAction(QtGui.QIcon(iconDir + 'cog.svg'),
                               'Customize', self.edit_parameters)
            self.a_op.setToolTip('Edit curves line and axes parameters')

        self.buttons = {}

        # Add the x,y location widget at the right side of the toolbar
        # The stretch factor is 1 which means any resizing of the toolbar
        # will resize this label instead of the buttons.
        if self.coordinates:
            self.locLabel = QLabel("", self)
            self.locLabel.setAlignment(
                    QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            self.locLabel.setSizePolicy(
                QSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Ignored))
            labelAction = self.addWidget(self.locLabel)
            labelAction.setVisible(True)

        # reference holder for subplots_adjust window
        self.adj_window = None

    if figureoptions is not None:
        def edit_parameters(self):
            allaxes = self.canvas.figure.get_axes()
            if len(allaxes) == 1:
                axes = allaxes[0]
            else:
                titles = []
                for axes in allaxes:
                    title = axes.get_title()
                    ylabel = axes.get_ylabel()
                    label = axes.get_label()
                    if title:
                        fmt = "%(title)s"
                        if ylabel:
                            fmt += ": %(ylabel)s"
                        fmt += " (%(axes_repr)s)"
                    elif ylabel:
                        fmt = "%(axes_repr)s (%(ylabel)s)"
                    elif label:
                        fmt = "%(axes_repr)s (%(label)s)"
                    else:
                        fmt = "%(axes_repr)s"
                    titles.append(fmt % dict(title=title,
                                         ylabel=ylabel, label=label,
                                         axes_repr=repr(axes)))
                item, ok = QInputDialog.getItem(
                    self.parent, 'Customize', 'Select axes:', titles, 0, False)
                if ok:
                    axes = allaxes[titles.index(six.text_type(item))]
                else:
                    return

            figureoptions.figure_edit(axes, self)
            
#    def mouse_move(self, event):
#        if not event.inaxes or not self._active:
#            if self._lastCursor != mplCursors.POINTER:
#                self.set_cursor(mplCursors.POINTER)
#                self._lastCursor = mplCursors.POINTER
#        else:
#            if self._active == 'ZOOM':
#                if self._lastCursor != mplCursors.SELECT_REGION:
#                    self.set_cursor(mplCursors.SELECT_REGION)
#                    self._lastCursor = mplCursors.SELECT_REGION
#                if self._xypress:
#                    x, y = event.x, event.y
#                    lastx, lasty, _, _, _, _ = self._xypress[0]
#                    self.draw_rubberband(event, x, y, lastx, lasty)
#            elif (self._active == 'PAN' and
#                  self._lastCursor != mplCursors.MOVE):
#                self.set_cursor(mplCursors.MOVE)
#
#                self._lastCursor = mplCursors.MOVE
#
#        if event.inaxes and event.inaxes.get_navigate():
#
#            try: s = event.inaxes.format_coord(event.xdata, event.ydata)
#            except ValueError: pass
#            except OverflowError: pass
#            else:
#                if len(self.mode):
#                    self.set_message('%s : %s' % (self.mode, s))
#                else:
#                    self.set_message(s)
#        else: self.set_message(self.mode)
            
    def toggle_grid(self):
        self.grid = not self.grid
        self.parent.redraw()
        
    def enable_update(self):
        self.enable_update = not self.enable_update
        self.a_gr.setEnabled(self.enable_update)
        self.a_ho.setEnabled(self.enable_update)
        self.a_ba.setEnabled(self.enable_update)
        self.a_fw.setEnabled(self.enable_update)
        self.a_pa.setEnabled(self.enable_update)
        self.a_zo.setEnabled(self.enable_update)
        self.a_fv.setEnabled(self.enable_update)
        self.a_rd.setEnabled(self.enable_update)
        self.a_sv.setEnabled(self.enable_update)
        self.a_op.setEnabled(self.enable_update)