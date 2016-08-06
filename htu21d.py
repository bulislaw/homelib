#!/usr/bin/python

import time
from i2c import I2C
import sqlite3

class HTU21D(I2C):
	def __init__(self, bus = 1):
		I2C.__init__(self, 0x40, bus)

		self.CMD_RESET = 0xFE
		self.CMD_READ_TEMP_NO_HOLD = 0xE3
		self.CMD_READ_HUM_NO_HOLD = 0xF5
		self.CMD_READ_REG = 0xE7
		self.CMD_WRITE_REG = 0xE6

	def reset(self):
		self._write(self.CMD_RESET)
		time.sleep(0.05)

	def read_reg(self):
		self._write(self.CMD_READ_REG)
		time.sleep(0.5)
		data = self._read(1)[0]

		return data

	def write_reg(self, reg):
		self._write(self.CMD_WRITE_REG)
		time.sleep(0.5)
		self._write(reg)

	def read_hum(self):
		self._write(self.CMD_READ_HUM_NO_HOLD)
		time.sleep(0.5)
		data = self._read(3)
		tmp = (data[0] << 8 | data[1]) & 0xFFFC
		return round(-6.0 + 125.0*tmp/65536.0, 2)

	def read_temp(self):
		self._write(self.CMD_READ_TEMP_NO_HOLD)
		time.sleep(0.055)
		data = self._read(3)
		tmp = (data[0] << 8 | data[1]) & 0xFFFC
		return round(-46.85 + 175.72*tmp/65536.0, 2)

if __name__ == "__main__":
	temp = HTU21D()
	time.sleep(1)
	temp.reset()
	time.sleep(1)
	print temp.read_temp()
	temp.close()
