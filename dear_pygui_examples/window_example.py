import dearpygui.dearpygui as dpg


def window_editor(sender, app_data, user_data):
    if dpg.does_item_exist("Test Window"):
        dpg.configure_item(
            "Test Window",
            width=dpg.get_value("Width"),
            height=dpg.get_value("Height"),
            pos=[dpg.get_value("Start x"), dpg.get_value("Start y")],
            autosize=dpg.get_value("No Autosize"),
            no_resize=dpg.get_value("No Resizable"),
            no_title_bar=dpg.get_value("No Title bar"),
            no_move=dpg.get_value("No Movable"),
            no_scrollbar=dpg.get_value("No Scroll bar"),
            no_collapse=dpg.get_value("No Collapse"),
            horizontal_scrollbar=dpg.get_value("Horizontal Scrollbar"),
            no_focus_on_appearing=dpg.get_value("No Focus on Appearing"),
            no_bring_to_front_on_focus=dpg.get_value("No Bring To Front on Focus"),
            menubar=dpg.get_value("Menubar"),
            no_close=dpg.get_value("No Close"),
            label=dpg.get_value("Label"))
    else:
        print("window does not exists")


def create_window():
    if dpg.does_item_exist("Test Window"):
        print("window already exists")
    else:
        with dpg.window(
                tag="Test Window",
                width=dpg.get_value("Width"),
                height=dpg.get_value("Height"),
                pos=[dpg.get_value("Start x"), dpg.get_value("Start y")],
                autosize=dpg.get_value("No Autosize"),
                no_resize=dpg.get_value("No Resizable"),
                no_title_bar=dpg.get_value("No Title bar"),
                no_move=dpg.get_value("No Movable"),
                no_scrollbar=dpg.get_value("No Scroll bar"),
                no_collapse=dpg.get_value("No Collapse"),
                horizontal_scrollbar=dpg.get_value("Horizontal Scrollbar"),
                no_focus_on_appearing=dpg.get_value("No Focus on Appearing"),
                no_bring_to_front_on_focus=dpg.get_value("No Bring To Front on Focus"),
                menubar=dpg.get_value("Menubar"),
                no_close=dpg.get_value("No Close"),
                label=dpg.get_value("Label"),
                on_close=on_window_close):

            for i in range(0, 5):
                dpg.add_button(label=f"button_{i}", tag=f"button_{i}")


def on_window_close(sender, app_data, user_data):
    # workaround
    children_dict = dpg.get_item_children(sender)
    for key in children_dict.keys():
        for child in children_dict[key]:
            dpg.delete_item(child)

    dpg.delete_item(sender)
    print("window was deleted")


dpg.create_context()

with dpg.window(tag="Main Window", label="Main Window"):
    dpg.add_input_text(label="Label", tag="Label", default_value="Test Window", callback=window_editor)
    dpg.add_slider_int(label="Width", tag="Width", default_value=400, min_value=-1, max_value=700, callback=window_editor)
    dpg.add_slider_int(label="Height", tag="Height", default_value=300, min_value=-1, max_value=700, callback=window_editor)
    dpg.add_slider_int(label="Start x", tag="Start x", default_value=150, min_value=-1, max_value=700, callback=window_editor)
    dpg.add_slider_int(label="Start y", tag="Start y", default_value=150, min_value=-1, max_value=700, callback=window_editor)
    dpg.add_button(label="Create New Window", tag="Create New Window", callback=create_window)
    dpg.add_checkbox(label="No Autosize", tag="No Autosize", callback=window_editor)
    dpg.add_checkbox(label="No Resizable", tag="No Resizable", callback=window_editor)
    dpg.add_checkbox(label="No Movable", tag="No Movable", callback=window_editor)
    dpg.add_checkbox(label="No Title bar", tag="No Title bar", callback=window_editor)
    dpg.add_checkbox(label="Menubar", tag="Menubar", callback=window_editor)
    dpg.add_checkbox(label="No Collapse", tag="No Collapse", callback=window_editor)
    dpg.add_checkbox(label="No Close", tag="No Close", callback=window_editor)
    dpg.add_checkbox(label="No Scroll bar", tag="No Scroll bar", callback=window_editor)
    dpg.add_checkbox(label="Horizontal Scrollbar", tag="Horizontal Scrollbar", callback=window_editor)
    dpg.add_checkbox(label="No Focus on Appearing", tag="No Focus on Appearing", default_value=True, callback=window_editor)
    dpg.add_checkbox(label="No Bring To Front on Focus", tag="No Bring To Front on Focus", callback=window_editor)

create_window()

dpg.create_viewport(title=f"Window Example", width=640, height=480)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
