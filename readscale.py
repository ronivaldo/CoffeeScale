#!/usr/bin/python
"""
# ScaleReader v0.5 - Andy Seubert - CollegeNET
# Thanks to http://steventsnyder.com/reading-a-dymo-usb-scale-using-python/ for the initial script
"""

import usb.core
import usb.util
import os
import sys

def readScale(serialno):
	VENDOR_ID = 0x0922
	PRODUCT_ID = 0x8004
	DATA_MODE_GRAMS = 2
	DATA_MODE_OUNCES = 11

	# find the USB Dymo scale devices
	devices = usb.core.find(find_all=True, idVendor=VENDOR_ID)

	## read loop
	for device in devices:		
		devbus = str(device.bus)
		devaddr = str(device.address)
		productid=str(device.idProduct)
		if str(usb.util.get_string(device,256,3)) == serialno:
			
			try:
				device.detach_kernel_driver(0)
			except Exception, e:
				pass # already unregistered

			# use the first/default configuration
			device.set_configuration()

			# first endpoint
			endpoint = device[0][(0,0)][0]

			# read a data packet
			attempts = 10
			data = None
			while data is None and attempts > 0:
				try:
					data = device.read(endpoint.bEndpointAddress,
								   endpoint.wMaxPacketSize)
				except usb.core.USBError as e:
					data = None
					if e.args == ('Operation timed out',):
						attempts -= 1
						continue
			
			# The raw scale array data
			#print data
			raw_weight = data[4] + (256 * data[5])

			if data[2] == DATA_MODE_OUNCES:
				ounces = raw_weight * 0.1
				weight = "%s oz" % ounces
			elif data[2] == DATA_MODE_GRAMS:
				grams = raw_weight
				weight = "%s g" % grams
				
			return weight
			