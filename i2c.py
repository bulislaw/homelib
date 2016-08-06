#!/usr/bin/python

import time
import array
import io
import fcntl
from struct import pack, unpack

class I2C(object):
	def __init__(self, adr, bus):
		self.I2C_SLAVE=0x0703
		self.rx = io.open("/dev/i2c-" + str(bus), "rb", buffering=0)
		self.tx = io.open("/dev/i2c-" + str(bus), "wb", buffering=0)

		fcntl.ioctl(self.rx, self.I2C_SLAVE, adr)
		fcntl.ioctl(self.tx, self.I2C_SLAVE, adr)

	def _write(self, data):
		self.tx.write(pack('B', data))

	def _read(self, size):
		return unpack('B'*size, self.rx.read(size))

	def close(self):
		self.tx.close()
		self.rx.close()

