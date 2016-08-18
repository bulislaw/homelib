#!/usr/bin/env python

from i2c import I2C
from time import sleep
import sys

class LCD1602(I2C):
	ROWS = 2
	COLS = 16

	CMD = 0
	DATA = 1

	BIT_RS = 1 << 0
	BIT_RW = 1 << 1
	BIT_E = 1 << 2
	BIT_BL = 1 << 3

	CMD_CLS = 1 << 0
	CMD_HOME = 1 << 1
	CMD_ENTRY = 1 << 2
	CMD_ON = 1 << 3
	CMD_FSET = 1 << 5

	SET_8BIT = 1 << 4
	SET_2LINES = 1 << 3
	SET_5X11 = 1 << 2
	ON_DISPLAY = 1 << 2
	ON_CURSOR = 1 << 1
	ON_BLINK = 1 << 0
	ENTRY_RIGHT = 1 << 1
	ENTRY_SHIFT = 1 << 0

	# Taken from the docs and tweaked till it doesn't cause problems
	WAIT_E_ON = 0.00002
	WAIT_LONG = 0.0152
	WAIT_SHORT = 0.0037


	def __init__(self, bus=1, bl=1):
		I2C.__init__(self, 0x27, bus)

		self.bl = bl

		self._write_cmd(self.CMD_FSET | self.SET_2LINES)
		self._write_cmd(self.CMD_ON | self.ON_DISPLAY)
		self._write_cmd(self.CMD_ENTRY | self.ENTRY_RIGHT)

		self.cls()

	def _wait(self, cmd):
		if cmd in [self.CMD_CLS, self.CMD_HOME]:
			sleep(self.WAIT_SHORT)
		elif cmd in [self.CMD_ENTRY, self.CMD_ON, self.CMD_FSET]:
			sleep(self.WAIT_LONG)

	def _write_byte(self, val, mode):
		val = val << 4
		if mode == self.DATA:
			val |= self.BIT_RS

		if self.bl:
			val |= self.BIT_BL

		val |= self.BIT_E
		self._write(val)
		val ^= self.BIT_E
		sleep(self.WAIT_E_ON)
		self._write(val)

	def _write_dev(self, cmd, mode):
		self._write_byte(cmd >> 4, mode)
		self._wait(cmd)
		self._write_byte(cmd & 0x0F, mode)
		self._wait(cmd)

	def _write_cmd(self, cmd):
		return self._write_dev(cmd, self.CMD)

	def _write_data(self, data):
		return self._write_dev(data, self.DATA)

	def cls(self):
		self._write_cmd(self.CMD_CLS)

	def _addr(self, c, r):
		return 0x80 + (r * 0x40) + c;

	def _putc(self, c, r, ch):
		addr = self._addr(c, r)
		self._write_cmd(addr)
		self._write_data(ch)

	def _next_pos(self, c, r):
		c += 1
		if c >= self.COLS:
			c = 0
			r += 1

		if r >= self.ROWS:
			c = 0

		return c, r

	def _next_line(self, r):
		c = 0
		r += 1
		if r >= self.ROWS:
			r = 0

		return c, r

	def printf(self, txt):
		c = 0
		r = 0
		for ch in txt:
			if ch == '\n':
				c, r = self._next_line(r)
				continue

			self._putc(c, r, ord(ch))
			c, r = self._next_pos(c, r)

	def set_bl(self, bl):
		self.bl = bl

if __name__ == "__main__":
	d = LCD1602()
	d.printf(sys.argv[1])
