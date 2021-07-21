#-*- coding:utf-8 -*-
#
# This file is part of CoTeTo - a code generation tool
# 201500225 Joerg Raedler jraedler@udk-berlin.de
#

import sys
import os
import os.path
import tempfile
import argparse
import logging
import configparser
import traceback
import CoTeTo
from CoTeTo.Controller import Controller
from PyQt5 import QtCore, QtWidgets, QtGui, uic

descr = """CoTeTo is a tool for the generation of source code and other text from
different data sources. It can be easily extended, runs with a GUI, a
commandline interface or can be integrated in other python projects as a module."""


# view log in Qt - inspired by
# http://stackoverflow.com/questions/14349563/how-to-get-non-blocking-real-time-behavior-from-python-logging-module-output-t

class QtLogHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        record = self.format(record)
        if record:
            XStream.stdout().write('%s\n' % record)


class XStream(QtCore.QObject):
    _stdout = None
    _stderr = None
    _ostdout = None
    _ostderr = None
    messageWritten = QtCore.pyqtSignal(str)

    def flush(self):
        pass

    def fileno(self):
        return -1

    def write(self, msg):
        if not self.signalsBlocked():
            self.messageWritten.emit(msg)

    @staticmethod
    def stdout():
        if not XStream._stdout:
            XStream._stdout = XStream()
            XStream._ostdout = sys.stdout
            sys.stdout = XStream._stdout
        return XStream._stdout

    @staticmethod
    def stderr():
        if not XStream._stderr:
            XStream._stderr = XStream()
            XStream._ostderr = sys.stderr
            sys.stderr = XStream._stderr
        return XStream._stderr

    @staticmethod
    def reset():
        if XStream._stdout:
            sys.stdout = XStream._ostdout
        if XStream._stderr:
            sys.stdout = XStream._ostderr


class LogViewer(QtWidgets.QWidget):

    def __init__(self, resPath, *arg, **kwarg):
        QtWidgets.QWidget.__init__(self)
        # load the ui
        self.ui = uic.loadUi(os.path.join(resPath, 'MessageBrowser.ui'), self)
        XStream.stdout().messageWritten.connect(self.textBrowser.insertPlainText)
        XStream.stderr().messageWritten.connect(self.textBrowser.insertPlainText)
        self.logHandler = QtLogHandler()
        self.logHandler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
        self.logger = logging.getLogger('CoTeTo')
        i = int(kwarg['logLevel'] / 10) - 1  # convert level to QComboBox index
        self.levelSelect.setCurrentIndex(i)
        self.levelSelect.currentIndexChanged.connect(self.setLevel)
        self.clearButton.pressed.connect(self.clearLog)
        self.saveButton.pressed.connect(self.saveLog)

    def setLevel(self, i):
        l = (i + 1) * 10  # convert QComboBox index to level :-)
        self.logger.setLevel(l)

    def clearLog(self):
        self.textBrowser.clear()

    def saveLog(self):
        f = QtWidgets.QFileDialog.getSaveFileName(self, 'Select Output File', '*')
        if not (f and f[0]):
            return
        try:
            open(f[0], 'w').write(self.textBrowser.toPlainText())
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error during save', 'Message log could not be saved!')
            self.logger.exception('Could not save message log')


class CoTeToWidget(QtWidgets.QWidget):

    def __init__(self, app, resPath, cfg, *arg, **kwarg):
        QtWidgets.QWidget.__init__(self)
        self.app = app

        # load the Icons
        sys.path.insert(0, resPath)
        import Icons_rc

        # load the ui
        self.ui = uic.loadUi(os.path.join(resPath, 'CoTeTo-GUI.ui'), self)
        self.setWindowTitle('CoTeTo GUI | Version: %s' % (CoTeTo.__version__))
        self.cfg = cfg
        self._arg = arg
        self._kwarg = kwarg

        # create a logView?
        if 'logLevel' in kwarg and kwarg['logLevel'] > 0:
            self.logView = LogViewer(resPath, *arg, **kwarg)
            self.coTeToMainView.addTab(self.logView, 'Messages')
            kwarg['logHandler'] = self.logView.logHandler
        # get the logger
        self.logger = logging.getLogger('CoTeTo')

        # replace systems exception hook
        sys.excepthook = self.exceptionHook

        # do more initialization later
        QtCore.QTimer().singleShot(500, self.lateInit)

    def lateInit(self):
        # create a controller
        self.ctt = Controller(*(self._arg), **(self._kwarg))
        # loaders
        self.loaderList.itemSelectionChanged.connect(self.activateLoader)
        self.loaderView.anchorClicked.connect(self.openURL)
        for a in sorted(self.ctt.loaders):
            self.loaderList.addItem(a)
        self.loaderList.item(0).setSelected(True)

        # generators
        self.activeGenerator = None
        self.generatorListReloadButton.pressed.connect(self.updateGeneratorList)
        self.generatorExplorerButton.pressed.connect(self.exploreGenerators)
        self.generatorList.itemSelectionChanged.connect(self.activateGenerator)
        self.generatorView.anchorClicked.connect(self.openURL)
        self.generateButton.clicked.connect(self.executeGenerator)
        self.updateGeneratorList(rescan=False)

        # buttons
        self.uriLoadButton.clicked.connect(self.getUriList)
        self.outputLoadButton.clicked.connect(self.getOutputFile)

        # set preferences from cfg
        if self.cfg.has_section('PREFERENCES'):
            p = self.cfg['PREFERENCES']
            self.uriInput.setText(p.get('uriList', ''))
            self.outputInput.setText(p.get('outputFile', ''))
            g = p.get('generator', '')
            for x in range(self.generatorList.count()):
                i = self.generatorList.item(x)
                if i.text() == g:
                    i.setSelected(1)
                    break
        # end of preferences

    # general methods
    def exceptionHook(self, t, v, tb):
        """Show unhandled exceptions"""
        msg = ''.join(traceback.format_exception(t, v, tb))
        self.logger.critical('An unhandled exception occured')
        print('*' * 40 + '\n' + msg + '*' * 40)
        QtWidgets.QMessageBox.critical(self, 'An unhandled exception occured',
                                       'Please have a look at the <b>Messages</b> tab for details!')

    def openURL(self, url):
        """open an link target from the generator or loader view"""
        scheme = url.scheme()
        if scheme == 'file':
            # print(url)
            QtGui.QDesktopServices.openUrl(url)
        elif scheme == 'loader':
            a = url.authority().replace('___', '::').lower()
            i = self.loaderList.findItems(a, QtCore.Qt.MatchFixedString)[0]
            self.loaderList.setCurrentItem(i)
            self.loaderList.itemActivated.emit(i)
            self.coTeToMainView.setCurrentIndex(1)
        else:
            print('Unknown URL scheme:', url)

    def getUriList(self):
        flist = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select Data Sources')
        if flist and flist[0]:
            self.uriInput.setText(', '.join(flist[0]))

    def getOutputFile(self):
        f = QtWidgets.QFileDialog.getSaveFileName(self, 'Select Output File', '*')
        if f and f[0]:
            self.outputInput.setText(f[0])

    # loader methods
    def activateLoader(self):
        items = self.loaderList.selectedItems()
        if items:
            loader = items[0].text()
        self.loaderView.clear()
        # FIXME: this is ugly, loader class is not instantiated yet ... but we need the information
        c = self.ctt.loaders[loader]
        self.loaderView.setText(c.infoText(c, 'html'))

    # generator methods
    def exploreGenerators(self):
        for p in self.ctt.generatorPath:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(p))

    def updateGeneratorList(self, rescan=True):
        # get old selection
        selItems = self.generatorList.selectedItems()
        selected = None
        if selItems:
            selected = selItems[0].text()
        if rescan:
            self.ctt.rescanGenerators()
        self.generatorList.clear()
        i = 0
        for n in sorted(self.ctt.generators):
            self.generatorList.addItem(n)
            if n == selected:
                # select previously selected generator
                self.generatorList.item(i).setSelected(True)
            i += 1
        if not self.generatorList.selectedItems():
            # nothing selected, select the first in the list
            self.generatorList.item(0).setSelected(True)

    def activateGenerator(self):
        sel = self.generatorList.selectedItems()
        if sel:
            gen = sel[0].text()
        else:
            return
        self.activeGenerator = self.ctt.generators[gen]
        self.generatorView.clear()
        self.generatorView.setText(self.activeGenerator.infoText('html'))

    def executeGenerator(self):
        line = self.uriInput.text()
        uriList = [u.strip() for u in line.split(',')]
        outputBase = str(self.outputInput.text())
        if not outputBase:
            tmp, outputBase = tempfile.mkstemp(suffix='.txt', text=True)
            self.outputInput.setText(outputBase)
        if not os.path.isabs(outputBase):
            outputBase = os.path.abspath(outputBase)
        x = self.activeGenerator.execute(uriList,outputBase)
        for ext in x:
            outputFile = outputBase + ext
            o = open(outputFile, 'w')
            o.write(x[ext].read())
            o.close()
            if self.openOutputButton.isChecked():
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(outputFile))

    def closeEvent(self, e):
        # first reset output streams to standard settings
        XStream.reset()
        # save preferences to config file
        if hasattr(self.cfg, 'path'):
            uriList = self.uriInput.text()
            outputFile = self.outputInput.text()
            generator = ''
            tmp = self.generatorList.selectedItems()
            if tmp:
                generator = tmp[0].text()
            try:
                c = self.cfg
                p = 'PREFERENCES'
                if not c.has_section(p):
                    c.add_section(p)
                c.set(p, 'uriList', uriList)
                c.set(p, 'outputFile', outputFile)
                c.set(p, 'generator', generator)
                with open(c.path, 'w') as configfile:
                    c.write(configfile)
            except BaseException:
                # silently ignore errors
                # FIXME: is this a good idea? But where should the errors appear?
                pass
        e.accept()


def main():
    """main function when CoTeTo is used with the Qt gui"""

    parser = argparse.ArgumentParser(description=descr)
    grp = parser.add_argument_group('path settings')
    grp.add_argument('-p', '--search-path', metavar='PATH', help='search path for generators (separated by ;)')
    grp = parser.add_argument_group('general information')
    grp.add_argument('-d', '--debug', metavar='LEVEL', help='set debug level and activate messages tab (1...5)')

    args = parser.parse_args()

    # first read config file for default values
    defaults = {
        'GeneratorPath': os.environ.get('COTETO_GENERATORS', ''),
        'LogLevel': '2',
    }
    cfg = configparser.ConfigParser(defaults)
    homeVar = {'win32': 'USERPROFILE', 'linux': 'HOME', 'linux2': 'HOME', 'darwin': 'HOME'}.get(sys.platform)
    cfgFile = os.path.join(os.environ.get(homeVar, ''), '.CoTeTo.cfg')
    if os.path.isfile(cfgFile):
        cfg.read(cfgFile)
        cfg.path = cfgFile

    # generatorPath
    gp = args.search_path or cfg['DEFAULT']['GeneratorPath']
    generatorPath = [p for p in gp.split(';') if p]

    # logLevel
    logLevel = 10 * cfg.getint('DEFAULT', 'LogLevel')
    if args.debug:
        logLevel = 10 * int(args.debug)

    # FIXME: resPath may need to be adjusted after installation,
    # or use pkg_resources? See:
    # http://stackoverflow.com/questions/779495/python-access-data-in-package-subdirectory
    resPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'res')

    app = QtWidgets.QApplication(sys.argv)
    mw = CoTeToWidget(app, resPath, cfg, generatorPath, logLevel=logLevel)
    mw.show()
    r = app.exec_()
    return(r)
