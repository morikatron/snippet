import dearpygui.dearpygui as dpg
import time


# callback
def retrieve_values(sender, app_data, user_data):
    print("args:")
    print(f" - sender: {sender}")
    print(f" - app_data: {app_data}")
    print(f" - user_data: {user_data}")

    print(f"Checkbox: {dpg.get_value('Checkbox')}")
    print(f"Combo: {dpg.get_value('Combo')}")
    print(f"Radio Button: {dpg.get_value('Radio Button')}")
    print(f"Listbox: {dpg.get_value('Listbox')}")
    print(f"Progress Bar: {dpg.get_value('Progress Bar')}")
    print(f"Selectable: {dpg.get_value('Selectable')}")
    print(f"Input Text: {dpg.get_value('Input Text')}")
    print(f"Input Float: {dpg.get_value('Input Float')}")
    print(f"Input Float X: {dpg.get_value('Input Float 3')}")
    print(f"Input Int: {dpg.get_value('Input Int')}")
    print(f"Input Int X: {dpg.get_value('Input Int 3')}")
    print(f"Drag Float: {dpg.get_value('Drag Float')}")
    print(f"Drag Float X: {dpg.get_value('Drag Float 3')}")
    print(f"Drag Int: {dpg.get_value('Drag Int')}")
    print(f"Drag Int X: {dpg.get_value('Drag Int 3')}")
    print(f"Slider Float: {dpg.get_value('Slider Float')}")
    print(f"Slider FloatX: {dpg.get_value('Slider Float 3')}")
    print(f"Slider Int: {dpg.get_value('Slider Int')}")
    print(f"Slider Int X: {dpg.get_value('Slider Int 3')}")
    print(f"Color Edit: {dpg.get_value('Color Edit')}")
    print(f"Color Picker: {dpg.get_value('Color Picker')}")
    print(f"Color Picker with Alpha: {dpg.get_value('Color Picker with Alpha')}")
    print(f"Tab Bar: {dpg.get_value('Tab Bar')}")


def get_date(sender, app_data, user_data: str):
    date = dpg.get_value(sender)
    weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    dpg.set_value(user_data, f"Date: {date['year']+1900}/{date['month']+1}/{date['month_day']} ({weekday[date['week_day']]})")


def get_time(sender, app_data, user_data: str):
    time = dpg.get_value(sender)
    dpg.set_value(user_data, f"Time: {time['hour']}:{time['min']}:{time['sec']}")

dpg.create_context()

with dpg.window(tag="Main Window", label="Main Window"):

    with dpg.menu_bar():
        with dpg.menu(label="Menu"):
            dpg.add_menu_item(label="Menu Item 1")
        dpg.add_menu_item(label="Menu Item 2")

    dpg.add_button(label="Get Widget Values", callback=retrieve_values, user_data="User Data Example")

    with dpg.tab_bar(label="Tab_Bar", tag="Tab Bar"):
        with dpg.tab(label="Basic Widgets", tag="Basic Widgets"):

            dpg.add_button(label="Button", tag="Button")
            dpg.add_color_button([255, 128, 0, 255], label="Color Button", tag="Color Button")
            dpg.add_checkbox(label="Checkbox", tag="Checkbox")
            dpg.add_combo(label="Combo", items=["Item 1", "Item 2", "item 3"])
            dpg.add_radio_button(label="Radio Button", tag="Radio Button", items=["Item 1", "Item 2", "item 3"])
            dpg.add_listbox(label="Listbox", tag="Listbox", items=["Item 1", "Item 2", "item 3"])
            dpg.add_progress_bar(tag="Progress Bar", default_value=0.45, overlay="Progress Bar")

            dpg.add_text("Text")
            dpg.add_selectable(label="Selectable", tag="Selectable")
            dpg.add_input_text(label="Input Text", tag="Input Text", default_value="default value")

            dpg.add_color_edit(label="Color Edit", tag="Color Edit")
            dpg.add_color_picker(label="Color Picker", tag="Color Picker", width=300)
            dpg.add_color_picker(label="Color Picker with Alpha", tag="Color Picker with Alpha", alpha_bar=True, width=300)

            dpg.add_separator()

            dpg.add_input_float(label="Input Float", tag="Input Float")
            dpg.add_input_floatx(label="Input Float X(size=3)", tag="Input Float 3", size=3)
            dpg.add_input_int(label="Input Int", tag="Input Int")
            dpg.add_input_intx(label="Input Int X(size=3)", tag="Input Int 3", size=3)

            dpg.add_drag_float(label="Drag Float", tag="Drag Float")
            dpg.add_drag_floatx(label="Drag Float X(size=3)", tag="Drag Float 3", size=3)
            dpg.add_drag_int(label="Drag Int", tag="Drag Int")
            dpg.add_drag_intx(label="Drag Int X(size=3)", tag="Drag Int 3", size=3)

            dpg.add_slider_float(label="Slider Float", tag="Slider Float")
            dpg.add_slider_floatx(label="Slider Float X(size=3)", tag="Slider Float 3", size=3)
            dpg.add_slider_int(label="Slider Int", tag="Slider Int")
            dpg.add_slider_intx(label="Slider Int X(size=3)", tag="Slider Int 3", size=3)

            dpg.add_knob_float(label="Knob Float", tag="Knob Float")

            with dpg.group(horizontal=True):
                dpg.add_date_picker(label="Date Picker", tag="Date Picker", callback=get_date, user_data="Date",
                                    default_value={"month_day": 1, "month": 0, "year": 122})
                dpg.add_time_picker(label="Time Picker", tag="Time Picker", callback=get_time, user_data="Time",
                                    default_value={"hour": 0, "min": 0, "sec": 0}, hour24=True)
                with dpg.group(horizontal=False):
                    dpg.add_text(tag="Date", default_value="Date:")
                    dpg.add_text(tag="Time", default_value="Time:")
        with dpg.tab(label="Container Widgets", tag="Container Widgets"):

            with dpg.tree_node(label="Tree Node 1", tag="Tree Node 1"):
                for i in range(0, 3):
                    dpg.add_text(f"Item {i}")
            with dpg.tree_node(label="Tree Node 2", tag="Tree Node 2"):
                for i in range(0, 3):
                    dpg.add_text(f"Item {i}")

            with dpg.collapsing_header(label="Collapsing Header", tag="Collapsing Header"):
                for i in range(0, 10):
                    dpg.add_text(f"Item {i} belonging to a collapsing header")

            with dpg.group(horizontal=True):
                with dpg.child_window(label="Child Window", tag="Child Window", width=220, height=100):
                    for i in range(0, 10):
                        dpg.add_text(f"Item {i} belonging to a child")

                with dpg.group(label="Group", tag="Group"):
                    dpg.add_text("Group")
                    for i in range(0, 3):
                        dpg.add_button(label=f"Button {i}", tag=f"Button {i}")

        with dpg.tab(label="Tables", tag="Tables"):
            with dpg.table(label="Table", header_row=False, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                           borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):

                dpg.add_table_column(label="Header 1")
                dpg.add_table_column(label="Header 2")
                dpg.add_table_column(label="Header 3")

                for i in range(0, 4):
                    with dpg.table_row():
                        for j in range(0, 3):
                            dpg.add_text(f"Row{i} Column{j}")

        with dpg.tab(label="Loading", tag="Loading"):

            def loading_callback(sender, app_data, user_data: int):
                if not dpg.does_item_exist("Loading Window"):
                    with dpg.window(label="Loading Window", tag="Loading Window", width=200, no_resize=True, no_move=True, no_close=True):
                        dpg.add_text("Now Loading")
                        dpg.add_loading_indicator()

                    time.sleep(user_data)
                    dpg.delete_item("Loading Window")

            dpg.add_button(label="Wait 3 Seconds", callback=loading_callback, user_data=3)

dpg.create_viewport(title=f"Widget Example", width=800, height=600)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
