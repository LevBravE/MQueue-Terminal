# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui
from SynchronizationServerThread import SynchronizationServerThread
from SynchronizationSessionThread import SynchronizationSessionThread
from DialogTerminal import DialogTerminal
from DialogSettings import DialogSettings

#**************************************************************************************************
# class: MainWindow
#**************************************************************************************************

class MainWindow(QtGui.QMainWindow):
    """
    Главное окно
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.__APPLICATION_CORP = 'LevCorp'
        self.__APPLICATION_NAME = 'MQueue-Terminal'
        self.__VERSION = '1.0'
        self.__dataBase = None
        self.__session = None
        self.__flagSession = False
        self.__lastSession = None
        # Thread
        self.__synchronizationServerThread = SynchronizationServerThread()
        self.__synchronizationSessionThread = SynchronizationSessionThread()
        # Timer
        self.__synchronizationTimer = QtCore.QTimer()
        # Label
        self.__imageCentralLabel = QtGui.QLabel()
        self.__imageCentralLabel.setPixmap('img/MQTerminalApp.png')

        self.__statusMQueueDataBase = QtGui.QLabel()
        self.__statusMQueueDataBase.setAlignment(QtCore.Qt.AlignHCenter)

        self.__statusMQueueSession = QtGui.QLabel()
        self.__statusMQueueSession.setAlignment(QtCore.Qt.AlignHCenter)
        # Dialog
        self.__dialogTerminal = None
        # Functions
        self._createActions()
        self._createToolBars()
        self._createMenus()
        self._createStatusBar()
        self._synchronizationAutoServer()
        self._readSettings()
        # Connect
        self.__synchronizationServerThread.finished.connect(self._checkAvailabilityServer)
        self.__synchronizationSessionThread.finished.connect(self._checkAvailabilitySession)
        self.__synchronizationSessionThread.finished.connect(self._openTerminal)

        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoServer)
        self.__synchronizationTimer.timeout.connect(self._synchronizationAutoSession)
        # Timer every 1 sec
        self.__synchronizationTimer.start(2000)
        # <<<Self>>>
        self.setWindowTitle('%s %s' % (self.__APPLICATION_NAME, self.__VERSION))
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setCentralWidget(self.__imageCentralLabel)
        self.layout().setSizeConstraint(QtGui.QLayout.SetFixedSize)

    def _createActions(self):
        # Action File
        self.__actionFileSettingTerminal = QtGui.QAction(QtGui.QIcon('img/black/png/wrench_plus_2_icon&16.png'),
            self.tr('&Настройки'), self, shortcut='Ctrl+Alt+S',
            statusTip=self.tr('Настройки терминала'), triggered=self._settingTerminal)

        self.__actionFileExit = QtGui.QAction(
            self.tr('В&ыход'), self, shortcut=QtGui.QKeySequence.Quit,
            statusTip=self.tr('Выйти из программы'), triggered=self.close)
        # Action Help
        self.__actionHelpAbout = QtGui.QAction(
            self.tr('&О программе'), self,
            statusTip=self.tr('Показать информацию о программе'), triggered=self._about)

    def _createToolBars(self):
        self.__toolBar = self.addToolBar(self.tr('Панель инструментов'))
        self.__toolBar.setMovable(False)
        self.__toolBar.addAction(self.__actionFileSettingTerminal)

    def _createMenus(self):
        fileMenu = self.menuBar().addMenu(self.tr('&Файл'))
        fileMenu.addAction(self.__actionFileSettingTerminal)
        fileMenu.addSeparator()
        fileMenu.addAction(self.__actionFileExit)

        helpMenu = self.menuBar().addMenu(self.tr('&Помощь'))
        helpMenu.addAction(self.__actionHelpAbout)

    def _createStatusBar(self):
        self.statusBar().showMessage(self.tr('Готово'))
        self.statusBar().addPermanentWidget(self.__statusMQueueSession)
        self.statusBar().addPermanentWidget(self.__statusMQueueDataBase)

    def _readSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        pos = settings.value('pos', QtCore.QPoint(200, 100))
        size = settings.value('size', QtCore.QSize(400, 200))

        self.resize(size)
        self.move(pos)

    def _writeSettings(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        settings.setValue('pos', self.pos())
        settings.setValue('size', self.size())

    def _openTerminal(self):
        if self.__dataBase and not self.__flagSession:
            settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
            windowWidth = settings.value('windowWidth', '1280')
            windowHeight = settings.value('windowHeight', '720')
            screenNumber = settings.value('screenNumber', '0')

            self.__flagSession = True

            if self.__dialogTerminal:
                self.__dialogTerminal.accept()

            self.__dialogTerminal = DialogTerminal(self.__dataBase, self.__session, windowWidth, windowHeight)
            screenRes = QtGui.QDesktopWidget().screenGeometry(int(screenNumber))
            self.__dialogTerminal.move(QtCore.QPoint(screenRes.x(), screenRes.y()))
            self.__dialogTerminal.showFullScreen()
            self.__dialogTerminal.exec_()

    def _settingTerminal(self):
        """
        Настройки приложения
        """
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        host = settings.value('address', '127.0.0.1')
        user = settings.value('user', 'mqueueserver')
        password = settings.value('password', 'mfc1000dog')
        port = settings.value('port', '3306')
        screenNumber = settings.value('screenNumber', '0')
        windowWidth = settings.value('windowWidth', '1280')
        windowHeight = settings.value('windowHeight', '720')

        dialogSettings = DialogSettings(self.tr('Настройки'))
        dialogSettings._setHostLineEdit(host)
        dialogSettings._setUserLineEdit(user)
        dialogSettings._setPasswordLineEdit(password)
        dialogSettings._setPortLineEdit(port)
        dialogSettings._setScreenComboBox(int(screenNumber))
        dialogSettings._setWindowWidthLineEdit(windowWidth)
        dialogSettings._setWindowHeightLineEdit(windowHeight)

        if dialogSettings.exec_() == QtGui.QDialog.Accepted:
            settings.setValue('address', dialogSettings._hostLineEdit())
            settings.setValue('user', dialogSettings._userLineEdit())
            settings.setValue('password', dialogSettings._passwordLineEdit())
            settings.setValue('port', dialogSettings._portLineEdit())
            settings.setValue('screenNumber', dialogSettings._screenComboBox())
            settings.setValue('windowWidth', dialogSettings._windowWidthLineEdit())
            settings.setValue('windowHeight', dialogSettings._windowHeightLineEdit())
            dialogSettings.close()

    def closeEvent(self, event):
        """
        Обработка события выхода из программы
        """
        ok = QtGui.QMessageBox.question(self, self.tr('Завершение программы'),
            self.tr('Завершить программу %s?' % self.__APPLICATION_NAME),
            QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel)

        if ok == QtGui.QMessageBox.Ok:
            self.__dialogTerminal.accept()
            event.accept()
        else:
            event.ignore()

    def _about(self):
        """
        О программе
        """
        QtGui.QMessageBox.about(self, self.tr('О программе'),
            self.tr('Программа <u>MQueue-Terminal</u> является частью '
                    'системы MQueue. Предназначенна для выполнения '
                    'функции терминала.\n'
                    '<p><b><i>LevBravE</i></b> специально для МФЦ'))

    def _synchronizationAutoServer(self):
        settings = QtCore.QSettings(self.__APPLICATION_CORP, self.__APPLICATION_NAME)
        host = settings.value('address', '127.0.0.1')
        user = settings.value('user', 'mqueueserver')
        password = settings.value('password', 'mfc1000dog')
        port = settings.value('port', '3306')

        self.__synchronizationServerThread._setHost(host)
        self.__synchronizationServerThread._setUser(user)
        self.__synchronizationServerThread._setPassword(password)
        self.__synchronizationServerThread._setPort(port)
        self.__synchronizationServerThread.start()

    def _checkAvailabilityServer(self):
        self.__dataBase = self.__synchronizationServerThread._response()

        if self.__dataBase:
            strStatusMQueueDataBase = self.tr('<p style="font-size: 12px"> '
                                              '<img width="11" height="11" src="img/circle_green.png"> База данных</p>')
            self.__statusMQueueDataBase.setText(strStatusMQueueDataBase)
            self.__statusMQueueDataBase.setToolTip(self.tr('Сервер базы данных, доступен'))

            return True
        else:
            strStatusMQueueDataBase = self.tr('<p style="font-size: 12px"> '
                                              '<img width="11" height="11" src="img/circle_red.png"> База данных</p>')
            self.__statusMQueueDataBase.setText(strStatusMQueueDataBase)
            self.__statusMQueueDataBase.setToolTip(self.tr('Сервер базы данных, недоступен'))

            return False

    def _synchronizationAutoSession(self):
        self.__synchronizationSessionThread._setDataBase(self.__dataBase)
        self.__synchronizationSessionThread.start()

    def _checkAvailabilitySession(self):
        self.__session = self.__synchronizationSessionThread._response()

        if self.__lastSession != self.__session:
            self.__lastSession = self.__session
            self.__flagSession = False


        if self.__session:
            strStatusMQueueSession = self.tr('<p style="font-size: 12px"> '
                                             '<img width="11" height="11" src="img/circle_green.png"> Сессия</p>')
            self.__statusMQueueSession.setText(strStatusMQueueSession)
            self.__statusMQueueSession.setToolTip(self.tr('Сессия начата'))

            return True
        else:
            strStatusMQueueSession = self.tr('<p style="font-size: 12px"> '
                                             '<img width="11" height="11" src="img/circle_red.png"> Сессия</p>')
            self.__statusMQueueSession.setText(strStatusMQueueSession)
            self.__statusMQueueSession.setToolTip(self.tr('Сессия завершена'))

            return False

