import numpy as np
import matplotlib.pyplot as plt
import gensignal as gs
import copy
import struct
import time
import random
from CRC16Kermit import CRC16Kermit

def getHex(x):
	t={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
	return t[x]

def getHex1(x):
	t={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
	return t[x]


def getSubsetandShift(signals, regionSize, shift, bandwidth):
	SIZE = 64
	length = len(signals)
	Group = length / SIZE
	cutSignals = [[0,0] for i in range(Group*regionSize)]
	delta = bandwidth / 2
	for i in range(Group):
		partSignals = copy.deepcopy(signals[i*SIZE+SIZE/2-delta:i*SIZE+SIZE/2+delta+1])
		for j in range(-delta,delta+1):
			cutSignals[i*regionSize + regionSize / 2 + shift + j][0] = partSignals[j+delta][0]
			cutSignals[i*regionSize + regionSize / 2 + shift + j][1] = partSignals[j+delta][1]
	return cutSignals

def getSubsetandShift2(signals1, signals2, regionSize, shift1, shift2, bandwidth):
	SIZE = 64
	length = len(signals1)
	Group = length / SIZE
	cutSignals = [[0,0] for i in range(Group*regionSize)]
	delta = bandwidth / 2
	for i in range(Group):
		partSignals1 = copy.deepcopy(signals1[i*SIZE+SIZE/2-delta:i*SIZE+SIZE/2+delta+1])
		N = len(partSignals1)
		for j in range(-delta,delta+1):
			cutSignals[i*regionSize + regionSize / 2 + shift1 + j][0] = partSignals1[j+delta][0]
			cutSignals[i*regionSize + regionSize / 2 + shift1 + j][1] = partSignals1[j+delta][1]
		
		partSignals2 = copy.deepcopy(signals2[i*SIZE+SIZE/2-delta:i*SIZE+SIZE/2+delta+1])
		N = len(partSignals2)
		for j in range(-delta,delta+1):
			cutSignals[i*regionSize + regionSize / 2 + shift2 + j][0] = partSignals2[j+delta][0]
			cutSignals[i*regionSize + regionSize / 2 + shift2 + j][1] = partSignals2[j+delta][1]

	return cutSignals

def cycleshift(symbol, offset):
	length = len(symbol)
	tsymbol = [0 for i in range(length)]
	for i in range(length):
		tsymbol[i] = symbol[i]
	if offset >= 0:
		csymbol = tsymbol[offset:]+tsymbol[:offset]
	if offset <= 0:
		offset = length + offset
		csymbol = tsymbol[offset:]+tsymbol[:offset]
	return csymbol

def generateAllSymbols():
	subc = 5
	ratio = float(1.0801) / 60
	delta = float(1.0801 *2) / 14
	ratio = ratio * 2
	approxfftAllIQs = []
	for symbol in range(16):
		approxfftIs = gs.generateISignal(symbol, ratio, subc)
		approxfftQs = gs.generateQSignal(symbol, ratio, subc)
		approxfftIQs = []

		for i in range(len(approxfftIs)):
			approxfftIQs.append([approxfftIs[i][0]+approxfftQs[i][0], approxfftIs[i][1]+approxfftQs[i][1]])
	
		qam = gs.generateQAM(64,1.0801)
		#qam.append([0,0])
		approxfftIQs = gs.approxQAM(qam, approxfftIQs)

		approxfftAllIQs.append(copy.deepcopy(approxfftIQs))
		
	return approxfftAllIQs

def generateParallelSignal(AllSymbols, symbol1, symbol2):
	approxfftIQs1 = AllSymbols[symbol1]
	approxfftIQs2 = AllSymbols[symbol2]
	approxfftIQs = getSubsetandShift2(approxfftIQs1, approxfftIQs2, 48, -15, 14, 11)
	return approxfftIQs


def generateMacPacket(load, seq_nr):
	d_msg = []
	d_msg.append(1)
	d_msg.append(4)
	d_msg.append(8)
	d_msg.append(8)
	d_msg.append((seq_nr & 0xFF) % 16)
	d_msg.append((seq_nr & 0xFF) / 16)
	d_msg.append(2)
	d_msg.append(2)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(15)
	d_msg.append(15)
	d_msg.append(15)
	d_msg.append(15)
	d_msg.append(1)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(15)
	d_msg.append(3)
	d_msg.append(6)
	d_msg.append(0)
	L = len(load)
	for i in range(L):
		d_msg.append(load[i])
	
	temp = [0 for i in range(len(d_msg))]
	for i in range(len(d_msg) / 2):
		temp[2*i] = d_msg[2*i+1]
		temp[2*i+1] = d_msg[2*i]
	data = ''
	for i in range(len(temp)):
		data += '%x'%temp[i]
	crc = 0
	target = bytearray.fromhex(data)
	crc = CRC16Kermit().calculate(target)
	d_msg.append((crc >> 8) % 16)
	d_msg.append((crc >> 8) / 16)
	d_msg.append((crc & 0xFF) % 16)
	d_msg.append((crc & 0xFF) / 16)
	return d_msg


def generateMacPacket1(load, seq_nr):
	d_msg = []
	d_msg.append(1)
	d_msg.append(4)
	d_msg.append(8)
	d_msg.append(8)
	d_msg.append((seq_nr & 0xFF) % 16)
	d_msg.append((seq_nr & 0xFF) / 16)
	d_msg.append(2)
	d_msg.append(2)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(1)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(0)
	d_msg.append(15)
	d_msg.append(3)
	d_msg.append(6)
	d_msg.append(0)
	L = len(load)
	for i in range(L):
		d_msg.append(load[i])
	
	temp = [0 for i in range(len(d_msg))]
	for i in range(len(d_msg) / 2):
		temp[2*i] = d_msg[2*i+1]
		temp[2*i+1] = d_msg[2*i]
	data = ''
	for i in range(len(temp)):
		data += '%x'%temp[i]
	crc = 0
	target = bytearray.fromhex(data)
	crc = CRC16Kermit().calculate(target)
	d_msg.append((crc >> 8) % 16)
	d_msg.append((crc >> 8) / 16)
	d_msg.append((crc & 0xFF) % 16)
	d_msg.append((crc & 0xFF) / 16)
	return d_msg


def generatePhyPacket(macpacket):
	d_msg = []
	MacLen = len(macpacket)
	for i in range(4):
		d_msg.append(0)
	d_msg.append(7)
	d_msg.append(10)
	d_msg.append((MacLen/2) % 16)
	d_msg.append((MacLen/2) / 16)
	for i in range(MacLen):
		d_msg.append(macpacket[i])

	return d_msg


def generateRandomPayload(len):
	load = []
	for i in range(len):
		content = int(random.uniform(0,15))
		load.append(content)

	return load

def generateFixedPayload(len, symbol):
	load = []
	load.append((symbol & 0xFF) % 16)
	load.append((symbol & 0xFF) / 16)
	for i in range(len-2):
		content = 5
		load.append(content)
	return load



AllSymbols = generateAllSymbols()

LoadLen = 2

for i in range(100):
	filename = "./data/WEBeeQAMs"+str(i)+".txt"
	qamfile = open(filename, "w")
 	payload = generateFixedPayload(LoadLen, i)
 	macload = generateMacPacket(payload, i)
 	phyload = generatePhyPacket(macload)
 	strhex = ''
 	for j in range(len(phyload)):
 		strhex = strhex + getHex1(phyload[j])
 	print strhex

 	payload2 = generateFixedPayload(LoadLen, i)
 	macload2 = generateMacPacket1(payload2, i)
 	phyload2 = generatePhyPacket(macload2)
 	N = len(phyload)
 	
	for sym in range(N):
		approxfftIQs = generateParallelSignal(AllSymbols, phyload[sym], phyload2[sym])
		for i in range(len(approxfftIQs)):
			real = approxfftIQs[i][0]
			img = approxfftIQs[i][1]
			qamfile.write("%.5f, %.5f" % (float(real), float(img)))
			qamfile.write("\n")

		qamfile.flush()

	qamfile.close()



