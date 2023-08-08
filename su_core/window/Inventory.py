import os
import io
import tomllib
import math
import pyMeow as pm
from PIL import Image
from logger import manager, traceback
from su_core.pyTypes.unitTypes import obtain_roster_members
from su_core.window.drawings import pm_colors
from su_core.utils.helpers import get_root
from su_core.utils.exceptions import FailedReadInventory

_logger = manager.get_logger(__file__)


class Inventory:

    def __init__(self, win_width, win_height, win_start_x, win_start_y, font_size):
        self._font_size = font_size
        self._win_start_x = win_start_x
        self._win_start_y = win_start_y

        root = get_root(__file__)
        sprites_path = os.path.join(root, "resources", "sprites", "inventory")
        # load inventory texture and its coordinates
        with open(os.path.join(sprites_path, "inventory_big.toml"), "rb") as inv_file:
            self._coords = tomllib.load(inv_file)

        img = Image.open(os.path.join(sprites_path, "inventory_big.png"))
        img = img.resize((int(0.3 * win_width), int(0.7 * win_height)))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        self._texture = pm.load_texture_bytes(".png", img_bytes)
        self._height_pad = int(0.095 * win_height)
        self._scale_w = img.size[0] / self._coords["size"]["width"]
        self._scale_h = img.size[1] / self._coords["size"]["height"]
        self._tooltips = dict()
        self._item_textures = {"amulet": dict(), "arm": dict(), "armor": dict(), "helm": dict(), "belt": dict(),
                               "boots": dict(), "gloves": dict(), "ring": dict(), "charms": dict()}
        self._switch_textures = []
        self._is_on_switch = False
        self._hover_player = None

        # load switch textures
        for i in range(1, 3):
            img_switch = Image.open(os.path.join(sprites_path, f"tab{i}.png"))
            img_switch = img_switch.resize(
                (int(self._scale_w * img_switch.size[0]), int(self._scale_h * img_switch.size[1]))
            )
            img_byte_arr = io.BytesIO()
            img_switch.save(img_byte_arr, format="PNG")
            img_bytes = img_byte_arr.getvalue()
            self._switch_textures.append(pm.load_texture_bytes(".png", img_bytes))

        # load items textures
        for cur_root, _, files in os.walk(os.path.join(root, "resources", "sprites", "items")):
            cur_dir = os.path.split(cur_root)[-1]
            for file in files:
                item_name = os.path.splitext(file)[0]
                item_img = Image.open(os.path.join(cur_root, file))
                item_img = item_img.resize(
                    (math.ceil(item_img.size[0] * self._scale_w), math.ceil(item_img.size[1] * self._scale_h))
                )
                img_byte_arr = io.BytesIO()
                item_img.save(img_byte_arr, format="PNG")
                item_img = img_byte_arr.getvalue()
                self._item_textures[cur_dir][item_name] = pm.load_texture_bytes(".png", item_img)

        pm.load_font(os.path.join(root, "fonts", "exocetblizzardot-medium.otf"), 2)

    def create_tooltips(self):
        player_level = 0
        self._tooltips.clear()
        self._is_on_switch = False
        if self._hover_player is not None:
            try:
                self._hover_player.read_player_inventory()
                rosters = obtain_roster_members()
                for r in rosters:
                    if r.unit_id == self._hover_player.unit_id:
                        player_level = r.player_level

            except Exception:
                if self._hover_player.inventory is None:
                    _logger.debug(
                        f"Exception occurred during drawing reading {self._hover_player.name} inventory."
                        "Canceling show player inventory command..."
                    )
                    _logger.debug(traceback.format_exc())
                    raise FailedReadInventory()
                else:
                    _logger.warning(
                        f"Exception occurred during drawing reading {self._hover_player.name} inventory."
                        f"Probably due to the player is too far."
                    )

            if self._hover_player.inventory.helm is not None:
                self._tooltips["helm"] = self._hover_player.inventory.helm.create_tooltip(player_level)

            if self._hover_player.inventory.amulet is not None:
                self._tooltips["amulet"] = self._hover_player.inventory.amulet.create_tooltip(player_level)

            if self._hover_player.inventory.armor is not None:
                self._tooltips["armor"] = self._hover_player.inventory.armor.create_tooltip(player_level)

            if self._hover_player.inventory.arm_left is not None:
                self._tooltips["arm_left"] = self._hover_player.inventory.arm_left.create_tooltip(player_level)

            if self._hover_player.inventory.arm_right is not None:
                self._tooltips["arm_right"] = self._hover_player.inventory.arm_right.create_tooltip(player_level)

            if self._hover_player.inventory.ring_left is not None:
                self._tooltips["ring_left"] = self._hover_player.inventory.ring_left.create_tooltip(player_level)

            if self._hover_player.inventory.ring_right is not None:
                self._tooltips["ring_right"] = self._hover_player.inventory.ring_right.create_tooltip(player_level)

            if self._hover_player.inventory.belt is not None:
                self._tooltips["belt"] = self._hover_player.inventory.belt.create_tooltip(player_level)

            if self._hover_player.inventory.boots is not None:
                self._tooltips["boots"] = self._hover_player.inventory.boots.create_tooltip(player_level)

            if self._hover_player.inventory.gloves is not None:
                self._tooltips["gloves"] = self._hover_player.inventory.gloves.create_tooltip(player_level)

            if self._hover_player.inventory.arm_switch_left is not None:
                self._tooltips["arm_switch_left"] = self._hover_player.inventory.arm_switch_left.create_tooltip(
                    player_level
                )

            if self._hover_player.inventory.arm_switch_right is not None:
                self._tooltips["arm_switch_right"] = self._hover_player.inventory.arm_switch_right.create_tooltip(
                    player_level
                )

            x, y, x2, y2 = self._coords["topleft_cell"].values()
            w, h = x2 - x, y2 - y
            item_size = 1

            for i in range(10):
                for j in range(4):
                    if item_size > 1:
                        item_size -= 1
                        continue

                    item_key = f"charms_{(j, i)}"
                    grid_item = self._hover_player.inventory[item_key]
                    if grid_item is not None:
                        self._tooltips[item_key] = grid_item.create_tooltip()
                        item_type = grid_item.item_type.name
                        item_size = 2 if item_type == "LargeCharm" else 3 if item_type != "SmallCharm" else 1
                        xmin = x + i * w
                        xmax = xmin + w
                        ymin = y + j * h
                        ymax = ymin + h * item_size
                        self._coords[item_key] = {"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax}

    def draw_inventory(self):
        pm.draw_texture(self._texture, 0, self._height_pad, pm_colors["white"], 0, 1)

        switch_texture = self._switch_textures[0] if not self._is_on_switch else self._switch_textures[1]
        pm.draw_texture(switch_texture, self._scale_w * self._coords["switch1"]["xmin"], self._scale_h * self._coords["switch1"]["ymin"] + self._height_pad, pm_colors["white"], 0, 1)
        pm.draw_texture(switch_texture, self._scale_w * self._coords["switch2"]["xmin"], self._scale_h * self._coords["switch2"]["ymin"] + self._height_pad, pm_colors["white"], 0, 1)

        if "helm" in self._tooltips:
            self._draw_inv_item("helm")
        if "amulet" in self._tooltips:
            self._draw_inv_item("amulet")
        if "armor" in self._tooltips:
            self._draw_inv_item("armor")
        if "arm_left" in self._tooltips and not self._is_on_switch:
            self._draw_inv_item("arm_left")
        if "arm_right" in self._tooltips and not self._is_on_switch:
            self._draw_inv_item("arm_right")
        if "ring_left" in self._tooltips:
            self._draw_inv_item("ring_left")
        if "ring_right" in self._tooltips:
            self._draw_inv_item("ring_right")
        if "belt" in self._tooltips:
            self._draw_inv_item("belt")
        if "boots" in self._tooltips:
            self._draw_inv_item("boots")
        if "gloves" in self._tooltips:
            self._draw_inv_item("gloves")
        if "arm_switch_left" in self._tooltips and self._is_on_switch:
            self._draw_inv_item("arm_switch_left")
        if "arm_switch_right" in self._tooltips and self._is_on_switch:
            self._draw_inv_item("arm_switch_right")

        for i in range(10):
            for j in range(4):
                if f"charms_{(j, i)}" in self._tooltips:
                    self._draw_inv_item(f"charms_{(j, i)}")

    def draw_item_tooltip(self):
        if self._is_loc_hovered("helm") and self._hover_player.inventory.helm is not None:
            x, y, w, h = self._inv_loc_position("helm")
            self._draw_item_tooltip("helm", x + w // 2, y + h + self._height_pad)
        elif self._is_loc_hovered("amulet") and self._hover_player.inventory.amulet is not None:
            x, y, w, h = self._inv_loc_position("amulet")
            self._draw_item_tooltip("amulet", x + w // 2, y + h + self._height_pad)
        elif self._is_loc_hovered("armor") and self._hover_player.inventory.armor is not None:
            x, y, w, h = self._inv_loc_position("armor")
            self._draw_item_tooltip("armor", x + w // 2, y + h + self._height_pad)
        elif self._is_loc_hovered("arm_left") and self._hover_player.inventory.arm_left is not None:
            x, y, w, h = self._inv_loc_position("arm_left")
            if self._is_on_switch and self._hover_player.inventory.arm_switch_left is not None:
                self._draw_item_tooltip("arm_switch_left", x + w // 2, y + h + self._height_pad)
            if not self._is_on_switch and self._hover_player.inventory.arm_left is not None:
                self._draw_item_tooltip("arm_left", x + w // 2, y + h + self._height_pad)
        elif self._is_loc_hovered("arm_right"):
            x, y, w, h = self._inv_loc_position("arm_right")
            if self._is_on_switch and self._hover_player.inventory.arm_switch_right is not None:
                self._draw_item_tooltip("arm_switch_right", x + w // 2, y + h + self._height_pad)
            if not self._is_on_switch and self._hover_player.inventory.arm_right:
                self._draw_item_tooltip("arm_right", x + w // 2, y + h + self._height_pad)
        elif self._is_loc_hovered("ring_left") and self._hover_player.inventory.ring_left is not None:
            x, y, w, h = self._inv_loc_position("ring_left")
            self._draw_item_tooltip("ring_left", x + w // 2, y + self._height_pad, direction="up")
        elif self._is_loc_hovered("ring_right") and self._hover_player.inventory.ring_right is not None:
            x, y, w, h = self._inv_loc_position("ring_right")
            self._draw_item_tooltip("ring_right", x + w // 2, y + self._height_pad, direction="up")
        elif self._is_loc_hovered("belt") and self._hover_player.inventory.belt is not None:
            x, y, w, h = self._inv_loc_position("belt")
            self._draw_item_tooltip("belt", x + w // 2, y + self._height_pad, direction="up")
        elif self._is_loc_hovered("boots") and self._hover_player.inventory.boots is not None:
            x, y, w, h = self._inv_loc_position("boots")
            self._draw_item_tooltip("boots", x + w // 2, y + self._height_pad, direction="up")
        elif self._is_loc_hovered("gloves") and self._hover_player.inventory.gloves is not None:
            x, y, w, h = self._inv_loc_position("gloves")
            self._draw_item_tooltip("gloves", x + w // 2, y + self._height_pad, direction="up")

        for i in range(10):
            for j in range(4):
                item_key = f"charms_{(j, i)}"
                if item_key in self._tooltips:
                    x, y, w, h = self._inv_loc_position(item_key)
                    if self._is_loc_hovered(item_key):
                        self._draw_item_tooltip(item_key, x + w // 2, y + self._height_pad, direction="up")

    def _draw_inv_item(self, loc: str):
        try:
            dir_name = loc.split("_")[0]
            unique_texture_name = self._hover_player.inventory[loc].unique_texture_name

            if unique_texture_name in self._item_textures[dir_name]:
                file_name = unique_texture_name
            else:
                file_name = self._hover_player.inventory[loc].texture_name

            x, y, w, h = self._inv_loc_position(loc)
            t_w = self._item_textures[dir_name][file_name]["width"]
            t_h = self._item_textures[dir_name][file_name]["height"]
            x_start = x + (w - t_w) // 2
            y_start = y + (h - t_h) // 2 + self._height_pad
            if self._is_loc_hovered(loc):
                pm.draw_rectangle(x, y + self._height_pad, w, h, pm_colors["invbackground"])
            pm.draw_texture(self._item_textures[dir_name][file_name], x_start, y_start, pm_colors["white"], 0, 1)

        except KeyError as e:
            _logger.debug(f"Exception occurred during drawing inventory texture")
            _logger.debug(traceback.format_exc())

    def _draw_item_tooltip(self, loc, start_x, start_y, direction="down"):
        # tooltip[0] = item_name, tooltip[1] = item_type, tooltip[2] = item_runes,
        # tooltip[3] = item_prolog, tooltip[4] = item_tooltip
        tooltip = self._tooltips[loc]
        item_quality = self._hover_player.inventory[loc].item_quality
        tooltip_lens = [pm.measure_font(2, s, self._font_size, 0) for s in tooltip[:-2]] + \
                       [pm.measure_font(2, s, self._font_size, 0) for s in tooltip[-2]] + \
                       [pm.measure_font(2, s, self._font_size, 0) for s in tooltip[-1]]

        text_box_width = max(e["x"] for e in tooltip_lens)
        text_box_height = sum(self._font_size for m in tooltip_lens if m["x"] > 0)

        # toolip[0] = item_type --> tooltip[0]["x"] always greater than 0
        tooltip_pads = [((text_box_width - tooltip_lens[0]["x"]) // 2, 0)]
        for i in range(1, len(tooltip_lens)):
            if tooltip_lens[i]["x"] > 0:
                line_w_pad = ((text_box_width - tooltip_lens[i]["x"]) // 2)
                line_h_pad = tooltip_pads[-1][1] + self._font_size
                tooltip_pads.append((line_w_pad, line_h_pad))

        start_x = start_x - text_box_width // 2
        if start_x < 0:
            start_x = 0

        if direction == "down":
            background_x = start_x
            background_y = start_y
            background_w = text_box_width
            background_h = text_box_height

        else:
            start_y = start_y - text_box_height
            background_x = start_x
            background_y = start_y
            background_w = text_box_width
            background_h = text_box_height

        type_pad_x, type_pad_y = None, None
        runes_pad_x, runes_pad_y = None, None

        if item_quality == "UNIQUE" or item_quality == "RUNEWORD":
            color = "d2rbrown"
        elif item_quality == "SET":
            color = "tooltipgreen"
        elif item_quality == "RARE":
            color = "tooltipyellow"
        elif item_quality == "CRAFTED":
            color = "tooltiporange"
        elif item_quality == "MAGIC":
            color = "tooltipblue"
        else:
            color = "tooltipgray"

        name_pad_x, name_pad_y = tooltip_pads.pop(0)

        if tooltip[1] != "":  # tooltip[1] = type
            type_pad_x, type_pad_y = tooltip_pads.pop(0)

        if tooltip[2] != "":  # tooltip[2] = runes
            runes_pad_x, runes_pad_y = tooltip_pads.pop(0)

        prolog_pad = [tooltip_pads.pop(0) for _ in range(len(tooltip[3]))]
        text_pad = [tooltip_pads.pop(0) for _ in range(len(tooltip[4]))]

        pm.draw_rectangle(background_x, background_y, background_w, background_h, pm_colors["tooltipbackground"])

        pm.draw_font(
            2, tooltip[0], start_x + name_pad_x, start_y + name_pad_y, self._font_size, 0, pm_colors[color]
        )

        if type_pad_x is not None and type_pad_y is not None:
            pm.draw_font(
                2, tooltip[1], start_x + type_pad_x, start_y + type_pad_y, self._font_size, 0,
                pm_colors["tooltipgray"] if item_quality == "RUNEWORD" else pm_colors[color]
            )

        if runes_pad_x is not None and runes_pad_y is not None:
            pm.draw_font(
                2, tooltip[2], start_x + runes_pad_x, start_y + runes_pad_y, self._font_size, 0, pm_colors[color]
            )

        for pad, text in zip(prolog_pad, tooltip[3]):
            pm.draw_font(2, text, start_x + pad[0], start_y + pad[1], self._font_size, 0, pm_colors["white"])

        for pad, text in zip(text_pad, tooltip[4]):
            pm.draw_font(2, text, start_x + pad[0], start_y + pad[1], self._font_size, 0, pm_colors["tooltipblue"])

    def _inv_loc_position(self, loc: str) -> tuple:
        xpos = int(self._scale_w * self._coords[loc]["xmin"])
        ypos = int(self._scale_h * self._coords[loc]["ymin"])
        w = int(self._scale_w * self._coords[loc]["xmax"]) - xpos
        h = int(self._scale_h * self._coords[loc]["ymax"]) - ypos
        return xpos, ypos, w, h

    def _is_loc_hovered(self, loc: str) -> bool:
        absolute_mouse = pm.mouse_position()
        relative_mouse = {"x": absolute_mouse["x"] - self._win_start_x, "y": absolute_mouse["y"] - self._win_start_y}
        x, y, w, h = self._inv_loc_position(loc)
        y += self._height_pad

        if x < relative_mouse["x"] < x + w and y < relative_mouse["y"] < y + h:
            return True

        return False

    @property
    def hover_player(self):
        return self._hover_player

    @hover_player.setter
    def hover_player(self, player):
        self._hover_player = player

    @property
    def is_on_switch(self):
        return self._is_on_switch

    @is_on_switch.setter
    def is_on_switch(self, value):
        self._is_on_switch = value
