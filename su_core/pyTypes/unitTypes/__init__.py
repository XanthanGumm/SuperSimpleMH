from su_core.pm import mem
from su_core.pyStructures import UnitHashTable, Minions
from su_core.pyTypes.unitTypes.Player import Player
from su_core.pyTypes.unitTypes.Monster import Monster
from su_core.pyTypes.unitTypes.Roster import Roster
from su_core.pyTypes.unitTypes.Menu import Menu, Menus
from su_core.utils.exceptions import PlayerNotFound, InvalidPlayerUnit
from su_core.data import TownNpc, MercNpc, PlayerMinionNpc


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
                if not isinstance(e, InvalidPlayerUnit):
                    print(e)

    return valid_units


def obtain_player() -> Player:
    candidates = obtain_units(unit_type=0)
    for c in candidates:
        if c._struct.pInventory:
            check_user = mem.read_int(c._struct.pInventory + 0x70) == 0
            if not check_user:
                Player.my_player_id = c.unit_id
                return c

    raise PlayerNotFound("Could not find player unit")


def obtain_npcs(in_town) -> dict:
    npcs = {"unique": [], "player_minions": [], "merc": [], "town": [], "other": []}
    for npc in obtain_units(unit_type=1):
        if not npc.is_dead and not npc.is_useless:
            # just ignore any invalid unit that changes in the middle
            try:
                npc.read_stats()
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
                print(e)

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


def obtain_hostiled_players(player_unit_id):
    player_roster = None
    hostiled_rosters = dict()
    hostiled_players = []
    rosters = obtain_roster_members()
    players = obtain_units(unit_type=0)

    for r in rosters:
        if r.unit_id == player_unit_id:
            player_roster = r
            break

    for r in rosters:
        # just ignore any invalid unit that changes in the middle
        try:
            if player_roster.is_hostiled(r.unit_id):
                hostiled_rosters[r.unit_id] = r
                print(r.name, r.life_percent)
        except Exception as e:
            print(e)
            pass

    for p in players:
        if p.unit_id in hostiled_rosters:
            # just ignore any invalid unit that changes in the middle
            try:
                # let's add here others players life - later I might change it.
                p.read_stats()
                p.life_percent = hostiled_rosters[p.unit_id].life_percent
                hostiled_players.append(p)
            except Exception as e:
                print(e)

    return hostiled_players, hostiled_rosters



