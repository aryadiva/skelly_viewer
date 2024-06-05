from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtWidgets import QSlider, QWidget, QLabel, QHBoxLayout, QPushButton, QVBoxLayout, QLineEdit, QCheckBox, QButtonGroup


#from skelly_viewer.utilities.freemocap_data_loader import FreeMoCapDataLoader
from scripts.read_csv import read_from_csv
#from scripts.calculate_angles import CalculateAngles
from REBA.calculate_reba import DegreetoREBA

import pandas as pd

# from pathlib import Path
# from freemocap.data_layer.recording_models.post_processing_parameter_models import ProcessingParameterModel
import os
import configparser

PRESUMED_FRAMES_PER_SECOND = 30

def use_checkbox_value(is_checked):
    print(f"Checkbox is {'checked' if is_checked else 'unchecked'}")


class QSliderButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setFixedWidth(75)


class PlayPauseCountSlider(QWidget):
    def __init__(self):
        super().__init__()

        self.config_check_path = "C:\\Users\\Arya\\config_check.ini"
        self.dataTF = self.read_config()
        # Define a global variable to hold the file path
        self.file_path = None

        #self.reba_arr = []

        # addition start
        # documents_folder = os.path.expanduser("~\\Documents")
        # filename = "angles-csv_location.txt"
        # txt_path = os.path.join(documents_folder, filename)
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
        h_layout1 = QHBoxLayout()
        h_layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)
        h_layout2 = QHBoxLayout()
        h_layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.label = QLabel("Enter angles.csv file path and press Submit", self)
        self.label2 = QLabel("Usually located in 'C:\\Users\\%USER%\\freemocap_data\\recording_sessions\\%SESSION%\\output_data\\angles.csv'", self)
        #self.label2 = QLabel(str(self.load_angles_path()), self)
        self.label2.setStyleSheet("font-size: 13px")
        h_layout1.addWidget(self.label)
        h_layout2.addWidget(self.label2)
        
        # Create a QSliderButton (custom QPushButton) for submission
        # h_layout2 = QHBoxLayout()
        self.button2 = QSliderButton('Submit')
        self.button2.clicked.connect(self.on_click)
        h_layout2.addWidget(self.button2)

        layout2.addLayout(h_layout1)
        layout2.addLayout(h_layout2)

        # Set the layout to the QWidget
        self.setLayout(layout2)
        #----------------------------------
        
        # Load the saved text box value
        self.load_textbox_value()


        # addition starts
        if self.textbox is not None:
            if os.path.exists(str(self.load_angles_path())):
                # Load the checkboxes value
                #self.load_checkbox_states()

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
                self.arr11 = read_from_csv(angles_csv, 10)
                self.arr12 = read_from_csv(angles_csv,11)
                self.arr13 = read_from_csv(angles_csv,12)

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

                self._slider.valueChanged.connect(lambda:self._frame_count_label11.setText(f"\nLeft Wrist: {self.arr11[self._slider.value()]}"))
                self._frame_count_label11 = QLabel(f"Left Wrist: {self._slider.value()}")
                new_hbox.addWidget(self._frame_count_label11)

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

                self._slider.valueChanged.connect(lambda:self._frame_count_label12.setText(f"\nRight Wrist: {self.arr12[self._slider.value()]}"))
                self._frame_count_label12 = QLabel(f"Right Wrist: {self._slider.value()}")
                new_hbox1.addWidget(self._frame_count_label12)

                new_hbox_reba = QHBoxLayout()
                self._layout.addLayout(new_hbox_reba)

                self._slider.valueChanged.connect(lambda:self._frame_count_label13.setText(f"\nREBA Score: {self.arr13[self._slider.value()]}"))
                self._frame_count_label13 = QLabel(f"REBA Score: {self._slider.value()}")
                new_hbox_reba.addWidget(self._frame_count_label13)
            else:
                pass
        #--------------------Condition-----------------------------
        vbox_weight = QVBoxLayout()
        hbox_weight1 = QHBoxLayout()
        hbox_weight2 = QHBoxLayout()
        self.label_weight = QLabel("Weight (kg):", self)
        vbox_weight.addWidget(self.label_weight)
        self.checkbox_group_weight = QButtonGroup(self)
        self.checkbox_group_weight.setExclusive(True)

        # Create a QCheckBox widget
        self.checkbox0 = QCheckBox('< 5kg', self)
        self.checkbox_group_weight.addButton(self.checkbox0, 1)
        self.checkbox0.stateChanged.connect(self.save_value)
        #self.checkbox0.stateChanged.connect(self.checkbox0)
        hbox_weight1.addWidget(self.checkbox0)

        self.checkbox1 = QCheckBox('5 - 10kg', self)
        self.checkbox_group_weight.addButton(self.checkbox1, 2)
        self.checkbox1.stateChanged.connect(self.save_value)
        #self.checkbox1.stateChanged.connect(self.checkbox1)
        hbox_weight1.addWidget(self.checkbox1)

        self.checkbox2 = QCheckBox('> 10kg', self)
        self.checkbox_group_weight.addButton(self.checkbox2, 3)
        self.checkbox2.stateChanged.connect(self.save_value)
        #self.checkbox2.stateChanged.connect(self.checkbox2)
        hbox_weight2.addWidget(self.checkbox2)

        vbox_neck = QVBoxLayout()
        self.label_neck = QLabel("Neck condition:", self)
        vbox_neck.addWidget(self.label_neck)
        # Create a QCheckBox widget
        self.checkbox3 = QCheckBox('Twisted', self)
        self.checkbox3.stateChanged.connect(self.save_value)
        vbox_neck.addWidget(self.checkbox3)
        self.checkbox4 = QCheckBox('Side Bending', self)
        self.checkbox4.stateChanged.connect(self.save_value)
        vbox_neck.addWidget(self.checkbox4)

        vbox_trunk = QVBoxLayout()
        hbox_trunk1 = QVBoxLayout()
        self.label_trunk = QLabel("Trunk condition:", self)
        vbox_trunk.addWidget(self.label_trunk)
        # Create a QCheckBox widget
        self.checkbox5 = QCheckBox('Twisted', self)
        self.checkbox5.stateChanged.connect(self.save_value)
        hbox_trunk1.addWidget(self.checkbox5)
        self.checkbox6 = QCheckBox('Side Bending', self)
        self.checkbox6.stateChanged.connect(self.save_value)
        hbox_trunk1.addWidget(self.checkbox6)

        vbox_u_arm = QVBoxLayout()
        hbox_u_arm1 = QHBoxLayout()
        hbox_u_arm2 = QHBoxLayout()
        self.label_u_arm = QLabel("Upper Arm condition:", self)
        vbox_u_arm.addWidget(self.label_u_arm)
        # Create a QCheckBox widget
        self.checkbox7 = QCheckBox('Shoulder is raised', self)
        self.checkbox7.stateChanged.connect(self.save_value)
        hbox_u_arm1.addWidget(self.checkbox7)
        self.checkbox8 = QCheckBox('Arm is abducted', self)
        self.checkbox8.stateChanged.connect(self.save_value)
        hbox_u_arm1.addWidget(self.checkbox8)
        self.checkbox9 = QCheckBox('Arm is supported/leaning', self)
        self.checkbox9.stateChanged.connect(self.save_value)
        hbox_u_arm2.addWidget(self.checkbox9)

        vbox_wrist = QVBoxLayout()
        vbox_wrist.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.label_wrist = QLabel("Wrist condition:", self)
        vbox_wrist.addWidget(self.label_wrist)
        # Create a QCheckBox widget
        self.checkbox9_1 = QCheckBox('Bent/twisted', self)
        self.checkbox9_1.stateChanged.connect(self.save_value)
        vbox_wrist.addWidget(self.checkbox9_1)

        vbox_coupling = QVBoxLayout()
        hbox_coupling1 = QHBoxLayout()
        hbox_coupling2 = QHBoxLayout()
        self.checkbox_group_coupling = QButtonGroup(self)
        self.checkbox_group_coupling.setExclusive(True)
        self.label_coupling = QLabel("Coupling Score:", self)
        vbox_coupling.addWidget(self.label_coupling)

        # Create a QCheckBox widget
        self.checkbox9_2 = QCheckBox('Good', self)
        self.checkbox_group_coupling.addButton(self.checkbox9_2, 1)
        self.checkbox9_2.stateChanged.connect(self.save_value)
        hbox_coupling1.addWidget(self.checkbox9_2)
        self.checkbox9_3 = QCheckBox('Fair', self)
        self.checkbox_group_coupling.addButton(self.checkbox9_3, 2)
        self.checkbox9_3.stateChanged.connect(self.save_value)
        hbox_coupling1.addWidget(self.checkbox9_3, alignment=Qt.AlignmentFlag.AlignLeft)
        self.checkbox9_4 = QCheckBox('Poor', self)
        self.checkbox_group_coupling.addButton(self.checkbox9_4, 3)
        self.checkbox9_4.stateChanged.connect(self.save_value)
        hbox_coupling2.addWidget(self.checkbox9_4)
        self.checkbox9_5 = QCheckBox('Unaccceptable', self)
        self.checkbox_group_coupling.addButton(self.checkbox9_5, 4)
        self.checkbox9_5.stateChanged.connect(self.save_value)
        hbox_coupling2.addWidget(self.checkbox9_5, alignment=Qt.AlignmentFlag.AlignLeft)

        vbox_weight.addLayout(hbox_weight1)
        vbox_weight.addLayout(hbox_weight2)

        vbox_trunk.addLayout(hbox_trunk1)

        vbox_u_arm.addLayout(hbox_u_arm1)
        vbox_u_arm.addLayout(hbox_u_arm2)

        vbox_coupling.addLayout(hbox_coupling1)
        vbox_coupling.addLayout(hbox_coupling2)

        layout_h.addLayout(vbox_weight)
        layout_h.addLayout(vbox_neck)
        layout_h.addLayout(vbox_trunk)
        layout_h.addLayout(vbox_u_arm)
        layout_h.addLayout(vbox_wrist)
        layout_h.addLayout(vbox_coupling)
        # Call the function to load checkbox states
        self.load_checkbox_states()
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
    # def save_value(self):
    #     for checkbox in self.checkbox_group_weight.buttons():
    #         if checkbox.isChecked():
    #             print(f'{checkbox.text()} is checked')
    #         else:
    #             print(f'{checkbox.text()} is unchecked')
    def save_value(self):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
            'Checkbox0State': 'checked' if self.checkbox0.isChecked() else 'unchecked',
            'Checkbox1State': 'checked' if self.checkbox1.isChecked() else 'unchecked',
            'Checkbox2State': 'checked' if self.checkbox2.isChecked() else 'unchecked',
            'Checkbox3State': 'checked' if self.checkbox3.isChecked() else 'unchecked',
            'Checkbox4State': 'checked' if self.checkbox4.isChecked() else 'unchecked',
            'Checkbox5State': 'checked' if self.checkbox5.isChecked() else 'unchecked',
            'Checkbox6State': 'checked' if self.checkbox6.isChecked() else 'unchecked',
            'Checkbox7State': 'checked' if self.checkbox7.isChecked() else 'unchecked',
            'Checkbox8State': 'checked' if self.checkbox8.isChecked() else 'unchecked',
            'Checkbox9State': 'checked' if self.checkbox9.isChecked() else 'unchecked',
            'Checkbox9_1State': 'checked' if self.checkbox9_1.isChecked() else 'unchecked',
            'Checkbox9_2State': 'checked' if self.checkbox9_2.isChecked() else 'unchecked',
            'Checkbox9_3State': 'checked' if self.checkbox9_3.isChecked() else 'unchecked',
            'Checkbox9_4State': 'checked' if self.checkbox9_4.isChecked() else 'unchecked',
            'Checkbox9_5State': 'checked' if self.checkbox9_5.isChecked() else 'unchecked'
        }
        with open('config_check.ini', 'w') as configfile:
            config.write(configfile)
        print("Saved checkbox states")

    def load_checkbox_states(self):
        config = configparser.ConfigParser()
        
        # Check if the config file exists before trying to read it
        if os.path.exists('config_check.ini'):
            config.read('config_check.ini')
        
        # Load the state of each checkbox
        for checkbox_attr in dir(self):
            if checkbox_attr.startswith("checkbox") and hasattr(getattr(self, checkbox_attr), "setChecked"):
                checkbox_state = config['DEFAULT'].get(checkbox_attr + 'State', 'unchecked')
                is_checked = checkbox_state == 'checked'
                getattr(self, checkbox_attr).setChecked(is_checked)
    
    print("Loaded checkbox states")

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.config_check_path)
        
        option_values = []
        for key, value in config.items('DEFAULT'):
            if value.lower() == 'unchecked':
                option_values.append(False)
            elif value.lower() == 'checked':
                option_values.append(True)
            else:
                option_values.append(value)
        
        return option_values
    
    def on_click(self):
        file_path = self.textbox.text()
        if os.path.exists(file_path):
            self.file_path = file_path
            message = f'File exists: {self.file_path}'
            self.save_textbox_value(self.file_path)

            self.angles_dict = self.csv_to_dict(self.file_path)
            self.col_len = self.get_csv_column_length(self.file_path) 
            self.reba_arr = []

            # print("DataTF:", self.dataTF)
            # print("Angles Dict:", self.angles_dict)
            # print("Column Length:", self.col_len)

            for i in range(self.col_len):
                reba_value = self.calculate_reba(self.angles_dict, i)
                self.reba_arr.append(reba_value)
                print(f"REBA Value at {i}: {reba_value}")

            self.update_csv_column(self.file_path, self.reba_arr, 12)

            # try:
            #     self._slider.valueChanged.connect(lambda:self._frame_count_label13.setText(f"\nREBA Score: {self.arr13[self._slider.value()]}"))
            # except Exception as e:
            #     self._frame_count_label13.setText("Error")
            # print("Final Angles Dict:", self.angles_dict)
            # print("REBA Array Length:", len(self.reba_arr))
            # print("Column Length:", self.col_len)
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
        
    def get_csv_column_length(self, file_path, column_name='neck'):
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)
            
            # Check if the column exists in the DataFrame
            if column_name not in df.columns:
                raise ValueError(f"Column '{column_name}' not found in the CSV file.")
            
            # Get the length of the specified column
            column_length = len(df[column_name])
            return column_length
        except FileNotFoundError:
            print(f"Error: The file at path '{file_path}' was not found.")
            return -1
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1
        
    def update_csv_column(self, file_path, new_column_data, target_column_index=12):
        # Read the existing CSV data into a DataFrame
        df = pd.read_csv(file_path)

        # Check if the target column index is within the bounds of the DataFrame
        if target_column_index >= len(df.columns):
            raise IndexError("Target column index is out of bounds")

        # Ensure new_column_data has the same number of rows as the existing data
        if len(new_column_data) != len(df):
            raise ValueError("Length of new_column_data must match the number of rows in the CSV file")

        # Update the specific column in the DataFrame
        df.iloc[:, target_column_index] = new_column_data

        # Write the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

    def csv_to_dict(self, file_path):
        df = pd.read_csv(file_path)
        columns = {
            'neck': df['neck'].tolist(),
            'trunk': df['trunk'].tolist(),
            'upper_left_arm': df['upper_left_arm'].tolist(),
            'upper_right_arm': df['upper_right_arm'].tolist(),
            'upper_left_leg': df['upper_left_leg'].tolist(),
            'upper_right_leg': df['upper_right_leg'].tolist(),
            'lower_left_arm': df['lower_left_arm'].tolist(),
            'lower_right_arm': df['lower_right_arm'].tolist(),
            'lower_left_leg': df['lower_left_leg'].tolist(),
            'lower_right_leg': df['lower_right_leg'].tolist(),
            'left_wrist': df['left_wrist'].tolist(),
            'right_wrist': df['right_wrist'].tolist(),
            'REBA': df['REBA'].tolist()
        }
        return columns
    
    def calculate_reba(self, angles_dict, i):
        if self.dataTF[0] is True:
            if self.dataTF[11] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[12] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    1
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[13] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    2
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[14] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    3
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            else:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
        elif self.dataTF[1] is True:
            if self.dataTF[11] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    1,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[12] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    1,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    1
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[13] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    1,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    2
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[14] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    1,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    3
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            else:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
        elif self.dataTF[2] is True:
            if self.dataTF[11] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    2,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[12] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    2,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    1
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[13] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    2,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    2
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            elif self.dataTF[14] is True:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    2,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    3
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
            else:
                calc_reba = DegreetoREBA([
                    angles_dict['neck'][i], self.dataTF[3], self.dataTF[4], 
                    angles_dict['trunk'][i], self.dataTF[5], self.dataTF[6], 
                    angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                    0,
                    angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], self.dataTF[7], self.dataTF[8], self.dataTF[9],
                    angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                    angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], self.dataTF[10],
                    0
                    ])
                score_res = calc_reba.reba_computation()
                return score_res
        else:
            #print("Asumming all limbs condition doesn't require adjustments since initial weight isn't checked")
            calc_reba = DegreetoREBA([
                        angles_dict['neck'][i], False, False, 
                        angles_dict['trunk'][i], False, False, 
                        angles_dict['lower_right_leg'][i], angles_dict['lower_left_leg'][i],
                        False,
                        angles_dict['upper_right_arm'][i], angles_dict['upper_left_arm'][i], False, False, False,
                        angles_dict['lower_right_arm'][i], angles_dict['lower_left_arm'][i],
                        angles_dict['left_wrist'][i], angles_dict['right_wrist'][i], False,
                        0
                        ])
            score_res = calc_reba.reba_computation()
            return score_res