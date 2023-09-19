from su_core.pyTypes import UnitAny
from su_core.pyStructures import ItemData, StatsList
from su_core.data import GameItem, ItemQuality, ItemFlag, items_codes, item_texture_name
from su_core.data import Skill, SkillTab
from su_core.utils.helpers import get_last_val, get_last_key
from su_core.utils.exceptions import ItemTypeNotFound
from su_core.logging.Logger import Logger, traceback
from su_core.data import (
    strings,
    statscost,
    runewords,
    uniques,
    sets,
    defensive,
    offensive,
    charstats,
    misc,
    magicprefix,
    magicsuffix,
    rareprefix,
    raresuffix,
)


class Item(UnitAny):
    _stats_ignore_list = [
        "durability",
        "maxdurability",
        "armorclass",
        "toblock",
        "item_throwable",
        "item_kickdamage",
        "item_staminadrainpct",
        "item_regenstamina_perlevel",
        "item_kick_damage_perlevel",
        "coldlength",
        "attackrate",
        "item_mindamage_percent",
        "item_maxdurability_percent",
        "item_levelreq",
        "quantity",
        "velocitypercent",
        "poisonlength",
        "poison_count",
        "item_throw_mindamage",
        "item_throw_maxdamage",
    ]

    def __init__(self, address):
        super(Item, self).__init__(address, path_type="item")
        self._logger = Logger.get_logger(__name__)
        self._item_type = None
        self._item_data = None
        self._item_quality = None
        self._is_runeword = None
        self._is_ethereal = None
        self._texture_name = None
        self._unique_texture_name = None
        self._stats = None
        self.update()

    def update(self):
        super(Item, self).update()
        self._item_data = self._mem.read_struct(self._struct.pUnitData, ItemData)
        self._item_type = GameItem(self._txt_file_no)

        self._is_runeword = self._item_data.ItemFlags & ItemFlag.IFLAG_RUNEWORD.value == ItemFlag.IFLAG_RUNEWORD.value

        self._is_ethereal = self._item_data.ItemFlags & ItemFlag.IFLAG_ETHEREAL.value == ItemFlag.IFLAG_ETHEREAL.value

        self._item_quality = ItemQuality(self._item_data.ItemQuality)
        self._texture_name = item_texture_name[self._item_type]

        if self._item_type in [
            GameItem.GrandCharm,
            GameItem.LargeCharm,
            GameItem.SmallCharm,
            GameItem.Ring,
            GameItem.Amulet,
        ]:  # means that item has skin
            self._texture_name += str(self._item_data.wSkinId)

        if self._item_quality == ItemQuality.UNIQUE:
            item_name = uniques.loc[self._item_data.dwUniqueOrSetId, "index"]
            self._unique_texture_name = item_name.replace(" ", "_").replace("'", "").lower()

        if self._item_quality == ItemQuality.SET:
            item_name = sets.loc[self._item_data.dwUniqueOrSetId, "index"]
            self._unique_texture_name = item_name.replace(" ", "_").replace("'", "").lower()

    def read_added_stats(self):
        if self._stats_list_struct.dwFlags & 0x80000000 == 0:
            return dict(), dict()

        if not self._stats_list_struct.BaseStats.pStats:
            return dict(), dict()

        added_basestats = dict()
        added_stats = dict()
        last_stats_list = self._mem.read_struct(self._stats_list_struct.pMyStats, StatsList)

        while True:
            if last_stats_list.BaseStats.pStats:
                added_basestats.update(self.read_stats(last_stats_list.BaseStats))

            try:
                if last_stats_list.Stats.pStats:
                    added_stats.update(self.read_stats(last_stats_list.Stats))
            except Exception as e:
                pass

            if not last_stats_list.pPrev:
                break

            last_stats_list = self._mem.read_struct(last_stats_list.pPrev, StatsList)

        return added_basestats, added_stats

    # TODO: restructure this func by creating separate function which returns single stat tooltip
    def create_tooltip(self, player_level=0):
        item_code = items_codes[self._item_type.value]
        self._stats = self.read_stats(self._stats_list_struct.Stats)
        added_basestats, added_stats = self.read_added_stats()

        # merge ed stat from added basestats/stats
        if "item_armor_percent" in added_stats and "item_armor_percent" in added_basestats:
            layer = get_last_key(added_stats["item_armor_percent"])
            added_stats["item_armor_percent"][-1][layer] += added_basestats["item_armor_percent"][-1][layer]
        if "item_maxdamage_percent" in added_stats and "item_maxdamage_percent" in added_basestats:
            layer = get_last_key(added_stats["item_maxdamage_percent"])
            added_stats["item_maxdamage_percent"][-1][layer] += added_basestats["item_maxdamage_percent"][-1][layer]

        # add additional stats
        for k, v in added_stats.items():
            self._stats.setdefault(k, v)

        for k, v in added_basestats.items():
            self._stats.setdefault(k, v)

        # merge resists
        if (
            "fireresist" in self._stats
            and "lightresist" in self._stats
            and "coldresist" in self._stats
            and "poisonresist" in self._stats
        ):
            fire = get_last_val(self._stats["fireresist"])
            light = get_last_val(self._stats["lightresist"])
            cold = get_last_val(self._stats["coldresist"])
            psn = get_last_val(self._stats["poisonresist"])
            if fire == light == cold == psn:
                self._merge_stats_tooltip(
                    "allresist",
                    0,
                    psn,
                    ["fireresist", "lightresist", "coldresist", "poisonresist"],
                )

        # merge attributes
        if (
            "strength" in self._stats
            and "energy" in self._stats
            and "dexterity" in self._stats
            and "vitality" in self._stats
        ):
            stren = get_last_val(self._stats["strength"])
            ene = get_last_val(self._stats["energy"])
            dex = get_last_val(self._stats["dexterity"])
            vit = get_last_val(self._stats["vitality"])
            if stren == ene == dex == vit:
                self._merge_stats_tooltip("allatt", 0, vit, ["strength", "energy", "dexterity", "vitality"])

        # merge elemental damage
        if "firemindam" in self._stats and "firemaxdam" in self._stats:
            new_layer, new_stat = get_last_val(self._stats["firemindam"]), get_last_val(self._stats["firemaxdam"])
            self._merge_stats_tooltip("firedam", new_layer, new_stat, ["firemindam", "firemaxdam"])
        if "coldmindam" in self._stats and "coldmaxdam" in self._stats:
            new_layer, new_stat = get_last_val(self._stats["coldmindam"]), get_last_val(self._stats["coldmaxdam"])
            self._merge_stats_tooltip("colddam", new_layer, new_stat, ["coldmindam", "coldmaxdam"])
        if "lightmindam" in self._stats and "lightmaxdam" in self._stats:
            new_layer, new_stat = get_last_val(self._stats["lightmindam"]), get_last_val(self._stats["lightmaxdam"])
            self._merge_stats_tooltip("lightdam", new_layer, new_stat, ["lightmindam", "lightmaxdam"])
        if "magicmindam" in self._stats and "magicmaxdam" in self._stats:
            new_layer, new_stat = get_last_val(self._stats["magicmindam"]), get_last_val(self._stats["magicmaxdam"])
            self._merge_stats_tooltip("magicdam", new_layer, new_stat, ["magicmindam", "magicmaxdam"])
        if "poisonmindam" in self._stats and "poisonmaxdam" in self._stats:
            new_layer, new_stat = get_last_val(self._stats["poisonmindam"]), get_last_val(self._stats["poisonmaxdam"])
            self._merge_stats_tooltip("poisondam", new_layer, new_stat, ["poisonmindam", "poisonmaxdam"])

        stats_filtered = {k: v for k, v in self._stats.items() if k not in self._stats_ignore_list}
        stats_sorted = dict(
            sorted(
                stats_filtered.items(),
                key=lambda s: statscost.loc[s[0], "descpriority"],
                reverse=True,
            )
        )

        item_name = ""
        item_prolog = []
        item_runes = ""
        item_tooltip = []

        if item_code not in offensive.index.values:
            # get rid any damage except maxdamage if item is not a weapon
            stats_sorted.pop("secondary_maxdamage", None)
            stats_sorted.pop("secondary_mindamage", None)
            stats_sorted.pop("item_throw_maxdamage", None)
            stats_sorted.pop("item_throw_mindamage", None)

        if item_code in defensive.index.values:
            item_type = defensive.loc[item_code, "name"]
            defense = get_last_val(self._stats["armorclass"])
            item_prolog.append(f"Defense: {defense}")

        elif item_code in offensive.index.values:
            item_type = offensive.loc[item_code, "name"]
            if "mindamage" in stats_sorted and "maxdamage" in stats_sorted:
                mindmg = get_last_val(stats_sorted["mindamage"])
                maxdmg = get_last_val(stats_sorted["maxdamage"])
                item_prolog.append(f"One-Hand Damage: {mindmg} to {maxdmg}")
                del stats_sorted["mindamage"]
                del stats_sorted["maxdamage"]
            if "secondary_mindamage" in stats_sorted and "secondary_maxdamage" in stats_sorted:
                mindmg = get_last_val(stats_sorted["secondary_mindamage"])
                maxdmg = get_last_val(stats_sorted["secondary_maxdamage"])
                item_prolog.append(f"Two-Hand Damage: {mindmg} to {maxdmg}")
                del stats_sorted["secondary_mindamage"]
                del stats_sorted["secondary_maxdamage"]
            if "item_throw_mindamage" in stats_sorted and "item_throw_maxdamage" in stats_sorted:
                mindmg = get_last_val(stats_sorted["item_throw_mindamage"])
                maxdmg = get_last_val(stats_sorted["item_throw_maxdamage"])
                item_prolog.append(f"Throw Damage: {mindmg} to {maxdmg}")
                del stats_sorted["item_throw_mindamage"]
                del stats_sorted["item_throw_maxdamage"]

        elif item_code in misc.index.values:
            item_type = misc.loc[item_code, "name"]

        else:
            raise ItemTypeNotFound(f"Item: {self._item_type}, Code: {item_code}")

        if self._item_quality == ItemQuality.UNIQUE:
            item_name = uniques.loc[self._item_data.dwUniqueOrSetId, "index"]

        elif self._item_quality == ItemQuality.SET:
            item_name = sets.loc[self._item_data.dwUniqueOrSetId, "index"]

        elif self._is_runeword:
            item_name = runewords.loc[self._item_data.MagicPrefix[0], "*Rune Name"]
            item_runes = runewords.loc[self._item_data.MagicPrefix[0], "*RunesUsed"]

        elif self._item_quality == ItemQuality.RARE or self._item_quality == ItemQuality.CRAFTED:
            name_prefix, name_suffix = None, None
            if self._item_data.RarePrefix:
                name_prefix = rareprefix.loc[self._item_data.RarePrefix, "name"]
            if self._item_data.RareSuffix:
                name_suffix = raresuffix.loc[self._item_data.RareSuffix, "name"]

            if name_prefix is not None:
                item_name = name_prefix

            if name_suffix is not None:
                item_name += " " + name_suffix

            item_name += "\n"

        elif self._item_quality == ItemQuality.MAGIC:
            name_prefix, name_suffix = None, None
            if self._item_data.MagicPrefix[0]:
                name_prefix = magicprefix.loc[self._item_data.MagicPrefix[0], "Name"]
            if self._item_data.MagicSuffix[0]:
                name_suffix = magicsuffix.loc[self._item_data.MagicSuffix[0], "Name"]

            if name_prefix is not None:
                item_name = name_prefix + " "

            item_name += item_type

            if name_suffix is not None:
                item_name += " " + name_suffix

            item_name += "\n"
            item_type = ""

        elif self._item_quality in [
            ItemQuality.NORMAL,
            ItemQuality.SUPERIOR,
            ItemQuality.INFERIOR,
            ItemQuality.TEMPERED,
        ]:
            item_name = item_type
            item_type = ""

        else:
            pass  # should not happen

        for name, stat in stats_sorted.items():
            descfunc = statscost.loc[name, "descfunc"]
            descval = statscost.loc[name, "descval"]
            shift_val = statscost.loc[name, "ValShift"]
            div_val = statscost.loc[name, "ValDivision"]

            if descfunc not in [24, 28]:
                layer, value = get_last_key(stat), get_last_val(stat)

            try:
                if shift_val != -1:
                    value = value >> shift_val

                elif div_val != -1:
                    value = value / div_val

            except Exception:
                self._logger.debug(f"Exception occurred during drawing create item tooltip at stat: {name}")
                self._logger.debug(traceback.format_exc())
                break

            try:
                if value < 0:
                    stat_key = statscost.loc[name, "descstrneg"]
                else:
                    stat_key = statscost.loc[name, "descstrpos"]

                stat_tooltip = strings.loc[stat_key, "value"]

            except KeyError:
                if descfunc not in [13, 14, 15, 16, 24, 27, 28]:
                    self._logger.debug(
                        f"Exception occurred during drawing create item tooltip at stat: {name} with key: {stat_key}"
                    )
                    self._logger.debug(traceback.format_exc())
                    break

            if descfunc == 0:  # do not display value
                stat_tooltip += "\n"

            elif descfunc == 1:  # plus or minus
                sign = "+" if value > 0 else ""
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} {sign}{value}\n"
                else:
                    stat_tooltip = f"{sign}{value} {stat_tooltip}\n"

            elif descfunc == 2:  # percent
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} {value}%\n"
                else:
                    stat_tooltip = f"{value}% {stat_tooltip}\n"

            elif descfunc == 3:  # string
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} {value}\n"
                else:
                    stat_tooltip = f"{value} {stat_tooltip}\n"

            elif descfunc == 4:  # plus percent
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} +{value}%\n"
                else:
                    stat_tooltip = f"+{value}% {stat_tooltip}\n"

            elif descfunc == 6:  # plus per level
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} +{int(value * player_level)} (Based On Character Level)\n"
                else:
                    stat_tooltip = f"+{int(value * player_level)} {stat_tooltip} (Based On Character Level)\n"

            elif descfunc == 7:  # percent per level
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} {int(value * player_level)}% (Based On Character Level)\n"
                else:
                    stat_tooltip = f"{int(value * player_level)}% {stat_tooltip} (Based On Character Level)\n"

            elif descfunc == 8:  # plus percent per level
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} +{int(value * player_level)}% (Based On Character Level)\n"
                else:
                    stat_tooltip = f"+{int(value * player_level)}% {stat_tooltip} (Based On Character Level)\n"

            elif descfunc == 13:  # class skill
                stat_tooltip = ""
                for stat_layer in stat:
                    (char_id, val), *_ = stat_layer.items()
                    char = charstats.loc[charstats["ID"] == char_id].index[0]
                    char_class_key = charstats.loc[char, "StrAllSkills"]
                    char_class_val = strings.loc[char_class_key, "value"]
                    stat_tooltip = stat_tooltip + f"+{val} {char_class_val}\n"

            elif descfunc == 14:  # skill tabs
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk_tab, val), *_ = stat_layer.items()
                    sk_tab_key = SkillTab(sk_tab).name
                    sk_tab_val = strings.loc[sk_tab_key, "value"]
                    char = charstats.loc[
                        (charstats["StrSkillTab1"] == sk_tab_key)
                        | (charstats["StrSkillTab2"] == sk_tab_key)
                        | (charstats["StrSkillTab3"] == sk_tab_key)
                    ].index[0]

                    stat_tooltip = stat_tooltip + f"{sk_tab_val.replace('%d', str(val))} ({char} Only)\n"

            elif descfunc == 15:  # skill on struck/strike/level/death
                stat_str = stat_tooltip
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk_layer, sk_chance), *_ = stat_layer.items()
                    skill = Skill(sk_layer >> 6)
                    skill_lvl = sk_layer % (1 << 6)
                    stat_tooltip = (
                        stat_tooltip
                        + stat_str.replace("%d%", str(sk_chance))
                        .replace("%d", str(skill_lvl))
                        .replace("%s", skill.name)
                        + "\n"
                    )

            elif descfunc == 16:
                stat_str = stat_tooltip
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk, sk_lvl), *_ = stat_layer.items()
                    sk = Skill(sk).name
                    stat_tooltip = stat_tooltip + stat_str.replace("%d", str(sk_lvl)).replace("%s", sk) + "\n"

            elif descfunc == 20:  # minus percent
                if descval == 2:
                    stat_tooltip = f"{stat_tooltip} -{value}%\n"
                else:
                    stat_tooltip = f"-{value}% {stat_tooltip}"

            elif descfunc == 24:  # charges
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk_layer, sk_val), *_ = stat_layer.items()
                    skill = Skill(sk_layer >> 6)
                    skill_lvl = sk_layer % (1 << 6)
                    max_charges = sk_val >> 8
                    charges = sk_val % (1 << 8)
                    stat_tooltip = stat_tooltip + f"Level {skill_lvl} {skill.name} ({charges}/{max_charges} Charges)\n"

            elif descfunc == 27:  # single skill
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk, sk_val), *_ = stat_layer.items()
                    sk = Skill(sk)
                    char = charstats.loc[
                        (charstats["skRangeMin"] <= sk.value) & (sk.value <= charstats["skRangeMax"])
                    ].index[0]
                    stat_tooltip = stat_tooltip + f"+{sk_val} {sk.name} ({char} Only)\n"

            elif descfunc == 28:  # non class skill
                stat_tooltip = ""
                for stat_layer in stat:
                    (sk, sk_lvl), *_ = stat_layer.items()
                    skill = Skill(sk)
                    skill_level = sk_lvl
                    stat_tooltip = stat_tooltip + f"+{skill_level} {skill.name}\n"

            elif descfunc == 30:  # sockets/ethereal
                stat_tooltip = stat_tooltip.replace("%d", str(value))
                if self._is_ethereal:
                    stat_tooltip = "Ethereal (Cannot Be Repaired), " + stat_tooltip

            elif descfunc == 31:  # elemental range damage
                if name == "poisondam":
                    # blame mapview for this hack
                    psn_len = get_last_val(self._stats["poisonlength"]) // 25
                    stat_tooltip = f"+{int(value / (10.2 / psn_len))} poison damage over {psn_len} seconds"
                else:
                    stat_tooltip = stat_tooltip.replace("%d-%d", f"{layer}-{value}") + "\n"

            item_tooltip.extend(stat_tooltip.splitlines())

        return item_name, item_type, item_runes, item_prolog, item_tooltip

    def _merge_stats_tooltip(self, stat_name, new_later, new_val, to_bin):
        self._stats[stat_name] = [{new_later: new_val}]
        for name in to_bin:
            del self._stats[name]

    @property
    def item_quality(self):
        if self._is_runeword:
            return "RUNEWORD"
        return self._item_quality.name

    @property
    def item_type(self):
        return self._item_type

    @property
    def texture_name(self):
        return self._texture_name

    @property
    def unique_texture_name(self):
        return self._unique_texture_name
