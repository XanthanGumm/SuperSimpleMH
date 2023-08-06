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
        self._switch_left = None
        self._switch_right = None
        self._grid = None
        self.update()

    def update(self):
        self._struct = mem.read_struct(self._address, Inventory)
        self._struct_inventories = mem.read_struct(self._struct.pInventoryGrid, InventoryGrid)
        self._owner_id = self._struct.dwOwnerId
        self._weapon_id = self._struct.dwWeaponId
        self._sig = self._struct.dwSignature

    def read_equip_items(self):
        raw_address = mem.read_bytes(self._struct_inventories.pEquipList, 13 * 8)
        equip_items_addresses = (ct.c_void_p * 13).from_buffer_copy(raw_address)
        if equip_items_addresses[1]:
            self._helm = Item(equip_items_addresses[1])
        if equip_items_addresses[2]:
            self._amulet = Item(equip_items_addresses[2])
        if equip_items_addresses[3]:
            self._armor = Item(equip_items_addresses[3])
        if equip_items_addresses[4]:
            self._arm_left = Item(equip_items_addresses[4])
        if equip_items_addresses[5]:
            self._arm_right = Item(equip_items_addresses[5])
        if equip_items_addresses[6]:
            self._ring_left = Item(equip_items_addresses[6])
        if equip_items_addresses[7]:
            self._ring_right = Item(equip_items_addresses[7])
        if equip_items_addresses[8]:
            self._belt = Item(equip_items_addresses[8])
        if equip_items_addresses[9]:
            self._boots = Item(equip_items_addresses[9])
        if equip_items_addresses[10]:
            self._gloves = Item(equip_items_addresses[10])
        if equip_items_addresses[11]:
            self._switch_left = Item(equip_items_addresses[11])
        if equip_items_addresses[12]:
            self._switch_right = Item(equip_items_addresses[12])

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
    def switch_left(self) -> Item:
        return self._switch_left

    @property
    def switch_right(self) -> Item:
        return self._switch_right

    def __getitem__(self, key):
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
        elif key == "switch_left":
            return self._switch_left
        elif key == "switch_right":
            return self._switch_right
        else:
            raise KeyError(f"Key: {key} is not a body location")

