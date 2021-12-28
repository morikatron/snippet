import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.font_registry():
    with dpg.font(file="./resources/Noto_Sans_JP/NotoSansJP-Medium.otf", size=20) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
    dpg.bind_font(default_font)
    with dpg.font(file="./resources/Noto_Sans_JP/NotoSansJP-Bold.otf", size=14) as small_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)

with dpg.window(label="Main Window", tag="Main Window"):
    dpg.add_text("フォントの設定を行うと日本語が表示できます")
    dpg.add_separator()
    with dpg.group(tag="license"):
        dpg.add_text("本プログラムでは表示フォントに「Noto Sans JP」(https://fonts.google.com/noto/specimen/Noto+Sans+JP) を使用しています。")
        dpg.add_text("Licensed under SIL Open Font License 1.1 (http://scripts.sil.org/OFL)")
        dpg.bind_item_font("license", small_font)

dpg.create_viewport(title=f"Font Example", width=640, height=480)
dpg.set_primary_window("Main Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
