import QtQuick 1.1

// Фон
Image {
    width: windowWidth
    height: windowHeight
    source: "../img/wallpaper.jpg"

    // Эмблема МФС в footer'е
    Image {
        id: footer
        anchors{
            bottom: parent.bottom
            bottomMargin: 50
            horizontalCenter: parent.horizontalCenter
        }
        source: "../img/logomfc.png"
    }

    // List element delegate (Button)
    Component {
        id: queueDelegate

        Item {
            property variant item: modelData

            width: parent.width
            height: 200

            Rectangle {
                property variant text

                id: container
                anchors.horizontalCenter: parent.horizontalCenter
                height: text.height + 50; width: text.width + 70
                border.width: 1
                radius: 4
                smooth: true

                gradient: Gradient {
                    GradientStop {
                        position: 0.0
                        color: !mouseArea.pressed ? "#696969" : "#000000"
                    }
                    GradientStop {
                        position: 1.0
                        color: !mouseArea.pressed ? "#F5F5F5" : "#E6E6FA"
                    }
                }

                SystemPalette { id: activePalette }

                MouseArea {
                    id: mouseArea

                    anchors.fill: parent
                    onClicked: {
                        queueView.currentIndex = index
                        dialogquestion.show()
                    }
                }

                Text {
                    id: text
                    anchors.centerIn:parent
                    font.pointSize: 50
                    style: Text.Raised
                    styleColor: "#AAAAAA"
                    text: modelData.name
                    color: !mouseArea.pressed ? activePalette.buttonText : "#F5F5F5"
                }
            }
        }
    }

    // Список передоставляемых сервисов
    ListView {
        id: queueView
        anchors{
            fill: parent
            topMargin: 100
        }
        model: queueModel
        delegate: queueDelegate
    }

    // Главный элемент для диалогового окна
    Rectangle {
        id: dialogquestion

        // Функция для отображения окна
        // изменяет прозрачность главного элемента
        function show() {
            dialogquestion.opacity = 1;
        }

        // Функция для закрытия окна
        function hide() {
            dialogquestion.opacity = 0;
        }

        // Прозрачный задний фон
        color: "transparent"
        // Полностью прозрачен по умолчанию
        opacity: 0

        // Ширина и высота устанавливаются равными
        // ширине и высоте родительского элемента
        // в данном случае это элемент с id: canvas
        width: parent.width
        height: parent.height

        // Видимым элемент будет считаться если выполняется условие
        // opacity > 0
        visible: opacity > 0

        // Дочерний элемент, создающий полупрозрачный фон
        Rectangle {
            anchors.fill: parent
            opacity: 0.5
            color: "gray"
        }

        Rectangle {
            anchors{
                top: parent.top
                bottom: parent.bottom
                left: parent.left
            }

            width: 200
            border.width: 1
            radius: 4
            smooth: true

            gradient: Gradient {
                GradientStop {
                    position: 0.0
                    color: !mouseArea.pressed ? "#DCDCDC" : "#E6E6FA"
                }
                GradientStop {
                    position: 1.0
                    color: !mouseArea.pressed ? "#C0C0C0" : "#E6E6FA"
                }
            }

            SystemPalette { id: activePalette }

            MouseArea {
                id: mouseArea

                anchors.fill: parent
                onClicked: {
                    dialogquestion.hide()
                }
            }

            Image {
                anchors.centerIn: parent
                source: "../img/arrow_left128x128.png"
            }
        }

        // Дочерний элемент создающий который является диалогом
        // "Question..."
        Rectangle {
            id: dialog

            // Ширина и высота являются фиксированными
            width: 580
            height: 250

            // Координаты верхнего левого угла вычисляются
            // исходя из размеров самого диалога и родителя
            // так, чтобы окно располагалось в центре
            x: parent.width / 2 - dialog.width / 2;
            y: parent.height / 2 - dialog.height / 2;
            // Задаем z индекс таким, чтобы он был
            // больше z тех элементов, которые должны остаться
            // за диалоговым окном
            z: 10
            border.width: 2
            border.color: "gray"
            radius: 6
            smooth: true
            color: "#F5F5DC"

            Text {
                anchors {
                    top: parent.top
                    topMargin: 10
                    horizontalCenter: parent.horizontalCenter
                }

                text: "Вы были ранее зарегистрированы?"
                font.bold: true
                font.pixelSize: 24
                color: "#DEB887"
                style: Text.Outline
                styleColor: "#696969"

            }

            BorderImage {
                 id: buttonYes
                 anchors {
                     left: parent.left
                     leftMargin: 40
                     bottom: parent.bottom
                     bottomMargin: 40
                 }
                 width: 200
                 height: 100
                 source: "../img/button-" + "green" + ".png"
                 clip: true
                 border {
                     left: 10
                     top: 10
                     right: 10
                     bottom: 10
                 }

                 Rectangle {
                     id: shadeYes
                     anchors.fill: buttonYes
                     radius: 10
                     color: "black"
                     opacity: 0
                 }

                 Text {
                     id: buttonTextYes
                     anchors.centerIn: parent
                     anchors.verticalCenterOffset: -1
                     font.pixelSize: parent.width > parent.height ? parent.height * .5 : parent.width * .5
                     style: Text.Sunken
                     color: "white"
                     styleColor: "black"
                     smooth: true
                     text: "Да"
                 }

                 MouseArea {
                     id: mouseAreaYes
                     anchors.fill: parent
                     onClicked: {
                         self._pkSelectService(queueView.currentItem.item.id)
                         dialogquestion.hide()
                         dialogUser.show()
                     }
                 }

                 states: State {
                     name: "pressed"
                     when: mouseAreaYes.pressed === true
                     PropertyChanges { target: shadeYes; opacity: .4 }
                 }
             }

            BorderImage {
                 id: buttonNo
                 anchors {
                     right: parent.right
                     rightMargin: 40
                     bottom: parent.bottom
                     bottomMargin: 40
                 }

                 width: 200
                 height: 100

                 source: "../img/button-" + "red" + ".png"
                 clip: true
                 border {
                     left: 10
                     top: 10
                     right: 10
                     bottom: 10
                 }

                 Rectangle {
                     id: shadeNo
                     anchors.fill: buttonNo
                     radius: 10
                     color: "black"
                     opacity: 0
                 }

                 Text {
                     id: buttonTextNo
                     anchors.centerIn: parent
                     anchors.verticalCenterOffset: -1
                     font.pixelSize: parent.width > parent.height ? parent.height * .5 : parent.width * .5
                     style: Text.Sunken
                     color: "white"
                     styleColor: "black"
                     smooth: true
                     text: "Нет"
                 }

                 MouseArea {
                     id: mouseAreaNo
                     anchors.fill: parent
                     onClicked: {
                         self._pkButtonNo(queueView.currentItem.item.id)
                         dialogquestion.hide()
                     }
                 }

                 states: State {
                     name: "pressed"
                     when: mouseAreaNo.pressed === true
                     PropertyChanges { target: shadeNo; opacity: .4 }
                 }
             }
        }

        Behavior on opacity {
            NumberAnimation { duration: 100 }
        }
    }


    Rectangle {
        id: dialogUser

        // Функция для отображения окна
        // изменяет прозрачность главного элемента
        function show() {
            dialogUser.opacity = 1;
        }

        // Функция для закрытия окна
        function hide() {
            dialogUser.opacity = 0;
        }

        // Прозрачный задний фон
        color: "transparent"
        // Полностью прозрачен по умолчанию
        opacity: 0

        // Ширина и высота устанавливаются равными
        // ширине и высоте родительского элемента
        // в данном случае это элемент с id: canvas
        width: parent.width
        height: parent.height

        // Видимым элемент будет считаться если выполняется условие
        // opacity > 0
        visible: opacity > 0

        // Дочерний элемент, создающий полупрозрачный фон
        Rectangle {
            anchors.fill: parent
            opacity: 0.5
            color: "gray"
        }

        Rectangle {
            anchors{
                top: parent.top
                bottom: parent.bottom
                left: parent.left
            }

            width: 200
            border.width: 1
            radius: 4
            smooth: true

            gradient: Gradient {
                GradientStop {
                    position: 0.0
                    color: !mouseAreaU.pressed ? "#DCDCDC" : "#E6E6FA"
                }
                GradientStop {
                    position: 1.0
                    color: !mouseAreaU.pressed ? "#C0C0C0" : "#E6E6FA"
                }
            }

            MouseArea {
                id: mouseAreaU

                anchors.fill: parent
                onClicked: {
                    dialogUser.hide()
                    dialogquestion.show()
                }
            }

            Image {
                anchors.centerIn: parent
                source: "../img/arrow_left128x128.png"
            }
        }

        // Дочерний элемент создающий который является диалогом
        // "Question..."
        Rectangle {
            id: dialogU

            // Ширина и высота являются фиксированными
            width: 580
            height: 500

            // Координаты верхнего левого угла вычисляются
            // исходя из размеров самого диалога и родителя
            // так, чтобы окно располагалось в центре
            x: parent.width / 2 - dialogU.width / 2;
            y: parent.height / 2 - dialogU.height / 2;
            // Задаем z индекс таким, чтобы он был
            // больше z тех элементов, которые должны остаться
            // за диалоговым окном
            z: 10
            border.width: 2
            border.color: "gray"
            radius: 6
            smooth: true
            color: "#F5F5DC"

            Text {
                anchors {
                    top: parent.top
                    topMargin: 10
                    horizontalCenter: parent.horizontalCenter
                }

                text: "Пожалуйста выберите сотрудника у\nкоторого вы были зарегистрированы."
                font.bold: true
                font.pixelSize: 24
                color: "#DEB887"
                style: Text.Outline
                styleColor: "#696969"

            }
            // List element delegate (User)
            Component {
                id: userDelegate

                Item {
                    property variant item: modelData

                    width: parent.width
                    height: 70

                    Rectangle {
                        property variant text

                        id: container
                        anchors.horizontalCenter: parent.horizontalCenter
                        height: text.height + 20; width: text.width + 20
                        border.width: 1
                        radius: 4
                        smooth: true

                        color: mouseArea.pressed ? "#E6E6FA" : "#FAF0E6"

                        MouseArea {
                            id: mouseArea

                            anchors.fill: parent
                            onClicked: {
                                userView.currentIndex = index
                                self._pkButtonYes(userView.currentItem.item.id)
                                dialogUser.hide()
                            }
                        }

                        Text {
                            id: text
                            anchors.centerIn:parent
                            font.pointSize: 15
                            style: Text.Raised
                            styleColor: "#AAAAAA"
                            text: modelData.name
                            color: !mouseArea.pressed ? "#AAAAAA" : "#F5F5F5"
                        }
                    }
                }
            }

            // Список передоставляемых сервисов
            ListView {
                id: userView
                anchors{
                    fill: parent
                    topMargin: 100
                }
                model: userModel
                delegate: userDelegate
                focus: true
                clip: true
            }

            ScrollBar {
                target: userView
            }
        }

        Behavior on opacity {
            NumberAnimation { duration: 100 }
        }
    }
}
