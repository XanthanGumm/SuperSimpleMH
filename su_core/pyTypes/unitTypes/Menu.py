from su_core.pm import mem
from su_core.pyStructures import UI
from su_core.data import Menus


class Menu:

    __instance = None
    # last menu that was open which is != from the current menu that is open
    last_open = None
    last_act = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Menu, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self._ui = None
        self._isGameActive = None
        self._invMenu = None
        self._charMenu = None
        self._skillMenu = None
        self._npcInteract = None
        self._quitMenu = None
        self._npcShop = None
        self._questsMenu = None
        self._waypointMenu = None
        self._partyMenu = None
        self._stash = None
        self._mercMenu = None
        self._act_num = None
        self._loading = None

        self._ui = mem.read_struct(mem.ui, UI)
        self._isGameActive = self._ui.isGameActive
        self._invMenu = self._ui.invMenu
        self._charMenu = self._ui.charMenu
        self._skillMenu = self._ui.skillMenu
        self._npcInteract = self._ui.npcInteract
        self._quitMenu = self._ui.quitMenu
        self._npcShop = self._ui.npcShop
        self._questsMenu = self._ui.questsMenu
        self._waypointMenu = self._ui.waypointMenu
        self._partyMenu = self._ui.partyMenu
        self._stash = self._ui.stash
        self._mercMenu = self._ui.mercMenu
        self._loading = self._ui.loading

        if self._act_num != self._ui.bAct:
            self.last_act = self._act_num
        self._act_num = self._ui.bAct

        if self._invMenu and self.last_open != Menus.invMenu:
            self.last_open = Menus.invMenu
        elif self._charMenu and self.last_open != Menus.charMenu:
            self.last_open = Menus.charMenu
        elif self._skillMenu and self.last_open != Menus.skillMenu:
            self.last_open = Menus.skillMenu
        elif self._npcInteract and self.last_open != Menus.npcInteract:
            self.last_open = Menus.npcInteract
        elif self._quitMenu and self.last_open != Menus.quitMenu:
            self.last_open = Menus.quitMenu
        elif self._npcShop and self.last_open != Menus.npcShop:
            self.last_open = Menus.npcShop
        elif self._questsMenu and self.last_open != Menus.questsMenu:
            self.last_open = Menus.questsMenu
        elif self._waypointMenu and self.last_open != Menus.waypointMenu:
            self.last_open = Menus.waypointMenu
        elif self._partyMenu and self.last_open != Menus.partyMenu:
            self.last_open = Menus.partyMenu
        elif self._stash and self.last_open != Menus.stash:
            self.last_open = Menus.stash
        elif self._mercMenu and self.last_open != Menus.mercMenu:
            self.last_open = Menus.mercMenu
        elif self._loading and self.last_open != Menus.mercMenu:
            self.last_open = Menus.loading

    @property
    def is_open(self) -> bool:
        return (
            not self._isGameActive or
            self._invMenu or
            self._charMenu or
            self._skillMenu or
            self._npcInteract or
            self._quitMenu or
            self._npcShop or
            self._questsMenu or
            self._waypointMenu or
            self._partyMenu or
            self._stash or
            self._mercMenu
        )

    @property
    def is_loading(self):
        return self._loading

    @property
    def is_game_active(self):
        return self._isGameActive

    @property
    def waypoint_menu(self):
        return self._waypointMenu


