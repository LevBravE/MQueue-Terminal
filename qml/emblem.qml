// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Image {
    width: windowWidth
    height: windowHeight
    source: "../img/backgraund.jpg"

    Image {
        anchors.centerIn: parent
        width: 600
        height: 160
        source: "../img/mfclogo1197x313.png"
    }
}
