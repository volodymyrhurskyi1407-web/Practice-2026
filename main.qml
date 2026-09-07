import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true; width: 400; height: 600; title: "Менеджер витрат"

    ColumnLayout {
        anchors.fill: parent; anchors.margins: 15

        Text { text: "Загалом: " + expenseManager.total.toFixed(2) + " ₴"; font.pointSize: 16; font.bold: true; Layout.alignment: Qt.AlignHCenter }

        RowLayout {
            Layout.fillWidth: true
            TextField { id: descF; placeholderText: "Назва"; Layout.fillWidth: true }
            TextField { id: amountF; placeholderText: "Сума"; Layout.preferredWidth: 80 }
        }
        ComboBox { id: catC; model: ["Продукти", "Транспорт", "Розваги", "Інше"]; Layout.fillWidth: true }
        Button {
            text: "Додати"; Layout.fillWidth: true
            onClicked: {
                if (descF.text !== "" && amountF.text !== "") {
                    expenseManager.addExpense(descF.text, amountF.text, catC.currentText)
                    descF.text = ""; amountF.text = ""
                }
            }
        }

        ListView {
            id: listView; Layout.fillWidth: true; Layout.fillHeight: true; model: expenseModel; clip: true; spacing: 5
            add: Transition { NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 300 } }
            delegate: Rectangle {
                width: listView.width; height: 50; color: "#f0f0f0"; radius: 5
                RowLayout {
                    anchors.fill: parent; anchors.margins: 10
                    Text { text: model.description + " (" + model.category + ")"; Layout.fillWidth: true }
                    Text { text: model.amount.toFixed(2) + " ₴"; font.bold: true }
                    Button { text: "X"; onClicked: expenseManager.removeExpense(index) }
                }
            }
        }
    }
}