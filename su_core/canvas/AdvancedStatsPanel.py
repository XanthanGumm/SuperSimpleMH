import os
import io
import tomllib
import pyMeow as pm
from PIL import Image
from su_core.utils.helpers import get_root, get_last_val
from su_core.canvas.drawings import Colors


class AdvancedStatsPanel:
    def __init__(self, win_width, win_height, win_start_x, win_start_y, font_size):
        self._font_size = font_size
        self._win_start_x = win_start_x
        self._win_start_y = win_start_y

        root = get_root(__file__)
        sprites_path = os.path.join(root, "resources", "sprites", "advanced_stats")

        with open(os.path.join(sprites_path, "advanced_stats_coords.toml"), "rb") as inv_file:
            self._coords = tomllib.load(inv_file)

        img = Image.open(os.path.join(sprites_path, "advanced_sheet.png"))
        img = img.resize((int(0.25 * win_width), int(0.7 * win_height)))

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        self._advanced_stats_texture = pm.load_texture_bytes(".png", img_bytes)
        self._scale_w = img.size[0] / self._coords["size"]["width"]
        self._scale_h = img.size[1] / self._coords["size"]["height"]

        img = Image.open(os.path.join(sprites_path, "value_box.png"))
        img = img.resize(
            (
                int(self._coords["value_box"]["width"] * self._scale_w),
                int(self._coords["value_box"]["height"] * self._scale_h),
            )
        )

        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_bytes = img_byte_arr.getvalue()

        self._value_box_texture = pm.load_texture_bytes(".png", img_bytes)
        self._height_pad = int(0.095 * win_height)

        self._hover_player = None
        self._stats_tooltips = []

    # TODO: restructure this func by using a func that returns stat tooltip
    def create_tooltip(self):
        self._stats_tooltips.clear()
        if self._hover_player is not None:
            diff = self._hover_player.act.act_misc.difficulty.value
            penalty = 100 if diff == 2 else 40 if diff == 1 else 0
            penalty -= 30
            stats = self._hover_player.read_stats(self._hover_player._stats_list_struct.Stats)  # change this later

            # fireresist, coldresist, lightresist, poisonresist resist
            self._stats_tooltips.append(
                f"Fire Resistance {get_last_val(stats['fireresist']) - penalty if 'fireresist' in stats else -penalty}%"
            )
            self._stats_tooltips.append(
                f"Cold Resistance {get_last_val(stats['coldresist']) - penalty if 'coldresist' in stats else -penalty}%"
            )
            self._stats_tooltips.append(
                f"Lightning Resistance {get_last_val(stats['lightresist']) - penalty if 'lightresist' in stats else -penalty}%"
            )
            self._stats_tooltips.append(
                f"Poison Resistance {get_last_val(stats['poisonresist']) - penalty if 'poisonresist' in stats else -penalty}%"
            )

            # damageresist - physical damage reduced
            if "damageresist" in stats:
                self._stats_tooltips.append(
                    f"Physical Damage Received Reduced by {get_last_val(stats['damageresist'])}%"
                )

            # item_fastercastrate - fcr
            if "item_fastercastrate" in stats:
                self._stats_tooltips.append(f"+{get_last_val(stats['item_fastercastrate'])}% Faster Cast Rate")

            # item_fasterattackrate - ias
            if "item_fasterattackrate" in stats:
                self._stats_tooltips.append(f"+{get_last_val(stats['item_fasterattackrate'])}% Increase Attack Speed")

            # item_fastermovevelocity - frw
            if "item_fastermovevelocity" in stats:
                self._stats_tooltips.append(f"+{get_last_val(stats['item_fastermovevelocity'])}% Faster Run Walk")

            # item_fastergethitrate - fhr
            if "item_fastergethitrate" in stats:
                self._stats_tooltips.append(f"+{get_last_val(stats['item_fastergethitrate'])}% Faster Hit Recovery")

            # item_absorbfire_percent - absorb fire
            if "item_absorbfire_percent" in stats:
                self._stats_tooltips.append(f"Fire Absorb +{get_last_val(stats['item_absorbfire_percent'])}%")

            # item_absorblight_percent - absorb light
            if "item_absorblight_percent" in stats:
                self._stats_tooltips.append(f"Lightning Absorb +{get_last_val(stats['item_absorblight_percent'])}%")

            # item_absorbcold_percent - absorb cold
            if "item_absorbcold_percent" in stats:
                self._stats_tooltips.append(f"Cold Absorb +{get_last_val(stats['item_absorbcold_percent'])}%")

            # hpregen - replenish life
            if "hpregen" in stats:
                self._stats_tooltips.append(f"Replenish Life +{get_last_val(stats['hpregen'])}")

            # manarecoverybonus - Regenmana
            if "manarecoverybonus" in stats:
                self._stats_tooltips.append(f"Regenerate Mana {get_last_val(stats['manarecoverybonus'])}%")

            # lifedrainmindam - life stolen per hit
            if "lifedrainmindam" in stats:
                self._stats_tooltips.append(f"{get_last_val(stats['lifedrainmindam'])}% Life Stolen Per Hit")

            # manadrainmindam - mana stolen per hit
            if "manadrainmindam" in stats:
                self._stats_tooltips.append(f"{get_last_val(stats['manadrainmindam'])}% Mana Stolen Per Hit")

            # item_magicbonus - magic find
            if "item_magicbonus" in stats:
                self._stats_tooltips.append(f"{get_last_val(stats['item_magicbonus'])}% Chance of Getting Magic Items")

            # item_deadlystrike - deadly strike
            if "item_deadlystrike" in stats:
                self._stats_tooltips.append(f"Deadly Strike {get_last_val(stats['item_deadlystrike'])}%")

            # item_crushingblow - crushing blow
            if "item_crushingblow" in stats:
                self._stats_tooltips.append(f"Crushing Blow {get_last_val(stats['item_crushingblow'])}%")

            # item_openwounds - open wounds
            if "item_openwounds" in stats:
                self._stats_tooltips.append(f"Open Wounds {stats['item_crushingblow']}%")

            # magicresist - magic resist
            if "magicresist" in stats:
                self._stats_tooltips.append(f"Magic Resistance {get_last_val(stats['magicresist'])}%")

            # item_slow - slow target by
            if "item_slow" in stats:
                self._stats_tooltips.append(f"Slow Target By {get_last_val(stats['item_slow'])}%")

            # TODO: add -resist

    def draw_advanced_stats(self):
        self._value_box_x = self._coords["value_box"]["x"] * self._scale_w
        self._value_box_y = self._coords["value_box"]["y"] * self._scale_h + self._height_pad
        self._value_box_h = self._coords["value_box"]["height"] * self._scale_h
        self._value_box_w = self._coords["value_box"]["width"] * self._scale_w
        line_limit = self._value_box_w - (2 * self._scale_w * 20)

        if self._stats_tooltips:
            pm.draw_texture(
                self._advanced_stats_texture,
                0,
                self._height_pad,
                Colors.Get("White"),
                0,
                1,
            )

            for i in range(len(self._stats_tooltips)):
                pm.draw_texture(
                    self._value_box_texture,
                    self._value_box_x,
                    self._value_box_y,
                    Colors.Get("White"),
                    0,
                    1,
                )

                text_len = pm.measure_font(2, self._stats_tooltips[i], self._font_size, 0)
                if text_len["x"] >= line_limit - 1:

                    split_text = self._stats_tooltips[i].split(" ")
                    text_1 = split_text.pop(0)
                    text_2 = split_text.pop(-2) + " " + split_text.pop(-1)

                    while split_text:
                        s = split_text.pop(0)
                        t1_len = pm.measure_font(2, text_1, self._font_size, 0)
                        s_len = pm.measure_font(2, s, self._font_size, 0)
                        if t1_len["x"] + s_len["x"] < line_limit:
                            text_1 += " " + s
                        else:
                            text_2 = s + " " + text_2

                    text_1_len = pm.measure_font(2, text_1, self._font_size, 0)
                    text_2_len = pm.measure_font(2, text_2, self._font_size, 0)

                    text_1_x = self._value_box_x + (line_limit - text_1_len["x"]) // 2
                    text_2_x = self._value_box_x + (line_limit - text_2_len["x"]) // 2
                    text_1_y = self._value_box_y + (self._value_box_h - 2 * self._font_size) // 2
                    text_2_y = text_1_y + self._font_size + 2

                    pm.draw_font(
                        2,
                        text_1,
                        text_1_x,
                        text_1_y,
                        self._font_size,
                        0,
                        Colors.Get("White"),
                    )

                    pm.draw_font(
                        2,
                        text_2,
                        text_2_x,
                        text_2_y,
                        self._font_size,
                        0,
                        Colors.Get("White"),
                    )

                else:
                    text_y = self._value_box_y + (self._value_box_h - self._font_size) // 2
                    text_x = self._value_box_x + (line_limit - text_len["x"]) // 2

                    pm.draw_font(
                        2,
                        self._stats_tooltips[i],
                        text_x,
                        text_y,
                        self._font_size,
                        0,
                        Colors.Get("White"),
                    )

                self._value_box_y += self._value_box_h + self._scale_h * 18

                if (
                    self._value_box_y + 2 * self._value_box_h
                    > self._advanced_stats_texture["height"] + self._height_pad
                ):
                    break

    def clear(self):
        pm.unload_texture(self._advanced_stats_texture)
        pm.unload_texture(self._value_box_texture)

    @property
    def hover_player(self):
        return self._hover_player

    @hover_player.setter
    def hover_player(self, player):
        self._hover_player = player
