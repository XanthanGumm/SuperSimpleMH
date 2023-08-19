import ast
import ctypes as ct
from su_core.pm import mem
from su_core.pyTypes.unitTypes.Item import Item
from su_core.pyStructures import Inventory, InventoryGrid


class Inventories:
    def __init__(self, address):
        self._address = address
        self._struct = None
        self._struct_inventories = None
        self._owner_id = None
        self._weapon_id = None
        self._sig = None
        self._helm = None
        self._amulet = None
        self._armor = None
        self._arm_left = None
        self._arm_right = None
        self._ring_left = None
        self._ring_right = None
        self._belt = None
        self._gloves = None
        self._boots = None
        self._arm_switch_left = None
        self._arm_switch_right = None
        self._grid: list[list[Item | None]] = [[None] * 10 for _ in range(4)]
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, Inventory)
        self._struct_inventories = mem.read_struct(self._struct.pInventoryGrid, InventoryGrid)
        self._owner_id = self._struct.dwOwnerId
        self._weapon_id = self._struct.dwWeaponId
        self._sig = self._struct.dwSignature

    def read_equip_items(self):
        body_raw_ptrs = mem.read_bytes(self._struct_inventories.pEquipList, 13 * 8)
        equip_items_arr = (ct.c_void_p * 13).from_buffer_copy(body_raw_ptrs)
        if equip_items_arr[1]:
            self._helm = Item(equip_items_arr[1])
        if equip_items_arr[2]:
            self._amulet = Item(equip_items_arr[2])
        if equip_items_arr[3]:
            self._armor = Item(equip_items_arr[3])
        if equip_items_arr[4]:
            self._arm_left = Item(equip_items_arr[4])
        if equip_items_arr[5]:
            self._arm_right = Item(equip_items_arr[5])
        if equip_items_arr[6]:
            self._ring_left = Item(equip_items_arr[6])
        if equip_items_arr[7]:
            self._ring_right = Item(equip_items_arr[7])
        if equip_items_arr[8]:
            self._belt = Item(equip_items_arr[8])
        if equip_items_arr[9]:
            self._boots = Item(equip_items_arr[9])
        if equip_items_arr[10]:
            self._gloves = Item(equip_items_arr[10])
        if equip_items_arr[11]:
            self._arm_switch_left = Item(equip_items_arr[11])
        if equip_items_arr[12]:
            self._arm_switch_right = Item(equip_items_arr[12])

    def read_grid_charms(self):
        r_l = len(self._grid[0])  # grid row length - number of nodes in a raw
        c_l = len(self._grid)  # grid col length - number of nodes in a column
        grid_raw_ptrs = mem.read_bytes(self._struct_inventories.pInventoryList, 40 * 8)
        grid_ptrs = (ct.c_void_p * 40).from_buffer_copy(grid_raw_ptrs)
        for i in range(40):
            if grid_ptrs[i]:
                g_r = i // r_l  # grid raw in 2d array
                g_c = i % r_l  # grid col in 2d array
                self._grid[g_r][g_c] = Item(grid_ptrs[i])

    @property
    def helm(self) -> Item:
        return self._helm

    @property
    def amulet(self) -> Item:
        return self._amulet

    @property
    def armor(self) -> Item:
        return self._armor

    @property
    def arm_left(self) -> Item:
        return self._arm_left

    @property
    def arm_right(self) -> Item:
        return self._arm_right

    @property
    def ring_left(self) -> Item:
        return self._ring_left

    @property
    def ring_right(self) -> Item:
        return self._ring_right

    @property
    def belt(self) -> Item:
        return self._belt

    @property
    def gloves(self) -> Item:
        return self._gloves

    @property
    def boots(self) -> Item:
        return self._boots

    @property
    def arm_switch_left(self) -> Item:
        return self._arm_switch_left

    @property
    def arm_switch_right(self) -> Item:
        return self._arm_switch_right

    @property
    def inv_grid(self) -> list[list[Item | None]]:
        return self._grid

    def __getitem__(self, key: int | str) -> Item:
        if key == "helm":
            return self._helm
        elif key == "amulet":
            return self._amulet
        elif key == "armor":
            return self._armor
        elif key == "arm_left":
            return self._arm_left
        elif key == "arm_right":
            return self._arm_right
        elif key == "ring_left":
            return self._ring_left
        elif key == "ring_right":
            return self._ring_right
        elif key == "belt":
            return self._belt
        elif key == "gloves":
            return self._gloves
        elif key == "boots":
            return self._boots
        elif key == "arm_switch_left":
            return self._arm_switch_left
        elif key == "arm_switch_right":
            return self._arm_switch_right
        elif "charms" in key:
            i, j = ast.literal_eval(key.split("_")[1])
            return self._grid[i][j]
        else:
            raise KeyError(f"Key: {key} of type: {type(key)} is not supported")
