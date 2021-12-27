import dearpygui.dearpygui as dpg

dpg.create_context()

# callback
def retrieve_callback(sender, app_data, user_data):
    print(f"Regular: {dpg.get_value('InputTextRegular')}")
    print(f"With Hint: {dpg.get_value('InputTextWithHint')}")
    print(f"No Spaces: {dpg.get_value('InputTextNoSpaces')}")
    print(f"Uppercase: {dpg.get_value('InputTextUppercase')}")
    print(f"Decimal Only: {dpg.get_value('InputTextDecimal')}")
    print(f"Hexadecimal Only: {dpg.get_value('InputTextHexadecimal')}")
    print(f"Read Only: {dpg.get_value('InputTextReadOnly')}")
    print(f"Password: {dpg.get_value('InputTextPassword')}")
    print(f"Multiline: {dpg.get_value('InputTextMultiline')}")
    print(f"Scientific: {dpg.get_value('InputTextScientific')}")
    print(f"On Enter: {dpg.get_value('InputTextOnEnter')}")


with dpg.window(tag="Main Window", label="Main Window"):
    dpg.add_text("This example demonstrates the input text widget.", bullet=True)
    dpg.add_text("Press the 'Retrieve' button to display the input values in the logger", wrap=500, bullet=True)

    dpg.add_input_text(label="Regular", tag="InputTextRegular")
    dpg.add_input_text(label="WithHint", tag="InputTextWithHint", hint="A hint")
    dpg.add_input_text(label="No Spaces", tag="InputTextNoSpaces", no_spaces=True)
    dpg.add_input_text(label="Uppercase", tag="InputTextUppercase", uppercase=True)
    dpg.add_input_text(label="Decimal Only", tag="InputTextDecimal", decimal=True)
    dpg.add_input_text(label="Hexadecimal Only", tag="InputTextHexadecimal", hexadecimal=True)
    dpg.add_input_text(label="Read Only", tag="InputTextReadOnly", readonly=True, default_value="Read Only")
    dpg.add_input_text(label="Password", tag="InputTextPassword", password=True)
    dpg.add_input_text(label="Multiline", tag="InputTextMultiline", multiline=True)
    dpg.add_input_text(label="Scientific", tag="InputTextScientific", scientific=True)
    dpg.add_input_text(label="On Enter", tag="InputTextOnEnter", on_enter=True)

    dpg.add_button(label="Retrieve", callback=retrieve_callback)

dpg.create_viewport(title=f"Input Text Example", width=500, height=500)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
