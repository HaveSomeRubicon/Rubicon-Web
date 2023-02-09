import os
import sys
import PyQt5.uic


clear = lambda: os.system("clear||cls")

def ui_to_py():
    PyQt5.uic.compileUiDir("rubicon_web", recurse=True)


def delete_compiled_ui_files():
    dir_name = os.getcwd()

    for root, dir, dirs in os.walk(dir_name):
        for dir in dirs:
            if dir.startswith("Ui_") and dir.endswith(".py"):
                try:
                    os.remove(os.path.join(root, dir))
                except OSError:
                    pass


def recompile_ui_files():
    delete_compiled_ui_files()
    ui_to_py()


def get_user_input():
    options = (
        ("1", "Compile all .ui files to .py files", ui_to_py),
        ("2", "Delete all compiled .ui files", delete_compiled_ui_files),
        ("3", "Recompile all .ui files", recompile_ui_files),
        ("4", "Quit this program", sys.exit),
    )
    options_indexes = [option[0] for option in options]
    
    clear()
    for option in options:
        print(f"{option[0]}: {option[1]}")
    selected_option = input("\nSelect an option number and press enter: ")
    
    if not selected_option in options_indexes:
        clear()
        input("That option does not exist! Press enter to try again.")
        get_user_input()
        return
    
    clear()
    options[int(selected_option) - 1][2]()
    input("The task was successfully completed. Press enter to continue.")
    get_user_input()

if __name__ == "__main__":
    get_user_input()