import dearpygui.dearpygui as dpg
from math import cos, sin


def plot_callback(sender, app_data, user_data):
    data1x = []
    data1y = []
    for i in range(0, 100):
        data1x.append(3.14 * i / 180)
        data1y.append(cos(3 * 3.14 * i / 180))

    data2x = []
    data2y = []
    for i in range(0, 100):
        data2x.append(3.14 * i / 180)
        data2y.append(sin(2 * 3.14 * i / 180))

    dpg.add_plot_axis(dpg.mvXAxis, label="x", parent="Plot")
    y = dpg.add_plot_axis(dpg.mvYAxis, label="y", parent="Plot")
    dpg.add_line_series(x=data1x, y=data1y, parent=y, label="Cos")
    dpg.add_shade_series(x=data1x, y1=data1y, parent=y, label="Cos Area")
    dpg.add_scatter_series(data2x, data2y, parent=y, label="Sin")


dpg.create_context()

with dpg.window(label="Main Window", tag="Main Window"):
    dpg.add_text("Tips")
    dpg.add_text("Double click plot to scale to data", bullet=True)
    dpg.add_text("Right click and drag to zoom to an area", bullet=True)
    dpg.add_text("Double click to open settings", bullet=True)
    dpg.add_text("Toggle data sets on the legend to hide them", bullet=True)
    dpg.add_text("Click and drag in the plot area to pan", bullet=True)
    dpg.add_text("Scroll mouse wheel in the plot area to zoom", bullet=True)
    dpg.add_text("Click and drag on an axis to just pan that dimension", bullet=True)
    dpg.add_text("Scroll mouse wheel on an axis to just scale that dimension", bullet=True)
    dpg.add_button(label="Plot data", callback=plot_callback)
    dpg.add_plot(label="Plot", tag="Plot", height=300)

    with dpg.plot(tag="Pie Chart", label="Pie Chart", width=300, height=300):
        labels = ["A", "B", "C", "D"]
        values = [10, 20, 30, 40]

        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True)
        dpg.set_axis_limits(dpg.last_item(), 0, 1)
        with dpg.plot_axis(dpg.mvYAxis, no_gridlines=True, no_tick_marks=True, no_tick_labels=True):
            dpg.set_axis_limits(dpg.last_item(), 0, 1)
            dpg.add_pie_series(0.5, 0.5, radius=0.5, values=values, labels=labels, format="%.0f", normalize=True)


dpg.create_viewport(title=f"Plot Example", width=800, height=600)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
