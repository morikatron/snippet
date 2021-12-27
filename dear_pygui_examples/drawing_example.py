import dearpygui.dearpygui as dpg

def update_layer_state(sender, app_data, user_data: str):
    is_show = dpg.get_value(sender)
    dpg.configure_item(user_data, show=is_show)

def update_drawing(sender, app_data, user_data):
    center = dpg.get_value("Center")
    radius = dpg.get_value("Radius")
    color = dpg.get_value("Color")
    dpg.configure_item("Circle", center=center, radius=radius, color=color)

dpg.create_context()

width, height, channels, data = dpg.load_image("sample_image.jpg")

with dpg.texture_registry():
    dpg.add_static_texture(width, height, data, tag="texture_tag")

with dpg.window(tag="Main Window", label="Main Window"):
    dpg.add_slider_intx(label="pos", tag="Center", min_value=0, max_value=600, default_value=[100, 100], size=2,
                        callback=update_drawing)
    dpg.add_slider_float(label="Radius", tag="Radius", min_value=0, max_value=100, default_value=20,
                         callback=update_drawing)
    dpg.add_color_edit(label="Color", tag="Color", default_value=[0, 255, 255], callback=update_drawing)
    with dpg.group(horizontal=True):
        dpg.add_text("Layer: ")
        dpg.add_checkbox(label="BG", default_value=True, callback=update_layer_state, user_data="Background")
        dpg.add_checkbox(label="Layer_1", default_value=True, callback=update_layer_state, user_data="Layer1")
        dpg.add_checkbox(label="Layer_2", default_value=True, callback=update_layer_state, user_data="Layer2")

    dpg.add_separator()

    with dpg.drawlist(width=width, height=height):
        with dpg.draw_layer(tag="Background"):
            dpg.draw_image("texture_tag", (0, 0), (width, height))

        with dpg.draw_layer(tag="Layer1"):
            dpg.draw_text([50, 300], "Layer1 Text", tag="Text Layer1", color=[0, 0, 255], size=15)
            dpg.draw_rectangle([0, 0], [100, 100], tag="Rectangle", color=[255, 255, 0], thickness=1)
            dpg.draw_circle(center=dpg.get_value("Center"), radius=dpg.get_value("Radius"), color=dpg.get_value("Color"),
                            tag="Circle", thickness=2)
            dpg.draw_line([10, 10], [100, 100], tag="Line", color=[255, 0, 0], thickness=1)
            dpg.draw_triangle([300, 500], [200, 200], [500, 200], tag="Triangle", color=[255, 255, 0], thickness=3)
        with dpg.draw_layer(tag="Layer2"):
            dpg.draw_text([50, 320], "Layer2 Text", tag="Text Layer2", color=[255, 0, 0], size=15)
            dpg.draw_rectangle([100, 0], [200, 100], tag="Rectangle Layer2", color=[255, 255, 0], fill=[0, 0, 255],
                               thickness=1)
            dpg.draw_polygon([[363, 471], [100, 498], [450, 220]], tag="Polygon", color=[255, 125, 0], fill=[255, 125, 0])
            dpg.draw_polyline([[300, 500], [200, 200], [500, 700]], tag="PolyLine", color=[125, 255, 0], thickness=2)
            dpg.draw_arrow([50, 70], [100, 65], tag="Arrow", color=[0, 200, 255], thickness=1, size=10)

dpg.create_viewport(title='Drawing Example', width=width, height=height+150)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
