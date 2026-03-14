# 🧮 Advanced PyQt5 Calculator

[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt-5-green.svg)](https://pypi.org/project/PyQt5/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A modern, feature-rich scientific calculator built with **Python** and **PyQt5**. This application combines a sleek dark-themed interface with advanced mathematical capabilities and persistent calculation history.

---

## ✨ Features

- **Basic Operations**: Addition, Subtraction, Multiplication, Division.
- **Scientific Functions**: 
  - Trigonometry: `sin`, `cos`, `tan` (degree-based).
  - Logarithms: `ln` (natural), `log` (base 10).
  - Power & Roots: `x²`, `√` (square root).
  - Constants: `π` (Pi), `e` (Euler's number).
  - Others: `1/x` (inverse).
- **Persistent History**: Stores your last 100 calculations in a `history.json` file, automatically reloaded on startup.
- **Modern UI**: Custom CSS styling with a premium dark mode, responsive button layout, and elegant typography.
- **Keyboard Support**: Full support for number keys, basic operators, `Enter` for equals, and `Backspace` for clearing.
- **Robust Error Handling**: Handles division by zero and invalid mathematical expressions gracefully.

---

## 📸 Screenshots

| Modern Interface | Scientific Panel |
| :---: | :---: |
| ![Main UI](Gui/1.jpg) | ![Features](Gui/2.jpg) |

---

## 🚀 Installation

### 1. Requirements

- Python 3.10 or higher
- **PyQt6**

### 2. Install Dependencies

```bash
pip install PyQt6
```

### 3. Clone the Repository
```bash
git clone https://github.com/bjyoucef/Calculator_using_PyQt5_in_Python.git
cd Calculator_using_PyQt5_in_Python
```

### 4. Run the Application
```bash
python main.py
```

---

## ⌨️ Keyboard Shortcuts

| Key | Action |
| :--- | :--- |
| `0-9` | Input Numbers |
| `+`, `-`, `*`, `/` | Basic Operators |
| `.` or `,` | Decimal Point |
| `Enter` / `=` | Evaluate Expression |
| `Backspace` | Clear Last Character |
| `Esc` | Clear All (AC) |

---

## 🛠️ Built With

- **Python**: Core logic.
- **PyQt5**: GUI Framework.
- **JSON**: Persistent storage for history.
- **Math**: Advanced arithmetic functions.

---

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📜 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

**Developed with ❤️ by [bjyoucef](https://github.com/bjyoucef)**
