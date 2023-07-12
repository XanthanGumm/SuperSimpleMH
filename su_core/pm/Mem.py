import sys
import ctypes as ct
import pyMeow as pm
from typing import Type


class Mem:

    unit_table_offset = "48 03 C7 49 8B 8C C6"
    expansion_offset = "48 8B 05 ?? ?? ?? ?? 48 8B D9 F3 0F 10 50"
    ui_offset = "40 84 ED 0F 94 05"
    minions_offset = "48 8B 05 ?? ?? ?? ?? 48 89 41 30 89 59 08"
    roster_offset = "02 45 33 D2 4D 8B"

    def __init__(self):

        try:
            self.proc = pm.open_process("D2R.exe")
            self.base = pm.get_module(self.proc, "D2R.exe")["base"]
        except Exception as e:
            sys.exit(e)

        self._expansion_address = None
        self._unit_table_address = None
        self._ui_address = None
        self._minions_address = None
        self._roster_address = None
        self.update()

    def update(self):
        self._unit_table_address = self.get_unit_table_address()
        self._expansion_address = self.get_expansion_address()
        self._ui_address = self.get_ui_address()
        self._minions_address = self.get_minions_address()
        self._roster_address = self.get_roster_address()

    def get_unit_table_address(self):
        """
        retrieve absolute address of the unit table
        :return: unit hash table address
        """
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.unit_table_offset)
        assert len(pattern_address) == 1, "Unit table address aob scan error."

        unit_table_offset = pm.r_int(self.proc, pattern_address[0] + 7)
        return self.base + unit_table_offset

    def get_expansion_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.expansion_offset)
        assert len(pattern_address) == 1, "Expansion aob scan error."

        relative_address = pm.r_int(self.proc, pattern_address[0] + 3)
        delta = pattern_address[0] - self.base
        return self.base + delta + 7 + relative_address

    def get_ui_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.ui_offset)
        assert len(pattern_address) == 1, "UI aob scan error."

        relative_address = pm.r_int(self.proc, pattern_address[0] + 6)
        delta = pattern_address[0] - self.base
        return self.base + delta + relative_address  # + 10

    def get_minions_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.minions_offset)
        assert len(pattern_address) == 1, "UI aob scan error."

        relative_address = pm.r_int(self.proc, pattern_address[0] + 3)
        delta = pattern_address[0] - self.base
        return self.base + delta + relative_address + 7

    def get_roster_address(self):
        pattern_address = pm.aob_scan_module(self.proc, "D2R.exe", self.roster_offset)
        assert len(pattern_address) == 1, "Roster aob scan error."

        relative_address = pm.r_int(self.proc, pattern_address[0] - 3)
        delta = pattern_address[0] - self.base
        return self.base + delta + relative_address + 1

    def read_struct(self, address, Ts: Type[ct.Structure]) -> ct.Structure:
        assert issubclass(Ts, ct.Structure), "Ts is not a C structure"
        return Ts.from_buffer_copy(pm.r_bytes(self.proc, address, ct.sizeof(Ts)))

    def read_int(self, address):
        return pm.r_int(self.proc, address)

    def read_bytes(self, address, num_bytes):
        return pm.r_bytes(self.proc, address, num_bytes)

    def read_pointer(self, address):
        return pm.r_int64(self.proc, address)

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


if __name__ == "__main__":
    mem = Mem()
    print("[!] Unitable address: ", hex(mem.unit_table))
    print("[!] Expansion address: ", hex(mem.expansion))
