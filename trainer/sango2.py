# -*- coding: CP936 -*-

from ctypes import *
from ctypes import wintypes
from copy import deepcopy
from _multiprocessing import win32
import threading
import time

POINT_BASE = 0x004C0EB8 # 基址地址

SUPER_MAX = c_uint16(0x7FFF) # 能使用的最大值 32767
SOLDIER_MAX = c_uint16(100) # 部分能使用的最大值 100

LIFE_MAX_OFFSET = 16 # 0x10 生命上限 
LIFE_OFFSET = 18 # 0x12 生命 
POWER_MAX_OFFSET = 20 # 0x14 技力上限 
POWER_OFFSET = 22 # 0x16 技力 
FORCE_OFFSET = 52 # 0x34 武力 
INTELLIGENCE_OFFSET = 54 # 0x36 智力
MORALE_OFFSET =  56 # 0x38 士气 
FATIGUE_OFFSET = 58 # 0x3A 疲劳 
LOYALTY_OFFSET = 60 # 0x3C 忠诚

INFANTRY_MAX_OFFSET = 66 # 0x42 步兵上限
INFANTRY_OFFSET = 68 # 0x44 步兵
CAVALARY_MAX_OFFSET = 70 # 0x46 骑兵上限
CAVALARY_OFFSET = 72 # 0x48 骑兵 

KILL_SKILL_OFFSET = 84 # 0x54 必杀技第一格，单字节，向后共8个必杀技
MILITARY_ADVISER_SKILL_OFFSET = 92 # 0x5C 军师技第一格，单字节，向后共8个军师技 

HORSE_OFFSET = 153 # 0x99 马（单字节，3F赤兔马）
WEAPON_OFFSET = 155 # 0x9B 武器（单字节，2D方天画戟，2E丈八蛇矛，2F青龙偃月刀） 
BOOK_OFFSET = 157 # 0x9D 书（单字节） 

ARMS_OFFSET = 135 # 0x87 兵种（具体数值不明） 
FORMATION_OFFSET = 167 # 0xA7 阵型（具体数值不明）


gProcessHandle = 0
gBaseAddrMap = {} # {base_address: name}
gRunning = 0
gLock = threading.Lock()

#========== 读写API ==========
rPM = windll.kernel32.ReadProcessMemory
rPM.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, c_size_t, POINTER(c_size_t)]
rPM.restype = wintypes.BOOL
wPM = windll.kernel32.WriteProcessMemory
wPM.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, c_size_t, POINTER(c_size_t)]
wPM.restype = wintypes.BOOL

def openProcess():
	global gProcessHandle
	windowHandle = windll.user32.FindWindowA(None, 'SANGO II')
	if windowHandle <= 0:
		print 'SANGO II is not running.'
		return -1
	processId = c_uint32(0)
	ret = windll.user32.GetWindowThreadProcessId(windowHandle, byref(processId))
	processId = processId.value
	gProcessHandle = windll.kernel32.OpenProcess(win32.PROCESS_ALL_ACCESS, False, processId)
	return gProcessHandle

def closeProcess():
	global gProcessHandle
	return windll.kernel32.CloseHandle(gProcessHandle)

def readBase():
	global gProcessHandle
	baseAddr = c_uint32(0)
	readSize = c_size_t()
	ret = rPM(gProcessHandle, POINT_BASE, byref(baseAddr), 4, byref(readSize))
	# print 'ret = {}'.format(ret)
	# print 'readSize = {}'.format(readSize.value)
	# print 'baseAddr = 0x{:0>8x}'.format(baseAddr.value)
	if ret and readSize.value == 4:
		return baseAddr.value

def writeValue(baseAddr):
	global gProcessHandle
	writeSize = c_size_t()
	# 体力上限
	wPM(gProcessHandle, baseAddr + LIFE_MAX_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 体力
	wPM(gProcessHandle, baseAddr + LIFE_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 技力上限
	wPM(gProcessHandle, baseAddr + POWER_MAX_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 技力
	wPM(gProcessHandle, baseAddr + POWER_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 武力
	wPM(gProcessHandle, baseAddr + FORCE_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 智力
	wPM(gProcessHandle, baseAddr + INTELLIGENCE_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 士气
	wPM(gProcessHandle, baseAddr + MORALE_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 疲劳
	wPM(gProcessHandle, baseAddr + FATIGUE_OFFSET, byref(c_uint16(0)), 2, byref(writeSize))
	# 忠诚
	wPM(gProcessHandle, baseAddr + LOYALTY_OFFSET, byref(SUPER_MAX), 2, byref(writeSize))
	# 步兵上限
	wPM(gProcessHandle, baseAddr + INFANTRY_MAX_OFFSET, byref(SOLDIER_MAX), 2, byref(writeSize))
	# 步兵
	wPM(gProcessHandle, baseAddr + INFANTRY_OFFSET, byref(SOLDIER_MAX), 2, byref(writeSize))
	# 骑兵上限
	wPM(gProcessHandle, baseAddr + CAVALARY_MAX_OFFSET, byref(SOLDIER_MAX), 2, byref(writeSize))
	# 骑兵
	wPM(gProcessHandle, baseAddr + CAVALARY_OFFSET, byref(SOLDIER_MAX), 2, byref(writeSize))
	# 坐骑
	wPM(gProcessHandle, baseAddr + HORSE_OFFSET, byref(c_uint8(0x3F)), 1, byref(writeSize))
	# 武器
	wPM(gProcessHandle, baseAddr + WEAPON_OFFSET, byref(c_uint8(0x2F)), 1, byref(writeSize))
	# 书本
	#wPM(gProcessHandle, baseAddr + BOOK_OFFSET, byref(c_uint8(??)), 1, byref(writeSize))
	# 必杀技
	wPM(gProcessHandle, baseAddr + KILL_SKILL_OFFSET + 7, byref(c_uint8(43)), 1, byref(writeSize))
	# 军师技
	wPM(gProcessHandle, baseAddr + MILITARY_ADVISER_SKILL_OFFSET + 7, byref(c_uint8(55)), 1, byref(writeSize))



class LockValueInBackground(threading.Thread):
	def run(self):
		global gRunning
		global gBaseAddrMap
		global gLock
		while gRunning:
			gLock.acquire()
			m = deepcopy(gBaseAddrMap)
			gLock.release()
			for b in m:
				writeValue(b)
				time.sleep(0.1)







def main():
	global gRunning
	global gBaseAddrMap
	global gLock
	print openProcess()
	vl = LockValueInBackground()
	gRunning = 1
	vl.start()
	while 1:
		cmd = raw_input()
		if cmd.strip().lower() == 'exit':
			break
		b = readBase()
		if b in gBaseAddrMap:
			print '0x{:0>8x}:{} is already in map.'.format(b, gBaseAddrMap[b])
		else:
			gLock.acquire()
			gBaseAddrMap[b] = cmd
			gLock.release()
			print '0x{:0>8x}:{} has been put into map.'.format(b, cmd)
	gRunning = 0
	print closeProcess()
	print 'Program stopped.'


if '__main__' == __name__:
	main()
