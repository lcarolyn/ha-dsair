import struct

from .ctrl_enum import EnumCmdType, EnumDevice


class Encode:
    def __init__(self):
        self._fmt = '<'
        self._len = 0
        self._list = []

    def write1(self, d):
        self._fmt += 'B'
        self._len += 1
        self._list.append(d)

    def write2(self, d):
        self._fmt += 'H'
        self._len += 2
        self._list.append(d)

    def write4(self, d):
        self._fmt += 'I'
        self._len += 4
        self._list.append(d)

    def writes(self, d):
        self._fmt += str(len(d))+'s'
        self._len += len(d)

    def pack(self):
        self._list[1] = self._len - 4
        return struct.pack(self._fmt, *self._list)

    @property
    def len(self):
        return self._len


class Param:
    cnt = 0

    def __init__(self, device_type: EnumDevice, cmd_type: EnumCmdType, has_result):
        self.cmd_type = cmd_type
        self.device_type = device_type
        self.has_result = has_result
        self.sub_body_ver = 0
        self.need_ack = 1

    def generate_subbody(self, s):
        return

    def to_string(self):
        s = Encode()
        s.write1(2)  # 0 保留字
        s.write2(16)  # 1~2 长度，不含首尾保留字及长度本身
        s.write1(13)  # 3 保留字
        s.write1(0)  # 4 保留字
        s.write1(self.sub_body_ver)  # 5 子体版本
        s.write1(0)  # 6 保留字
        Param.cnt += 1
        s.write4(Param.cnt)  # 7~10 自增命令ID
        s.write1(self.device_type.value[0])  # 11 设备类型
        s.write4(self.device_type.value[1])  # 12~15 设备类型id
        s.write1(self.need_ack)  # 16 是否需要ack
        s.write2(self.cmd_type.value)  # 17~18 命令类型id
        self.generate_subbody(s)
        s.write1(3)  # 最后一位 保留字
        return s.pack()


class SystemParam(Param):
    def __init__(self, cmd_type, has_result):
        Param.__init__(self, EnumDevice.SYSTEM, cmd_type, has_result)


class HandShakeParam(SystemParam):
    def __init__(self):
        SystemParam.__init__(self, EnumCmdType.SYS_HAND_SHAKE, True)
