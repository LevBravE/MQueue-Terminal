# -*- coding: utf-8 -*-

__author__ = 'levbrave'

from PySide import QtCore, QtGui, QtDeclarative

#**************************************************************************************************
# class: DialogTerminal
#**************************************************************************************************

class DialogTerminal(QtGui.QDialog):
    """
    Диалоговое окно терминала
    """
    def __init__(self, dataBase, session, windowWidth, windowHeight):
        QtGui.QDialog.__init__(self)
        self.__dataBase = dataBase
        self.__session = session
        self.__selectService = None
        # Printer
        self.__printer = QtGui.QPrinter()
        self.__printer.setPaperSize(QtGui.QPrinter.A8)
        # DeclarativeView
        self.__view = QtDeclarative.QDeclarativeView()
        self.__contextView = self.__view.rootContext()
        self.__contextView.setContextProperty('windowWidth', int(windowWidth))
        self.__contextView.setContextProperty('windowHeight', int(windowHeight))

        if self.__session:
            cursor = self.__dataBase.cursor()
            cursor.execute('SELECT `service`.`id`, `service`.`name`  FROM `mqueuedb`.`service` '
                           'WHERE `service`.`enable`="1"')
            self.__dataBase.commit()
            lstService = cursor.fetchall()
            dataService = []

            for itemService in lstService:
                dataService.append({'id': itemService[0], 'name': self.tr(itemService[1])})

            self.__contextView.setContextProperty('queueModel', dataService)
            self.__contextView.setContextProperty('self', self)

            self.__view.setSource(QtCore.QUrl('qml/terminal.qml'))
        else:
            self.__view.setSource(QtCore.QUrl('qml/emblem.qml'))
        # Layout
        self.__layoutHMain = QtGui.QHBoxLayout()
        self.__layoutHMain.addWidget(self.__view)
        self.__layoutHMain.setContentsMargins(0, 0, 0, 0)
        # <<<Self>>>
        self.setLayout(self.__layoutHMain)
        #self.setCursor(QtCore.Qt.BlankCursor)

    @QtCore.Slot(int)
    def _pkSelectService(self, pk):
        self.__selectService = pk

        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `user`.`id`, `user`.`name` '
                       'FROM `mqueuedb`.`user` WHERE `user`.`service_id` = %s' % self.__selectService)
        self.__dataBase.commit()
        lstUser = cursor.fetchall()
        dataUser = []

        for itemUser in lstUser:
            dataUser.append({'id': itemUser[0], 'name':self.tr(itemUser[1])})

        self.__contextView.setContextProperty('userModel', dataUser)

    @QtCore.Slot(int)
    def _pkButtonNo(self, pk):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `dynamic_data`.`client_number` FROM `mqueuedb`.`dynamic_data`')
        self.__dataBase.commit()
        data = cursor.fetchone()

        cursor.execute('SELECT NOW()')
        self.__dataBase.commit()
        standDataTime = unicode(cursor.fetchone()[0])

        strV = 'INSERT INTO `mqueuedb`.`client` (`number`, `stand_time`, `start_time`, `finish_time`, `service_id`) ' \
               'VALUES ("%s", "%s", "0000-00-00 00:00:00", "0000-00-00 00:00:00", %s)' % (data[0], standDataTime, pk)
        cursor.execute(strV)
        self.__dataBase.commit()

        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `service`.`name` '
                       'FROM `mqueuedb`.`service` WHERE `service`.`id`="%s"' % pk)
        self.__dataBase.commit()
        serviceName = cursor.fetchone()

        regData = QtCore.QDateTime().fromString(standDataTime, QtCore.Qt.ISODate).toString('dd.MM.yyyy')
        regTime = QtCore.QDateTime().fromString(standDataTime, QtCore.Qt.ISODate).toString('hh:mm:ss')

        document = QtGui.QTextDocument()

        document.setPageSize(QtCore.QSizeF(self.__printer.width(), self.__printer.height()))

        document.setHtml(self.tr('<center><b style="font-size: 14pt;">Ваш номер</b>\n '
                                 '<p style="font-size: 14pt;">%s</p>\n '
                                 '<p><img src="img/MQLogo.png"/></p>\n '
                                 '<p>Услуга: %s</p> '
                                 '<p>Дата регистрации: %s</p> '
                                 '<p>Время регистрации: %s</p></center>' % (data[0], serviceName[0], str(regData), str(regTime))))
        document.print_(self.__printer)

        value = int(data[0])
        value += 1

        if value < 10:
            strValue = '00' + str(value)
        elif value < 100:
            strValue = '0' + str(value)
        else:
            strValue = str(value)

        strV = 'UPDATE `mqueuedb`.`dynamic_data` SET `client_number`="%s" WHERE `id`="1"' % strValue
        cursor.execute(strV)
        self.__dataBase.commit()


    @QtCore.Slot(int)
    def _pkButtonYes(self, pk):
        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `dynamic_data`.`client_number` FROM `mqueuedb`.`dynamic_data`')
        self.__dataBase.commit()
        data = cursor.fetchone()

        cursor.execute('SELECT NOW()')
        self.__dataBase.commit()
        standDataTime = unicode(cursor.fetchone()[0])

        strV = 'INSERT INTO mqueuedb.client (`number`, `stand_time`, `start_time`, `finish_time`, `user_id`, `service_id`) ' \
               'VALUES ("%s", "%s", "0000-00-00 00:00:00", "0000-00-00 00:00:00", %s, %s)' % (data[0], standDataTime, pk, self.__selectService)
        cursor.execute(strV)
        self.__dataBase.commit()

        cursor = self.__dataBase.cursor()
        cursor.execute('SELECT `service`.`name` '
                       'FROM `mqueuedb`.`service` WHERE `service`.`id` = %s' % self.__selectService)
        self.__dataBase.commit()
        serviceName = cursor.fetchone()

        cursor.execute('SELECT `user`.`name` '
                       'FROM `mqueuedb`.`user` WHERE `user`.`id` = %s' % pk)
        self.__dataBase.commit()
        userName = cursor.fetchone()

        regData = QtCore.QDateTime().fromString(standDataTime, QtCore.Qt.ISODate).toString('dd.MM.yyyy')
        regTime = QtCore.QDateTime().fromString(standDataTime, QtCore.Qt.ISODate).toString('hh:mm:ss')

        document = QtGui.QTextDocument()

        document.setPageSize(QtCore.QSizeF(self.__printer.width(), self.__printer.height()))
        document.setHtml(self.tr('<center><b style="font-size: 14pt;">Ваш номер</b>\n '
                                 '<p style="font-size: 14pt;">%s</p>\n '
                                 '<p><img src="img/MQLogo.png"/></p>\n '
                                 '<p>Услуга: %s</p> '
                                 '<p>Обслуживает: %s</p> '
                                 '<p>Дата регистрации: %s</p> '
                                 '<p>Время регистрации: %s</p></center>' % (data[0], serviceName[0], userName[0], str(regData), str(regTime))))
        document.print_(self.__printer)

        value = int(data[0])
        value += 1

        if value < 10:
            strValue = '00' + str(value)
        elif value < 100:
            strValue = '0' + str(value)
        else:
            strValue = str(value)

        strV = 'UPDATE `mqueuedb`.`dynamic_data` SET `client_number`="%s" WHERE `id`="1"' % strValue
        cursor.execute(strV)
        self.__dataBase.commit()
