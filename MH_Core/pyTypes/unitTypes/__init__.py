from MH_Core.pm import mem
from MH_Core.pyStructures import UnitHashTable
from MH_Core.pyTypes.unitTypes.Player import Player
from MH_Core.pyTypes.unitTypes.Menu import Menu, Menus
from MH_Core.utils.exceptions import PlayerNotFound


def obtain_units(unit_type: int) -> list:
    valid_units = []
    units = mem.read_struct(mem.unit_table + unit_type * 0x400, UnitHashTable)

    for pUnit in units.table:
        if pUnit:
            valid_units.append(Player(pUnit))
            while valid_units[-1].next:
                valid_units.append(Player(valid_units[-1].next))

    return valid_units


def obtain_player() -> Player:
    candidates = obtain_units(unit_type=0)

    for c in candidates:
        if c._struct.pInventory:
            check_user = mem.read_int(c._struct.pInventory + 0x70) == 0
            if not check_user:
                return c

    raise PlayerNotFound("Could not find player unit")


# # TODO: create ui unit, later...
# def is_manu_open() -> bool:
#     ui: UI = mem.read_struct(mem.ui, UI)
#     return (
#         not ui.inGame or
#         ui.invMenu or
#         ui.charMenu or
#         ui.skillMenu or
#         ui.npcInteract or
#         ui.quitMenu or
#         ui.npcShop or
#         ui.questsMenu or
#         ui.waypointMenu or
#         ui.partyMenu or
#         ui.stash or
#         ui.mercMenu or
#         ui.loading
#     )
