import dearpygui.dearpygui as dpg


def open_file(sender, app_data, user_data):
    with dpg.file_dialog(default_filename="file_example", callback=apply_selected_directory):
        dpg.add_file_extension(".py")
        dpg.add_file_extension(".gif")


def apply_selected_directory(sender, app_data, user_data):
    print(app_data)
    dpg.set_value("File Path", app_data["file_path_name"])


dpg.create_context()

with dpg.window(label="Main Window", tag="Main Window"):
    with dpg.menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Open", callback=open_file)
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="File Path")
        dpg.add_button(label="Select File", callback=open_file)

dpg.create_viewport(title=f"File Example", width=640, height=800)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
