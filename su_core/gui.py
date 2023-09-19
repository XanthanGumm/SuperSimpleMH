import ctypes
import dearpygui.dearpygui as dpg
from su_core.data import Area
from ctypes import c_int


def on_dir_selection(_, app_data, user_data):
    cfg, shared_memory = user_data
    if cfg.is_d2lod_path_is_valid(app_data["current_path"]):
        cfg.update_d2lod_path(app_data["current_path"])
        dpg.configure_item("main", show=True)
        # dpg.set_viewport_width(325)
        # dpg.set_viewport_width(465)
        shared_memory.on_path_validator.set()

    else:
        on_dir_cancellation()


def on_dir_cancellation(*args):
    dpg.configure_item("mbox", show=True)


def on_message_box_ok(*args):
    dpg.configure_item("mbox", show=False)
    dpg.configure_item("DiabloII_lod_dialog", show=True)


def on_directions_change(sender, app_data, user_data):
    directions, shared_memory = user_data
    area = Area(shared_memory.area.value)
    dst_area = Area(sender)
    shared_memory.directions[dst_area.name] = app_data
    directions[area.name][dst_area.name] = app_data
    shared_memory.on_directions_change.set()


def on_quality_change(_, app_data, user_data):
    cfg, shared_memory = user_data
    shared_memory.quality.value = bytes(app_data, "utf8")
    cfg.general["properties"]["quality"] = app_data
    shared_memory.on_quality_change.set()


def on_opacity_change(sender, app_data, user_data):
    cfg, shared_memory = user_data
    opacity_value = (10 - app_data) * 0.1

    if sender == "overlay_opacity":
        shared_memory.overlay_opacity.value = opacity_value
    elif sender == "directions_opacity":
        shared_memory.directions_opacity.value = opacity_value
    else:
        shared_memory.npcs_opacity.value = opacity_value

    cfg.general["properties"][sender] = app_data


def on_draw_npc_change(sender, app_data, user_data):
    cfg, shared_memory = user_data

    if sender == "draw_monsters":
        shared_memory.monsters.value = app_data
    elif sender == "draw_uniques":
        shared_memory.uniques.value = app_data
    else:
        shared_memory.merc.value = app_data

    cfg.general["properties"][sender] = app_data


def on_area_checkbox_change(sender, app_data, user_data):
    cfg, act, shared_memory = user_data
    cfg.areas[act][sender] = app_data
    shared_memory.acts_levels.update(cfg.areas)


def on_overlay_checkbox_change(_, app_data, user_data):
    cfg, shared_memory = user_data
    cfg.general["properties"]["draw_overlay"] = app_data
    shared_memory.overlay.value = app_data


def on_visibility_change(state):
    if state:
        main_height = dpg.get_item_height("main")
        dpg.set_viewport_height(main_height)
    else:
        dpg.set_viewport_height(20)


def create_gui(shared_memory, cfg):

    is_path_valid = cfg.is_d2lod_path_is_valid(cfg.map_api["diablo2"]["path"])

    if not is_path_valid:
        dpg.set_viewport_width(700)
        dpg.set_viewport_height(700)

    else:
        shared_memory.on_path_validator.set()

    dpg.add_file_dialog(
        label="Select your Diablo II lod 1.13c directory",
        user_data=(cfg, shared_memory),
        tag="DiabloII_lod_dialog",
        width=500,
        height=350,
        callback=on_dir_selection,
        show=not is_path_valid,
        modal=False,
        directory_selector=True,
        cancel_callback=on_dir_cancellation,
    )

    with dpg.window(
            label="Message Box",
            tag="mbox",
            modal=True,
            no_title_bar=True,
            show=False,
            width=360,
            height=100,
            pos=[(600 - 430) // 2, (350 - 100) // 2],
            popup=True
    ):
        dpg.add_text("Please select your Diablo II lod 1.13c directory.")
        dpg.add_separator()
        dpg.add_button(label="OK", tag="b_ok", width=100, pos=[(350 - 100) // 2, 65], callback=on_message_box_ok)

        with dpg.window(
            label="SuperSimpleMH Settings",
            tag="main",
            no_move=True,
            no_resize=True,
            width=320,
            height=460,
            show=is_path_valid,
            no_close=True,
        ):

            with dpg.tab_bar(tag="options"):
                with dpg.tab(label="Overlay", tag="overlay"):
                    dpg.add_text(default_value="Overlay Settings")
                    dpg.add_checkbox(
                        label="Show Overlay",
                        tag="draw_overlay",
                        default_value=cfg.general["properties"]["draw_overlay"],
                        callback=on_overlay_checkbox_change,
                        user_data=(cfg, shared_memory),
                    )

                    dpg.add_combo(
                        label="Quality",
                        tag="quality",
                        default_value=cfg.general["properties"]["quality"],
                        items=["Low", "Medium", "High"],
                        callback=on_quality_change,
                        user_data=(cfg, shared_memory),
                        width=150,
                    )

                    dpg.add_slider_int(
                        label="Overlay Opacity",
                        tag="overlay_opacity",
                        default_value=cfg.general["properties"]["overlay_opacity"],
                        min_value=0,
                        max_value=9,
                        callback=on_opacity_change,
                        user_data=(cfg, shared_memory),
                        width=150,
                       )

                    dpg.add_slider_int(
                        label="Directions Opacity",
                        tag="directions_opacity",
                        default_value=cfg.general["properties"]["directions_opacity"],
                        min_value=0,
                        max_value=9,
                        callback=on_opacity_change,
                        user_data=(cfg, shared_memory),
                        width=150
                       )

                    dpg.add_slider_int(
                        label="Npcs Opacity",
                        tag="npcs_opacity",
                        default_value=cfg.general["properties"]["npcs_opacity"],
                        min_value=0,
                        max_value=9,
                        callback=on_opacity_change,
                        user_data=(cfg, shared_memory),
                        width=150,
                       )

                    dpg.add_checkbox(
                        label="Show Normal Monsters",
                        tag="draw_monsters",
                        default_value=cfg.general["properties"]["draw_monsters"],
                        callback=on_draw_npc_change,
                        user_data=(cfg, shared_memory),
                    )

                    dpg.add_checkbox(
                        label="Show Uniques/Champions",
                        tag="draw_uniques",
                        default_value=cfg.general["properties"]["draw_uniques"],
                        callback=on_draw_npc_change,
                        user_data=(cfg, shared_memory),
                    )

                    dpg.add_checkbox(
                        label="Show Mercenary",
                        tag="draw_merc",
                        default_value=cfg.general["properties"]["draw_uniques"],
                        callback=on_draw_npc_change,
                        user_data=(cfg, shared_memory),
                    )

                    dpg.add_text(default_value="Directions Settings")

                    with dpg.child_window(tag="directions_win", width=200, height=175):
                        with dpg.group(tag="directions"):
                            pass

                    dpg.add_button(
                        label="Save Settings",
                        tag="save",
                        width=100,
                        callback=lambda: cfg.save(),
                    )

                with dpg.tab(label="Areas"):
                    with dpg.tab_bar():
                        with dpg.tab(label="Act1", tag="Act1"):
                            for name, to_load in cfg.areas["Act1"].items():
                                dpg.add_checkbox(
                                    label=name,
                                    tag=name,
                                    default_value=to_load,
                                    user_data=(cfg, "Act1", shared_memory),
                                    callback=on_area_checkbox_change,
                                )

                        with dpg.tab(label="Act2", tag="Act2"):
                            for name, to_load in cfg.areas["Act2"].items():
                                dpg.add_checkbox(
                                    label=name,
                                    tag=name,
                                    default_value=to_load,
                                    user_data=(cfg, "Act2", shared_memory),
                                    callback=on_area_checkbox_change,
                                )

                        with dpg.tab(label="Act3", tag="Act3"):
                            for name, to_load in cfg.areas["Act3"].items():
                                dpg.add_checkbox(
                                    label=name,
                                    tag=name,
                                    default_value=to_load,
                                    user_data=(cfg, "Act3", shared_memory),
                                    callback=on_area_checkbox_change,
                                )

                        with dpg.tab(label="Act4", tag="Act4"):
                            for name, to_load in cfg.areas["Act4"].items():
                                dpg.add_checkbox(
                                    label=name,
                                    tag=name,
                                    default_value=to_load,
                                    user_data=(cfg, "Act4", shared_memory),
                                    callback=on_area_checkbox_change,
                                )

                        with dpg.tab(label="Act5", tag="Act5"):
                            for name, to_load in cfg.areas["Act5"].items():
                                dpg.add_checkbox(
                                    label=name,
                                    tag=name,
                                    default_value=to_load,
                                    user_data=(cfg, "Act5", shared_memory),
                                    callback=on_area_checkbox_change,
                                )


def create_directions_checkboxes(shared_memory, directions):
    dpg.delete_item("directions")
    with dpg.group(tag="directions", parent="directions_win"):
        for area, to_draw in directions[Area(shared_memory.area.value).name].items():
            dpg.add_checkbox(
                label=area,
                tag=Area.FromName(area).value,
                default_value=to_draw,
                user_data=(directions, shared_memory),
                callback=on_directions_change,
            )


class MARGINS(ctypes.Structure):
    _fields_ = [("cxLeftWidth", c_int), ("cxRightWidth", c_int), ("cyTopHeight", c_int), ("cyBottomHeight", c_int)]
