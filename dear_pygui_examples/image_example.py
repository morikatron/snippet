import dearpygui.dearpygui as dpg


def open_window(sender, app_data, user_data):
    dpg.show_item("Using add_image()")
    dpg.show_item("Using draw_image()")


dpg.create_context()

with dpg.texture_registry():
    width, height, channels, data = dpg.load_image("image_button.png")
    dpg.add_static_texture(width, height, data, tag="image_button")

    width, height, channels, data = dpg.load_image("sample_image.jpg")
    dpg.add_static_texture(width, height, data, tag="texture_tag")

with dpg.window(label="Using add_image()", tag="Using add_image()", show=False):
    dpg.add_image("texture_tag", label="Image", tag="Image")

with dpg.window(label="Using draw_image()", tag="Using draw_image()", pos=[100, 100], show=False):
    with dpg.drawlist(width=width, height=height):
        dpg.draw_image("texture_tag", (0, 0), (width, height))

with dpg.window(tag="Main Window", label="Main Window"):
    dpg.add_image_button("image_button", width=32, height=32, callback=open_window)

dpg.create_viewport(title='Image Example', width=800, height=600)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
