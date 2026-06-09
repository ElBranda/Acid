import sys
import src.documentador as d
from src.gui.app import launch_gui

def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
        d.printer(path)
    else:
        launch_gui()

if __name__ == "__main__":
    main()