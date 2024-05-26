from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QSlider, QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit, QCheckBox, QButtonGroup


from skelly_viewer.utilities.freemocap_data_loader import FreeMoCapDataLoader
from scripts.read_csv import read_from_csv

# from pathlib import Path
# from freemocap.data_layer.recording_models.post_processing_parameter_models import ProcessingParameterModel
import os
import configparser

PRESUMED_FRAMES_PER_SECOND = 30


class QSliderButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedWidth(75)


class PlayPauseCountSlider(QWidget):
    def __init__(self):
        super().__init__()

        # Define a global variable to hold the file path
        self.file_path = None

        # addition start
        documents_folder = os.path.expanduser("~\\Documents")
        filename = "angles-csv_location.txt"
        txt_path = os.path.join(documents_folder, filename)
        # temp_path = os.path.join(documents_folder, 'temp.txt')
        

        #angles_csv = 'C:\\Users\\Arya\\OneDrive - Universiti Sains Malaysia\\Final Year\\CAT405\\Project_Final\\out_angle4.csv'

        # creating arr1 - arr10

        self._timer = QTimer()
        self._timer.timeout.connect(self._timer_timeout)

        self._layout = QVBoxLayout(self)

        slider_hbox = QHBoxLayout()
        self._layout.addLayout(slider_hbox)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        slider_hbox.addWidget(self._slider)
        self.slider_max = 0
        self._slider.valueChanged.connect(lambda: self._frame_count_label.setText(f"Frame# {self._slider.value()}"))

        self._frame_count_label = QLabel(f"Frame# {self._slider.value()}")
        slider_hbox.addWidget(self._frame_count_label)

        hbox = QHBoxLayout()
        self._layout.addLayout(hbox)

        self._play_button = QSliderButton("Play")
        self._play_button.clicked.connect(self._play_button_clicked)
        hbox.addWidget(self._play_button)

        self._pause_button = QSliderButton("Pause")
        self._pause_button.clicked.connect(self._pause_button_clicked)
        hbox.addWidget(self._pause_button)

        self._reset_button = QSliderButton("Reset")
        self._reset_button.clicked.connect(self._reset_button_clicked)
        hbox.addWidget(self._reset_button)
                   
        # layout = QHBoxLayout()
        # self._layout.addLayout(layout)
        # layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # label_test2 = QLabel("test")  
        # label_test2.setStyleSheet("font-size: 15px")
        # label_test2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # label_test2.setWordWrap(True)
        # layout.addWidget(label_test2)
        #---------------------------------
        
        layout_h = QHBoxLayout()
        self._layout.addLayout(layout_h)
        layout_h.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set the layout
        layout2 = QVBoxLayout()
        self._layout.addLayout(layout2)
        layout2.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        # Create a QLineEdit widget for text input (file path)
        self.textbox = QLineEdit(self)
        layout2.addWidget(self.textbox)
        
        # Create a QLabel to display the result
        self.label = QLabel("Enter angles.csv file path and press Submit", self)
        self.label2 = QLabel("Usually located in 'C:\\Users\\%USER%\\freemocap_data\\recording_sessions\\%SESSION%\\output_data\\angles.csv'", self)
        #self.label2 = QLabel(str(self.load_angles_path()), self)
        self.label2.setStyleSheet("font-size: 13px")
        layout2.addWidget(self.label)
        layout2.addWidget(self.label2)
        
        # Create a QSliderButton (custom QPushButton) for submission
        self.button2 = QSliderButton('Submit')
        self.button2.clicked.connect(self.on_click)
        layout2.addWidget(self.button2)

        # Set the layout to the QWidget
        self.setLayout(layout2)
        #----------------------------------
        
        # Load the saved text box value
        self.load_textbox_value()


        # addition starts
        if self.textbox is not None:
            if os.path.exists(str(self.load_angles_path())):
                # Load the saved text box value
                #self.load_textbox_value()

                # with open(self.load_textbox_value(), 'r') as file:
                #     angles_csv = file.read()
                angles_csv = self.load_angles_path()

                self.arr1 = read_from_csv(angles_csv, 0)
                self.arr2 = read_from_csv(angles_csv, 1)
                self.arr3 = read_from_csv(angles_csv, 2)
                self.arr4 = read_from_csv(angles_csv, 3)
                self.arr5 = read_from_csv(angles_csv, 4)
                self.arr6 = read_from_csv(angles_csv, 5)
                self.arr7 = read_from_csv(angles_csv, 6)
                self.arr8 = read_from_csv(angles_csv, 7)
                self.arr9 = read_from_csv(angles_csv, 8)
                self.arr10 = read_from_csv(angles_csv,9)

                # angles display addition start
                new_hbox = QHBoxLayout()
                self._layout.addLayout(new_hbox)

                self._slider.valueChanged.connect(lambda:self._frame_count_label1.setText(f"\nHead: {self.arr1[self._slider.value()]}"))
                self._frame_count_label1 = QLabel(f"Head: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label1)

                self._slider.valueChanged.connect(lambda:self._frame_count_label3.setText(f"\nUpper Left Arm: {self.arr3[self._slider.value()]}"))
                self._frame_count_label3 = QLabel(f"Upper Left Arm: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label3)

                self._slider.valueChanged.connect(lambda:self._frame_count_label4.setText(f"\nUpper Right Arm: {self.arr4[self._slider.value()]}"))
                self._frame_count_label4 = QLabel(f"Upper Right Arm: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label4)

                self._slider.valueChanged.connect(lambda:self._frame_count_label5.setText(f"\nUpper Left Leg: {self.arr5[self._slider.value()]}"))
                self._frame_count_label5 = QLabel(f"Upper Left Leg: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label5)

                self._slider.valueChanged.connect(lambda:self._frame_count_label6.setText(f"\nUpper Right Leg: {self.arr6[self._slider.value()]}"))
                self._frame_count_label6 = QLabel(f"Upper Right Leg: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label6)

                new_hbox1 = QHBoxLayout()
                self._layout.addLayout(new_hbox1)

                self._slider.valueChanged.connect(lambda:self._frame_count_label2.setText(f"\nTrunk: {self.arr2[self._slider.value()]}"))
                self._frame_count_label2 = QLabel(f"Trunk: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label2)

                self._slider.valueChanged.connect(lambda:self._frame_count_label7.setText(f"\nLower Left Arm: {self.arr7[self._slider.value()]}"))
                self._frame_count_label7 = QLabel(f"Lower Left Arm: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label7)

                self._slider.valueChanged.connect(lambda:self._frame_count_label8.setText(f"\nLower Right Arm: {self.arr8[self._slider.value()]}"))
                self._frame_count_label8 = QLabel(f"Lower Right Arm: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label8)

                self._slider.valueChanged.connect(lambda:self._frame_count_label9.setText(f"\nLower Left Leg: {self.arr9[self._slider.value()]}"))
                self._frame_count_label9 = QLabel(f"Lower Left Leg: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label9)

                self._slider.valueChanged.connect(lambda:self._frame_count_label10.setText(f"\nLower Right Leg: {self.arr10[self._slider.value()]}"))
                self._frame_count_label10 = QLabel(f"Lower Right Leg: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label10)
                #--------------------Condition-----------------------------
                vbox_weight = QVBoxLayout()
                self.label_weight = QLabel("Weight (kg):", self)
                vbox_weight.addWidget(self.label_weight)
                self.checkbox_group_weight = QButtonGroup(self)
                # Create a QCheckBox widget
                self.checkbox = QCheckBox('< 5kg')
                self.checkbox_group_weight.addButton(self.checkbox)
                self.checkbox_group_weight.setId(self.checkbox, 1)
                self.checkbox.stateChanged.connect(self.get_selected_values)
                vbox_weight.addWidget(self.checkbox)

                self.checkbox2 = QCheckBox('5 - 10kg')
                self.checkbox_group_weight.addButton(self.checkbox2)
                self.checkbox_group_weight.setId(self.checkbox2, 2)
                self.checkbox2.stateChanged.connect(self.get_selected_values)
                vbox_weight.addWidget(self.checkbox2)

                self.checkbox3 = QCheckBox('> 10kg')
                self.checkbox_group_weight.addButton(self.checkbox3)
                self.checkbox_group_weight.setId(self.checkbox3, 3)
                self.checkbox3.stateChanged.connect(self.get_selected_values)
                vbox_weight.addWidget(self.checkbox3)

                vbox_neck = QVBoxLayout()
                self.label_neck = QLabel("Neck condition:", self)
                vbox_neck.addWidget(self.label_neck)
                # Create a QCheckBox widget
                self.checkbox4 = QCheckBox('Twisted', self)
                self.checkbox4.stateChanged.connect(self.get_checkbox_value)
                vbox_neck.addWidget(self.checkbox4)
                self.checkbox5 = QCheckBox('Side Bending', self)
                self.checkbox5.stateChanged.connect(self.get_checkbox_value)
                vbox_neck.addWidget(self.checkbox5)

                vbox_trunk = QVBoxLayout()
                self.label_trunk = QLabel("Trunk condition:", self)
                vbox_trunk.addWidget(self.label_trunk)
                # Create a QCheckBox widget
                self.checkbox6 = QCheckBox('Twisted')
                self.checkbox6.stateChanged.connect(self.get_checkbox_value)
                vbox_trunk.addWidget(self.checkbox6)
                self.checkbox7 = QCheckBox('Side Bending')
                self.checkbox7.stateChanged.connect(self.get_checkbox_value)
                vbox_trunk.addWidget(self.checkbox7)

                vbox_u_arm = QVBoxLayout()
                self.label_u_arm = QLabel("Upper Arm condition:", self)
                vbox_u_arm.addWidget(self.label_u_arm)
                # Create a QCheckBox widget
                self.checkbox8 = QCheckBox('Shoulder is raised')
                self.checkbox8.stateChanged.connect(self.get_checkbox_value)
                vbox_u_arm.addWidget(self.checkbox8)
                self.checkbox9 = QCheckBox('Upper arm is abducted')
                self.checkbox9.stateChanged.connect(self.get_checkbox_value)
                vbox_u_arm.addWidget(self.checkbox9)
                self.checkbox10 = QCheckBox('Arm is supported/leaning')
                self.checkbox10.stateChanged.connect(self.get_checkbox_value)
                vbox_u_arm.addWidget(self.checkbox10)

                layout_h.addLayout(vbox_weight)
                layout_h.addLayout(vbox_neck)
                layout_h.addLayout(vbox_trunk)
                layout_h.addLayout(vbox_u_arm)
            else:
                pass
        # end
        

        self.set_frames_per_second(PRESUMED_FRAMES_PER_SECOND)

    @property
    def frames_per_second(self):
        return self._frames_per_second

    @property
    def frame_duration(self):
        return self._frame_duration

    def set_frames_per_second(self, frames_per_second):
        self._frames_per_second = frames_per_second
        self._frame_duration = 1.0 / frames_per_second

    def set_slider_range(self, num_frames):
        self.slider_max = num_frames - 1
        self._slider.setValue(0)
        self._slider.setMaximum(self.slider_max)

    @Slot()
    def _timer_timeout(self):
        if self._slider.value() < self.slider_max:
            self._slider.setValue(self._slider.value() + 1)
        else:
            self._slider.setValue(0)

    @Slot()
    def _play_button_clicked(self):
        self._timer.stop()
        self._timer.start(0)  # play as fast as possible

    @Slot()
    def _pause_button_clicked(self):
        self._timer.stop()

    @Slot()
    def _reset_button_clicked(self):
        self._timer.stop()
        self._slider.setValue(0)

    #-------------------------------------------------
    def get_selected_values(self):
        # Iterate through the checkboxes and print the IDs of checked ones
        for button in self.checkbox_group_weight.buttons():
            if button.isChecked():
                button_id = self.checkbox_group_weight.id(button)
                print(f"Checkbox ID: {button_id}")

    def get_checkbox_value(self):
        checkbox4_state = self.checkbox4.isChecked()
        checkbox5_state = self.checkbox5.isChecked()
        print(self.checkbox4.isChecked())
    
    def on_click(self):
        # Get the text from the textbox
        file_path = self.textbox.text()
        
        # Check if the file exists
        if os.path.exists(file_path):
            # If the file exists, update the global variable
            self.file_path = file_path
            
            # Save the text box value
            self.save_textbox_value(self.file_path)
            
            message = f'File exists: {self.file_path}'
        else:
            message = f'File does not exist: {file_path}'
        
        # Update the label to display the result
        self.label.setText(message)
        
        # Print the result to the console (optional)
        print(message)

        # Print the checkbox state
        # print(f"Checkbox is {'checked' if self.checkbox.checkState() == Qt.CheckState.Checked else 'unchecked'}")
    
    def save_textbox_value(self, value):
        # Save the text box value to a configuration file
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'file_path': value}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    
    def load_textbox_value(self):
        # Load the text box value from the configuration file
        config = configparser.ConfigParser()
        if os.path.exists('config.ini'):
            config.read('config.ini')
            file_path = config['DEFAULT'].get('file_path', '')
            self.textbox.setText(file_path)

    def load_angles_path(self):
        # Load the text box value from the configuration file
        config = configparser.ConfigParser()
        if os.path.exists('config.ini'):
            config.read('config.ini')
            file_path = config['DEFAULT'].get('file_path', '')
            return file_path
        else:
            return None