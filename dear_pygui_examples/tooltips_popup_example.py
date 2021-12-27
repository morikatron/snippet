import dearpygui.dearpygui as dpg


dpg.create_context()

with dpg.window(label="Main Window", tag="Main Window"):
    dpg.add_button(label="Hover me", tag="Tooltip Parent")
    with dpg.tooltip(parent="Tooltip Parent"):
        dpg.add_text("Tooltips")

    dpg.add_button(label="Modal Popup")
    with dpg.popup(parent=dpg.last_item(), tag="ModalPopup", modal=True, mousebutton=dpg.mvMouseButton_Left):
        dpg.add_text("Popup(Modal=True)")

    dpg.add_text("Right Click This Text")
    with dpg.popup(parent=dpg.last_item()):
        dpg.add_text("Popup(Modal=False)")

dpg.create_viewport(title=f"Tooltips and Popup Example", width=640, height=480)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
