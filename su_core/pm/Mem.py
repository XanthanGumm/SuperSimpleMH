import sys
import ctypes as ct
import pyMeow as pm
from typing import Type
from logger import manager


class Mem:

    unit_table_offset = "48 03 C7 49 8B 8C C6"
    expansion_offset = "48 8B 05 ?? ?? ?? ?? 48 8B D9 F3 0F 10 50"
    ui_offset = "40 84 ED 0F 94 05"
    minions_offset = "48 8B 05 ?? ?? ?? ?? 48 89 41 30 89 59 08"
    roster_offset = "02 45 33 D2 4D 8B"
    hover_offset = "C6 84 C2 ?? ?? ?? ?? ?? 48 8B 74 24 ??"

    def __init__(self):

        try:
            self.proc = pm.open_process("D2R.exe")
            self.base = pm.get_module(self.proc, "D2R.exe")["base"]
        except Exception as e:
            sys.exit(e)

        self._logger = manager.get_logger(__name__)
        self._expansion_address = None
        self._unit_table_address = None
        self._ui_address = None
        self._minions_address = None
        self._roster_address = None
        self._hover_address = None
        self.update()

    def update(self):
        self._unit_table_address = self.get_unit_table_address()
        self._expansion_address = self.get_expansion_address()
        self._ui_address = self.get_ui_address()
        self._minions_address = self.get_minions_address()
        self._roster_address = self.get_roster_address()
        self._hover_address = self.get_last_hover_address()

    def get_unit_table_address(self):
        """
        retrieve absolute address of the unit table
        :return: unit hash table address
        """
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.unit_table_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find unit table offset with pattern: {self.unit_table_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"Unit table has been found at offset: {hex(pattern_address[0])} + (7)")
        else:
            self._logger.warning(f"Found more then one unit table offset with pattern: {self.unit_table_offset}")

        unit_table_offset = pm.r_int(self.proc, pattern_address[0] + 7)

        address = self.base + unit_table_offset
        self._logger.debug(f"Found unit table address: {hex(address)} at r_int(pattern + 7)\n")
        return address

    def get_expansion_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.expansion_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find expansion offset with pattern: {self.expansion_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"Expansion has been found at offset: {hex(pattern_address[0])} + (3)")
        else:
            self._logger.warning(f"Found more then one Expansion offset with pattern: {self.expansion_offset}")

        relative_address = pm.r_int(self.proc, pattern_address[0] + 3)
        delta = pattern_address[0] - self.base

        address = self.base + delta + 7 + relative_address
        self._logger.debug(f"Found Expansion address: {hex(address)} at r_int(pattern + 3) + pattern - base + 7\n")
        return address

    def get_ui_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.ui_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find UI offset with pattern: {self.ui_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"UI has been found at offset: {hex(pattern_address[0])} + (6)")
        else:
            self._logger.warning(f"Found more then one UI offset with pattern: {self.ui_offset}")

        relative_address = pm.r_int(self.proc, pattern_address[0] + 6)
        delta = pattern_address[0] - self.base

        address = self.base + delta + relative_address  # + 10
        self._logger.debug(f"Found UI address: {hex(address)} at r_int(pattern + 6) + pattern - base\n")
        return address

    def get_minions_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.minions_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find players minions offset with pattern: {self.minions_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"Players minions has been found at offset: {hex(pattern_address[0])} + (3)")
        else:
            self._logger.warning(f"Found more then one players minions offset with pattern: {self.minions_offset}")

        relative_address = pm.r_int(self.proc, pattern_address[0] + 3)
        delta = pattern_address[0] - self.base

        address = self.base + delta + relative_address + 7
        self._logger.debug(f"Found players minions address: {hex(address)} at r_int(pattern + 3) + pattern - base + 7\n")
        return address

    def get_roster_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.roster_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find roster offset with pattern: {self.roster_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"Roster has been found at offset: {hex(pattern_address[0])} - (3)")
        else:
            self._logger.warning(f"Found more then one roster offset with pattern: {self.roster_offset}")

        relative_address = pm.r_int(self.proc, pattern_address[0] - 3)
        delta = pattern_address[0] - self.base

        address = self.base + delta + relative_address + 1
        self._logger.debug(f"Found roster address: {hex(address)} at r_int(pattern - 3) + pattern - base + 1\n")
        return address

    def get_last_hover_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.hover_offset)
        if len(pattern_address) == 0:
            self._logger.warning(f"Could not find last hover offset with pattern: {self.hover_offset}")
        elif len(pattern_address) == 1:
            self._logger.info(f"Last hover has been found at offset: {hex(pattern_address[0])} + (3)")
        else:
            self._logger.warning(f"Found more then one last hover offset with pattern: {self.hover_offset}")

        relative_address = pm.r_int(self.proc, pattern_address[0] + 3) - 1

        address = self.base + relative_address
        self._logger.debug(f"Found last hover address: {hex(address)} at r_int(pattern + 3) - 1\n")
        return address

    def read_struct(self, address, Ts: Type[ct.Structure]) -> ct.Structure:
        assert issubclass(Ts, ct.Structure), "Ts is not a C structure"
        return Ts.from_buffer_copy(pm.r_bytes(self.proc, address, ct.sizeof(Ts)))

    def read_structure(self, address, Ts: Type[ct.Structure]) -> ct.Structure:
        return pm.r_ctype(self.proc, address, Ts())

    def read_int(self, address):
        return pm.r_int(self.proc, address)

    def read_bytes(self, address, num_bytes):
        return pm.r_bytes(self.proc, address, num_bytes)

    def read_pointer(self, address):
        return pm.r_int64(self.proc, address)

    def read_uint(self, address):
        return pm.r_uint(self.proc, address)

    @property
    def expansion(self):
        return self._expansion_address

    @property
    def unit_table(self):
        return self._unit_table_address

    @property
    def ui(self):
        return self._ui_address

    @property
    def minions(self):
        return self._minions_address

    @property
    def roster(self):
        return self._roster_address

    @property
    def last_hover(self):
        return self._hover_address


if __name__ == "__main__":
    mem = Mem()
    print("[!] Unitable address: ", hex(mem.unit_table))
    print("[!] Expansion address: ", hex(mem.expansion))
