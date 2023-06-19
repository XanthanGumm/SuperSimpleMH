import os
import inspect
from functools import wraps
from ctypes import CDLL
from ctypes import c_uint32
from ctypes import c_int32
from ctypes import c_char_p
from ctypes import c_bool
from pyWrappers.pyStructures import *


def signature(*args, **kwargs):
    if len(args):
        raise TypeError("Allowing only keywords arguments")

    def decorator(fn):
        sig_func = inspect.signature(fn)
        sig_types = inspect.signature(signature)

        @wraps(fn)
        def wrapper(*fn_args, **fn_kwargs):
            func_args = sig_func.bind(*fn_args, **fn_kwargs)
            type_args = sig_types.bind(*args, **kwargs).kwargs
            for arg_name, arg_type in type_args.items():
                if func_args.arguments.get(arg_name):
                    if not isinstance(func_args.arguments.get(arg_name), arg_type):
                        func_args.arguments[arg_name] = arg_type(func_args.arguments[arg_name])
                if func_args.kwargs.get(arg_name):
                    if not isinstance(func_args.kwargs.get(arg_name), arg_type):
                        func_args.kwargs[arg_name] = arg_type(func_args.kwargs[arg_name])
            return fn(*func_args.args, **func_args.kwargs)
        return wrapper
    return decorator


class ApiWrapper:

    def __init__(self, d2lod_path: bytes):
        root = os.path.join(os.path.dirname(__file__), "..")
        api_lib = CDLL(os.path.join(root, "MapApi.dll"))
        self._path = c_char_p(d2lod_path)

        self._Initialize = api_lib["Initialize"]
        self._Initialize.argtypes = [c_char_p]
        self._Initialize.restype = c_bool

        self._InitLevel = api_lib["InitLevel"]
        self._InitLevel.argtypes = [POINTER(Level)]
        self._InitLevel.restype = None

        self._GetLevel = api_lib["GetLevel"]
        self._GetLevel.argtypes = [POINTER(ActMisc), DWORD]
        self._GetLevel.restype = POINTER(Level)

        self._GetLevelTxt = api_lib["GetLevelTxt"]
        self._GetLevelTxt.argtypes = [DWORD]
        self._GetLevelTxt.restype = POINTER(LevelTxt)

        self._GetObjectTxt = api_lib["GetObjectTxt"]
        self._GetObjectTxt.argtypes = [DWORD]
        self._GetObjectTxt.restype = POINTER(ObjectTxt)

        self._AddRoomData = api_lib["AddRoomData"]
        self._AddRoomData.argtypes = [POINTER(Act), c_int32, c_int32, c_int32, POINTER(Room1)]
        self._AddRoomData.restype = None

        self._RemoveRoomData = api_lib["RemoveRoomData"]
        self._RemoveRoomData.argtypes = [POINTER(Act), c_int32, c_int32, c_int32, POINTER(Room1)]
        self._RemoveRoomData.restype = None

        self._LoadAct = api_lib["LoadAct"]
        self._LoadAct.argtypes = [c_uint32, c_uint32, c_uint32, c_uint32]
        self._LoadAct.restype = POINTER(Act)

        self._UnloadAct = api_lib["UnloadAct"]
        self._UnloadAct.argtypes = [POINTER(Act)]
        self._UnloadAct.restype = None

    def initialize(self) -> bool:
        return self._Initialize(self._path)

    def init_level(self, p_level: POINTER(Level)):
        self._InitLevel(p_level)

    @signature(misc=POINTER(ActMisc), level_no=c_uint32)
    def get_level(self, misc, level_no) -> POINTER(Level):
        level_txt = self._GetLevelTxt(level_no)
        if not level_txt:
            raise ValueError("[-] LevelTxt is NULL")
        return self._GetLevel(misc, level_no)

    @signature(dwTxtFileNo=c_uint32)
    def get_object_txt(self, dwTxtFileNo) -> POINTER(ObjectTxt):
        return self._GetObjectTxt(dwTxtFileNo)

    def add_room_data(self,
                      p_act: POINTER(Act),
                      level_id: c_int32,
                      x_pos: c_int32,
                      y_pos: c_int32,
                      p_room: POINTER(Room1)):
        self._AddRoomData(p_act, level_id, x_pos, y_pos, p_room)

    def remove_room_data(self,
                         p_act: POINTER(Act),
                         level_id: c_int32,
                         x_pos: c_int32,
                         y_pos: c_int32,
                         p_room: POINTER(Room1)):
        self._RemoveRoomData(p_act, level_id, x_pos, y_pos, p_room)

    @signature(act_no=c_uint32, seed=c_uint32, difficulty=c_uint32, town_lvl_id=c_uint32)
    def load_act(self,
                 act_no,
                 seed,
                 difficulty,
                 town_lvl_id) -> POINTER(Act):
        return self._LoadAct(act_no, seed, difficulty, town_lvl_id)

    def unload_act(self, p_act: POINTER(Act)):
        self._UnloadAct(p_act)
