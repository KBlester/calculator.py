import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from ui import CalculatorUI


def main():
    root = tk.Tk()
    app = CalculatorUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
