# pyuic5 -x interfaceCal.ui -o ui_interfaceCal.py
# pyrcc5 ressources.qrc -o ressources_rc.py
import sys
import json
import os
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
from Gui.ui_interfaceCal import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setupCalculator()
        self.addScientificButtons()
        self.applyStyles()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def applyStyles(self):
        """Apply a more premium look using CSS."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121212;
            }
            QPushButton {
                background-color: #1e1e1e;
                color: #ffffff;
                border: none;
                border-radius: 10px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
                min-height: 50px;
            }
            QPushButton:hover {
                background-color: #333333;
            }
            QPushButton:pressed {
                background-color: #444444;
            }
            QPushButton[scientific="true"] {
                background-color: #1a1a1a;
                color: #00a8ff;
                font-size: 14px;
            }
            QPushButton#btn1, QPushButton#btn2, QPushButton#btn3, 
            QPushButton#btn4, QPushButton#btn5, QPushButton#btn6, 
            QPushButton#btn7, QPushButton#btn8, QPushButton#btn9, QPushButton#btn0 {
                font-size: 24px;
                background-color: #252525;
            }
            QPushButton#btnEvaluate {
                background-color: #0078d4;
                color: white;
                font-size: 24px;
            }
            QPushButton#btnEvaluate:hover {
                background-color: #0086f0;
            }
            QPushButton#btnAdd, QPushButton#btnSubtract, QPushButton#btnMultiply, QPushButton#btnDivide {
                background-color: #2d2d2d;
                color: #00a8ff;
                font-size: 22px;
            }
            QPushButton#btnAC, QPushButton#btnC {
                background-color: #2d2d2d;
                color: #ff5e5e;
            }
            QLabel#calcLabel {
                color: #ffffff;
                background: transparent;
                padding: 10px;
                font-size: 48px;
                font-family: 'Segoe UI Light', sans-serif;
            }
            QTextEdit#textEdit_HC {
                background-color: #0d0d0d;
                color: #666666;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
            }
        """)

    def addScientificButtons(self):
        """Add scientific buttons to the left and right of the main grid."""
        sci_left = [
            ('sin', 'math.sin(math.radians({x}))'),
            ('cos', 'math.cos(math.radians({x}))'),
            ('tan', 'math.tan(math.radians({x}))'),
            ('√', 'math.sqrt({x})'),
            ('ln', 'math.log({x})'),
        ]
        sci_right = [
            ('log', 'math.log10({x})'),
            ('1/x', '1/({x})'),
            ('π', 'math.pi'),
            ('e', 'math.e'),
            ('x²', '({x})**2'),
        ]
        
        layout = self.ui.gridLayout
        # Expand labels to span across 6 columns (0 to 5)
        layout.addWidget(self.ui.textEdit_HC, 1, 0, 1, 6)
        layout.addWidget(self.ui.calcLabel, 2, 0, 1, 6)

        for i, (label, func) in enumerate(sci_left):
            btn = QPushButton(label)
            btn.setProperty("scientific", "true")
            btn.clicked.connect(lambda _, f=func: self.calculator.apply_sci_function(f))
            layout.addWidget(btn, 4 + i, 0) 

        for i, (label, func) in enumerate(sci_right):
            btn = QPushButton(label)
            btn.setProperty("scientific", "true")
            btn.clicked.connect(lambda _, f=func: self.calculator.apply_sci_function(f))
            layout.addWidget(btn, 4 + i, 5) 

    def setupCalculator(self):
        self.calculator = Calculator(self.ui)

        # Connect digit buttons
        for i in range(10):
            button = getattr(self.ui, f"btn{i}")
            button.clicked.connect(lambda _, num=str(i): self.calculator.func_button_num(num))

        # Connect operator buttons
        self.ui.btnAdd.clicked.connect(lambda: self.calculator.func_button_flag('+'))
        self.ui.btnMultiply.clicked.connect(lambda: self.calculator.func_button_flag('*'))
        self.ui.btnDivide.clicked.connect(lambda: self.calculator.func_button_flag('/'))
        self.ui.btnSubtract.clicked.connect(lambda: self.calculator.func_button_flag('-'))

        self.ui.btnPoint.clicked.connect(self.calculator.func_button_dot)
        self.ui.btnAC.clicked.connect(self.calculator.clear_all)
        self.ui.btnC.clicked.connect(self.calculator.clear)
        self.ui.btnEvaluate.clicked.connect(self.calculator.evaluate)

    def keyPressEvent(self, event):
        key = event.text()
        if key in "0123456789":
            self.calculator.func_button_num(key)
        elif key in "+-*/":
            self.calculator.func_button_flag(key)
        elif key in ".,":
            self.calculator.func_button_dot()
        elif event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return or key == "=":
            self.calculator.evaluate()
        elif event.key() == Qt.Key.Key_Backspace:
            self.calculator.clear()
        elif event.key() == Qt.Key.Key_Escape:
            self.calculator.clear_all()


class Calculator:
    HISTORY_FILE = "history.json"

    def __init__(self, ui):
        self.ui = ui
        # Explicitly initialize to avoid lint errors
        self.equation_completed = False
        self.operator_selected = False
        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''
        self.reset_state()
        self.load_history()

    def reset_state(self):
        self.equation_completed = False
        self.operator_selected = False
        self.first_number = ''
        self.second_number = ''
        self.operator = ''
        self.result = ''
        self.ui.calcLabel.setText('0')

    def clear_all(self):
        self.reset_state()

    def clear(self):
        if self.equation_completed:
            self.reset_state()
            return
            
        if self.second_number:
            self.second_number = self.second_number[:-1]
        elif self.operator_selected:
            self.operator_selected = False
            self.operator = ''
        elif self.first_number:
            self.first_number = self.first_number[:-1]
            
        self.update_display()

    def update_display(self):
        if not self.operator_selected:
            display_text = self.first_number or '0'
        else:
            display_text = f"{self.first_number} {self.operator} {self.second_number}"
        self.ui.calcLabel.setText(display_text)

    def func_button_num(self, num):
        if self.equation_completed:
            self.reset_state()

        if not self.operator_selected:
            self.first_number += num
        else:
            self.second_number += num
        self.update_display()

    def func_button_flag(self, operator):
        if self.equation_completed:
            self.first_number = self.result
            self.second_number = ''
            self.equation_completed = False
        
        if self.first_number == '':
            if operator == '-':
                self.first_number = '-'
                self.update_display()
                return
            else:
                self.first_number = '0'

        self.operator = operator
        self.operator_selected = True
        self.update_display()

    def func_button_dot(self):
        target = self.second_number if self.operator_selected else self.first_number
        if '.' not in target:
            if not target or target == '-':
                target += '0.'
            else:
                target += '.'
            
            if self.operator_selected:
                self.second_number = target
            else:
                self.first_number = target
                
        self.update_display()

    def evaluate(self):
        if not self.operator_selected or not self.second_number:
            return

        try:
            expr = f"{self.first_number} {self.operator} {self.second_number}"
            cleaned_expr = expr.replace('X', '*').replace('÷', '/')
            
            res_val = eval(cleaned_expr, {"__builtins__": None}, {"math": math})
            self.display_result(res_val, expr)
            
        except ZeroDivisionError:
            self.ui.calcLabel.setText("Error: Div by 0")
        except Exception:
            self.ui.calcLabel.setText("Error")

    def apply_sci_function(self, func_template):
        """Apply a scientific function like sin(x) to the current number."""
        try:
            current = self.second_number if self.operator_selected else (self.first_number or '0')
            if current == '-':
                current = '0'
            
            # If it's a constant
            if '{x}' not in func_template:
                val = eval(func_template, {"__builtins__": None}, {"math": math})
                if self.operator_selected:
                    self.second_number = str(val)
                else:
                    self.first_number = str(val)
                self.update_display()
                return

            expr = func_template.replace('{x}', current)
            res_val = eval(expr, {"__builtins__": None}, {"math": math})
            
            if self.operator_selected:
                self.second_number = f"{res_val:.8g}"
            else:
                self.first_number = f"{res_val:.8g}"
                
            self.update_display()
        except Exception:
            self.ui.calcLabel.setText("Math Error")

    def display_result(self, res_val, original_expr):
        if isinstance(res_val, float):
            if res_val.is_integer():
                self.result = str(int(res_val))
            else:
                self.result = f"{res_val:.8g}"
        else:
            self.result = str(res_val)

        self.ui.calcLabel.setText(self.result)
        
        calculation = f"{original_expr} = {self.result}"
        self.ui.textEdit_HC.append(calculation)
        self.save_history_entry(calculation)
        
        self.equation_completed = True

    def load_history(self):
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, 'r') as f:
                    history = json.load(f)
                    for entry in history:
                        self.ui.textEdit_HC.append(entry)
            except Exception:
                pass

    def save_history_entry(self, entry):
        history = []
        if os.path.exists(self.HISTORY_FILE):
            try:
                with open(self.HISTORY_FILE, 'r') as f:
                    history = json.load(f)
            except Exception:
                pass
        
        history.append(entry)
        history = history[-100:]
        try:
            with open(self.HISTORY_FILE, 'w') as f:
                json.dump(history, f, indent=4)
        except Exception:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
