import dearpygui.dearpygui as dpg
import tkinter
import tkinter.filedialog as filedialog


def open_file(sender, app_data, user_data):
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    dpg.set_value("File Path", file_path)


dpg.create_context()

with dpg.window(label="Main Window", tag="Main Window"):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open", callback=open_file)
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="File Path")
        dpg.add_button(label="Select File", callback=open_file)

dpg.create_viewport(title=f"File Example", width=800, height=600)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
