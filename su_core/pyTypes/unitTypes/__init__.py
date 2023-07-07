from su_core.pm import mem
from su_core.pyStructures import UnitHashTable, Minions
from su_core.pyTypes.unitTypes.Player import Player
from su_core.pyTypes.unitTypes.Monster import Monster
from su_core.pyTypes.unitTypes.Menu import Menu, Menus
from su_core.utils.exceptions import PlayerNotFound
from su_core.data import TownNpc, MercNpc, PlayerMinionNpc


def obtain_units(unit_type: int) -> list:
    unit_types = [Player, Monster]
    obtain_type = unit_types[unit_type]

    valid_units = []
    units = mem.read_struct(mem.unit_table + unit_type * 0x400, UnitHashTable)

    for pUnit in units.table:
        if pUnit:
            valid_units.append(obtain_type(pUnit))
            while valid_units[-1].next:
                valid_units.append(obtain_type(valid_units[-1].next))

    return valid_units


def obtain_player() -> Player:
    candidates = obtain_units(unit_type=0)
    for c in candidates:
        c.update()
        if c._struct.pInventory:
            check_user = mem.read_int(c._struct.pInventory + 0x70) == 0
            if not check_user:
                return c

    raise PlayerNotFound("Could not find player unit")


def obtain_npcs(in_town) -> dict:
    npcs = {"unique": [], "player_minions": [], "merc": [], "town": [], "other": []}
    # npcs = []
    for npc in obtain_units(unit_type=1):
        # just ignore any invalid unit that changes in the middle
        try:
            npc.update()
            if not npc.is_dead and not npc.is_useless:
                npc.read_resistances()
                if npc.npc in MercNpc:
                    npcs["merc"].append(npc)
                elif npc.npc in TownNpc:
                    npcs["town"].append(npc)
                elif npc.npc in PlayerMinionNpc:
                    npcs["player_minions"].append(npc)
                elif npc.is_strong_monster:
                    npcs["unique"].append(npc)
                else:
                    npcs["other"].append(npc)
                # npcs.append(npc)
        except Exception as e:
            print(e)
            pass

    # if in_town:
    #     npcs = [npc for npc in npcs if npc.npc in TownNpc]

    return npcs


def obtain_player_minions(unit_id):
    minions = []
    minion_address = mem.read_pointer(mem.minions)

    while True:
        minion = mem.read_struct(minion_address, Minions)
        if minion.dwOwnerId == unit_id:
            minions.append(minion)

        if not minion.pNext:
            break

        minion_address = minion.pNext

    return minions
