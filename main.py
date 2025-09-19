import tkinter as tk
from views.gui import FarmManagementApp   # type: ignore

def main():
    root = tk.Tk()
    app = FarmManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()