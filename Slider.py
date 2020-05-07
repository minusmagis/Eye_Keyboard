import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider,QLabel
from PyQt5.QtCore import Qt

class Slider():
    def __init__(self,Name = 'Slider 1', Min_Value = 0 , Max_Value = 100, Step_size = 1, Tick_Number = 5,Starting_value = 0):
        self.Name =Name
        self.Min_Value = Min_Value
        self.Max_Value = Max_Value
        self.Step_size = Step_size
        self.Tick_Interval = (Max_Value-Min_Value)/(Tick_Number+1)
        self.Starting_value = Starting_value


class Slider_window(QMainWindow):

    # This function accepts a list of the needed labels for the sliders and initializes that ammount of sliders
    def __init__(self,Slider_list):
        super().__init__()

        Label_max_length = 0
        spacing = 30
        self.Label_list = list()
        self.Slider_list = list()

        for index,Slider in enumerate(Slider_list):
            if len(Slider.Name) > Label_max_length:
                Label_max_length = len(Slider.Name)

            self.Label_list.append(QLabel(self))
            self.Label_list[index].resize(len(Slider.Name)*10, 20)
            self.Label_list[index].setText(str(Slider.Starting_value)+'  .'+str(Slider.Name))
            self.Label_list[index].move(240,38+spacing*index)


            self.Slider_list.append(QSlider(Qt.Horizontal, self))
            self.Slider_list[index].setGeometry(30, 40+spacing*index, 200, 30)
            self.Slider_list[index].setMinimum(Slider.Min_Value)
            self.Slider_list[index].setMaximum(Slider.Max_Value)
            self.Slider_list[index].setSingleStep(Slider.Step_size)
            self.Slider_list[index].setTickInterval(Slider.Tick_Interval)
            self.Slider_list[index].setTickPosition(QSlider.TicksBelow)
            self.Slider_list[index].setValue(Slider.Starting_value)
            self.Slider_list[index].valueChanged.connect(self.changeValue)


        self.setGeometry(50,50,350+Label_max_length*4,80+spacing*len(Slider_list))
        self.setWindowTitle("Parameter variables")
        self.show()

    def changeValue(self):
        for index,Slider_n in enumerate(self.Slider_list):
            Slider_label = self.Label_list[index].text().split('.',1)[1]
            Slider_label = str(self.Slider_list[index].value())+'  .' +Slider_label
            self.Label_list[index].setText(Slider_label)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Slider_window()
    sys.exit(app.exec_())