from su_core.pm import mem
from su_core.pyStructures import UnitHashTable, Minions, LastHoverUnit
from su_core.pyTypes.unitTypes.Player import Player
from su_core.pyTypes.unitTypes.Monster import Monster
from su_core.pyTypes.unitTypes.Roster import Roster
from su_core.pyTypes.unitTypes.Menu import Menu, Menus
from su_core.data import TownNpc, MercNpc, PlayerMinionNpc
from su_core.logger import manager, traceback

_logger = manager.get_logger(__name__)


def obtain_units(unit_type: int) -> list:
    unit_types = [Player, Monster]
    obtain_type = unit_types[unit_type]

    valid_units = []
    units = mem.read_struct(mem.unit_table + unit_type * 0x400, UnitHashTable)

    for pUnit in units.table:
        if pUnit:
            # just ignore any invalid unit that changes in the middle
            try:
                valid_units.append(obtain_type(pUnit))
                while valid_units[-1].next:
                    valid_units.append(obtain_type(valid_units[-1].next))
            except Exception as e:
                _logger.debug(f"Exception occurred during a search in the unit table for a unit of type {unit_type}")
                _logger.debug(traceback.format_exc())
                pass

    return valid_units


def obtain_player() -> Player | None:
    candidates = obtain_units(unit_type=0)
    menu = Menu()
    for c in candidates:
        if c._struct.pInventory:
            check_user = mem.read_int(c._struct.pInventory + 0x70) == 0
            if not check_user:
                try:
                    c.update()
                    Player.my_player_id = c.unit_id
                    return c
                except Exception as e:
                    if menu.last_open in [Menus.waypointMenu, Menus.loading, None]:
                        return None
                    raise e
    return None


# def obtain_players() -> list[Player]:
#     players = []
#     players_units = obtain_units(0)
#     for p in players_units:
#         if p.unit_id != Player.my_player_id:
#             try:
#                 p.update()
#                 players.append(p)
#             except Exception as e:
#                 _logger.debug(f"Exception occurred during searching for players")
#                 _logger.debug(traceback.format_exc())
#
#     return players


def obtain_npcs() -> dict:
    npcs = {"unique": [], "player_minions": [], "merc": [], "town": [], "other": []}
    for npc in obtain_units(unit_type=1):
        if not npc.is_dead and not npc.is_useless and not npc.is_revived:
            # just ignore any invalid unit that changes in the middle
            try:
                npc.update()
                if not npc.read_npc_stats():
                    continue

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
            except Exception as e:
                _logger.debug(f"Exception occurred during update/read_npc_stats")
                _logger.debug(traceback.format_exc())
                pass

    return npcs


def obtain_player_minions(unit_id):
    minions = []

    try:
        minion_address = mem.read_pointer(mem.minions)

        while True:
            minion = mem.read_struct(minion_address, Minions)
            if minion.dwOwnerId == unit_id:
                minions.append(minion)

            if not minion.pNext:
                break

            minion_address = minion.pNext

    except Exception:
        # log here
        pass

    return minions


def obtain_roster_members():
    rosters = []
    roster_address = mem.read_pointer(mem.roster)

    while True:
        member = Roster(roster_address)
        rosters.append(member)

        if not member.next:
            break

        roster_address = member.next

    return rosters


def obtain_members(player_unit_id):
    player_roster = None
    in_party_rosters = dict()
    hostiled_rosters = dict()
    hostiled_members = []
    in_party_members = []
    members = []
    rosters = obtain_roster_members()
    players = obtain_units(unit_type=0)

    for r in rosters:
        if r.unit_id == player_unit_id:
            player_roster = r
            break

    for r in rosters:
        if r.unit_id != player_roster.unit_id:
            # just ignore any invalid unit that changes in the middle
            try:
                if player_roster.is_hostiled(r.unit_id):
                    hostiled_rosters[r.unit_id] = r
                if player_roster.party_id == r.party_id and r.party_id < 2 ** 16 - 1:
                    in_party_rosters[r.unit_id] = r
            except Exception as e:
                _logger.debug("Exception occurred during searching for hostiled rosters structures")
                _logger.debug(traceback.format_exc())
                pass

    for p in players:
        # just ignore any invalid unit that changes in the middle
        if p.unit_id in [r.unit_id for r in rosters] and p.unit_id != Player.my_player_id:
            try:
                p.update()
                if p.unit_id in hostiled_rosters:
                    # let's add here others players life - later I might change it.
                    p.life_percent = hostiled_rosters[p.unit_id].life_percent
                    hostiled_members.append(p)
                elif p.unit_id in in_party_rosters:
                    in_party_members.append(p)
                else:
                    members.append(p)
            except Exception as e:
                _logger.debug("Exception occurred during searching for hostiled players units")
                _logger.debug(traceback.format_exc())
                pass

    return hostiled_members, in_party_members, members, hostiled_rosters, in_party_rosters


def obtain_unit_hover():
    unit_hover = mem.read_struct(mem.last_hover, LastHoverUnit)
    return unit_hover.bIsHovered, unit_hover.dwType, unit_hover.dwUnitId


def obtain_hovered_player() -> Player | None:
    is_hovered, unit_type, unit_id = obtain_unit_hover()
    if is_hovered and unit_type == 0:
        players = obtain_units(unit_type=0)
        for p in players:
            if p.unit_id == unit_id:
                p.update()
                p.read_player_stats()
                return p

    return None
