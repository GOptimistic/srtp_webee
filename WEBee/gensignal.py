import numpy as np
import copy
import struct


WITHCP = 80
#WITHCP = 64
WITHOUTCP = 64
SAMPLERATE = WITHCP / 4

ALIGNMENT = [1,0,1,0] #1 means RIGHT and 0 means LEFT

def complexmultiply(a,b):
	c = [0, 0]
	c[0] = a[0]*b[0] - a[1]*b[1] 
	c[1] = a[1]*b[0] + a[0]*b[1]
	return c

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


def complexmultiply(a,b):
	c = [0, 0]
	c[0] = a[0]*b[0] - a[1]*b[1] 
	c[1] = a[1]*b[0] + a[0]*b[1]
	return c

def generateQAM(N, side):
	qam = [[0,0] for i in range(N)]
	m = int(np.sqrt(N))
	interval = float(side * 2) / (m - 1)
	xstart = -1 * side
	ystart = -1 * side
	for i in range(m):
		for j in range(m):
			x = xstart + i * interval
			y = ystart + j * interval
			qam[i*m + j][0] = float("%.5f" %x)
			qam[i*m + j][1] = float("%.5f" %y)
	return qam

def Edis(point1,point2):
	N = len(point1)
	temp = 0
	for i in range(N):
		temp = temp + (point1[i] - point2[i])**2
	dis = np.sqrt(temp)
	return dis

def approxQAM(qam, IQs):
	N = len(IQs)
	M = len(qam)
	approxIQs = []
	for i in range(N):
		x1 = IQs[i][0]
		y1 = IQs[i][1]
		if x1 == 0 and y1 == 0:
			approxIQs.append([0,0])
		else:
			mindis = 1000
			minindex = -1
			for j in range(M):
				x2 = qam[j][0]
				y2 = qam[j][1]
				dis = Edis([x1,y1],[x2,y2])
				if dis < mindis:
					mindis = dis
					minindex = j
			approxIQs.append(qam[minindex])
	return approxIQs

def generateIQ(symbol, ratio):
	chips = [[] for i in range(16)]
	chips[0] = [1,1,0,1,  1,0,0,1,  1,1,0,0, 0,0,1,1,  0,1,0,1, 0,0,1,0, 0,0,1,0, 1,1,1,0]
	chips[1] = [1,1,1,0,  1,1,0,1,  1,0,0,1,  1,1,0,0, 0,0,1,1,  0,1,0,1, 0,0,1,0, 0,0,1,0]
	chips[2] = [0,0,1,0, 1,1,1,0,  1,1,0,1,  1,0,0,1,  1,1,0,0, 0,0,1,1,  0,1,0,1, 0,0,1,0]
	chips[3] = [0,0,1,0, 0,0,1,0, 1,1,1,0,  1,1,0,1,  1,0,0,1,  1,1,0,0, 0,0,1,1,  0,1,0,1]
	chips[4] = [0,1,0,1, 0,0,1,0, 0,0,1,0, 1,1,1,0,  1,1,0,1,  1,0,0,1,  1,1,0,0, 0,0,1,1]
	chips[5] = [0,0,1,1,  0,1,0,1, 0,0,1,0, 0,0,1,0, 1,1,1,0,  1,1,0,1,  1,0,0,1,  1,1,0,0] 
	chips[6] = [1,1,0,0, 0,0,1,1,  0,1,0,1, 0,0,1,0, 0,0,1,0, 1,1,1,0,  1,1,0,1,  1,0,0,1]
	chips[7] = [1,0,0,1,  1,1,0,0, 0,0,1,1,  0,1,0,1,  0,0,1,0, 0,0,1,0, 1,1,1,0, 1,1,0,1]
	chips[8] = [1,0,0,0,  1,1,0,0,  1,0,0,1, 0,1,1,0,  0,0,0,0, 0,1,1,1, 0,0,1,1, 1,0,1,1]
	chips[9] = [1,0,1,1, 1,0,0,0,  1,1,0,0,  1,0,0,1, 0,1,1,0,  0,0,0,0, 0,1,1,1, 0,0,1,1]
	chips[10] = [0,0,1,1, 1,0,1,1, 1,0,0,0,  1,1,0,0,  1,0,0,1, 0,1,1,0,  0,0,0,0, 0,1,1,1]
	chips[11] = [0,1,1,1, 0,0,1,1, 1,0,1,1, 1,0,0,0,  1,1,0,0,  1,0,0,1, 0,1,1,0,  0,0,0,0]
	chips[12] = [0,0,0,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,0,0,0,  1,1,0,0,  1,0,0,1, 0,1,1,0]
	chips[13] = [0,1,1,0,  0,0,0,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,0,0,0,  1,1,0,0,  1,0,0,1]
	chips[14] = [1,0,0,1, 0,1,1,0,  0,0,0,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,0,0,0,  1,1,0,0]
	chips[15] = [1,1,0,0, 1,0,0,1, 0,1,1,0,  0,0,0,0, 0,1,1,1, 0,0,1,1, 1,0,1,1, 1,0,0,0]
	chip = chips[symbol]
	chip_len = len(chip)
	IQs = []

	Ichips = []
	Qchips = []
	for i in range(chip_len):
		if i % 2 == 0:
			Ichips.append(chip[i])
		else:
			Qchips.append(chip[i])

	Interval = []
	for i in range(chip_len + 1):
		Interval.append(i*np.pi / 2)
	SampleRate = SAMPLERATE
	X = []
	for i in range(16):
		for j in range(SampleRate):
			X.append(i*np.pi + j*np.pi / SampleRate)
	
	for i in range(len(X)):
		x = X[i]
		index = 0
		while x > Interval[index]:
			index = index + 1 
		index = index - 1
		Iindex = index / 2
		Qindex = (index - 1) / 2
		if Qindex < 0:
			Qindex = 0
		if Ichips[Iindex] == 1:
			Ibit = 1
		else:
			Ibit = -1
		if Qchips[Qindex] == 1:
			Qbit = 1
		else:
			Qbit = -1

		Iphase = Ibit*np.sin(x - Iindex * np.pi)
		Qphase = Qbit*np.sin(x - np.pi / 2 - Qindex * np.pi)
		
		if abs(Iphase) < 0.01:
			Iphase = 0
		if abs(Qphase) < 0.01:
			Qphase = 0	

		Iphase = Iphase * ratio
		Qphase = Qphase * ratio		
		IQs.append([Iphase,Qphase])

	return IQs


def shiftCons(approxfftIQs, xdelta, ydelta):
	length = len(approxfftIQs)
	newIQs = [[0, 0] for i in range(length)]
	for i in range(length):
		newIQs[i][0] = approxfftIQs[i][0] + xdelta
		newIQs[i][1] = approxfftIQs[i][1] + ydelta

	return newIQs

def cyclicprefixer(IQs):
    M = WITHOUTCP
    N = WITHCP
    length = len(IQs)
    G = length / M
    afterIQs = []
    for g in range(G):
    	tempIQs = IQs[g*M:(g+1)*M]
    	for j in range(N-M):
            cpI = tempIQs[2*M - N + j][0]
            cpQ = tempIQs[2*M - N + j][1]
            afterIQs.append([cpI,cpQ])
        for j in range(M):
            afterIQs.append([tempIQs[j][0], tempIQs[j][1]])

    return afterIQs

def generateIQSignal(symbol, ratio, subc):
	WholeSignals = []
	WholeIQs = generateIQ(symbol, ratio)
	length = len(WholeIQs)
	groupsize = WITHCP
	groupbeforecp = WITHOUTCP
	delta = WITHCP - WITHOUTCP
	Groups = length / groupsize
	approxIY = []
	approxQY = []
	for g in range(Groups):
		complexIQs = []
		for i in range(delta, WITHCP):
			complexIQs.append(np.complex64(WholeIQs[g*groupsize + i][0] + WholeIQs[g*groupsize + i][1]*1j))
            
		complexIQs = np.array(complexIQs)
		tempsp = np.fft.fft(complexIQs)
		tempsp = np.fft.fftshift(tempsp)

		tempSignals = []
		for jj in range(len(tempsp)):
		 	tempSignals.append([tempsp[jj].real, tempsp[jj].imag])
		
		# for jj in range(len(tempsp)):
		# 	comangle = 1*2*jj*np.pi*delta*1.0/WITHOUTCP
		# 	offset = [np.cos(comangle), np.sin(comangle)]
		# 	tempSignals.append(complexmultiply([tempsp[jj].real, tempsp[jj].imag],offset))
		
		sp = []
		for jj in range(groupbeforecp):
			sp.append(np.complex64(tempSignals[jj][0]+tempSignals[jj][1]*1j))
        
		for i in range(len(sp)):
			if abs(i - len(sp)/2) <= subc:
				WholeSignals.append([sp[i].real,sp[i].imag])
			else:
				WholeSignals.append([0,0])
  
	return WholeSignals


def generateISignal(symbol, ratio, subc):
	WholeSignals = []
	WholeIQs = generateIQ(symbol, ratio)
	length = len(WholeIQs)
	groupsize = WITHCP
	groupbeforecp = WITHOUTCP
	delta = WITHCP - WITHOUTCP
	Groups = length / groupsize
	approxIY = []
	approxQY = []
	for g in range(Groups):
		complexIQs = []
		if ALIGNMENT[g] == 0:
			for i in range(0, WITHCP - delta):
				complexIQs.append(np.complex64(WholeIQs[g*groupsize + i][0]))
		if ALIGNMENT[g] == 1:
			for i in range(delta, WITHCP):
				complexIQs.append(np.complex64(WholeIQs[g*groupsize + i][0]))

		complexIQs = np.array(complexIQs)
		tempsp = np.fft.fft(complexIQs)
		tempsp = np.fft.fftshift(tempsp)

		tempSignals = []		
		if ALIGNMENT[g] == 0:
			for jj in range(len(tempsp)):
			 	comangle = 1*2*jj*np.pi*delta*1.0/WITHOUTCP
			 	offset = [np.cos(comangle), np.sin(comangle)]
			 	tempSignals.append(complexmultiply([tempsp[jj].real, tempsp[jj].imag], offset))

		if ALIGNMENT[g] == 1:
			for jj in range(len(tempsp)):
				tempSignals.append([tempsp[jj].real, tempsp[jj].imag])
				
		sp = []
		for jj in range(groupbeforecp):
			sp.append(np.complex64(tempSignals[jj][0]+tempSignals[jj][1]*1j))

		for i in range(len(sp)):
			if abs(i - len(sp)/2) <= subc:
				WholeSignals.append([sp[i].real,sp[i].imag])
			else:
				WholeSignals.append([0,0])
	return WholeSignals


def generateQSignal(symbol, ratio, subc):
	WholeSignals = []
	WholeIQs = generateIQ(symbol, ratio)
	length = len(WholeIQs)
	groupsize = WITHCP
	groupbeforecp = WITHOUTCP
	delta = WITHCP - WITHOUTCP
	Groups = length / groupsize
	delta1 = WITHCP / 8

	LeftWholeIQs = copy.deepcopy(WholeIQs)
	RightWholeIQs = copy.deepcopy(WholeIQs)

	LeftWholeIQs = cycleshift(RightWholeIQs, -1*delta1)
	RightWholeIQs = cycleshift(RightWholeIQs, delta1)
	
	#Left Shift
	if symbol == 5 or symbol == 2 or symbol == 4 or symbol == 6 or symbol == 12 or symbol == 13 or symbol == 14:
		for i in range(delta1):
	 		LeftWholeIQs[i][1] = -1 * LeftWholeIQs[i][1]

    #Right Shift
	if symbol == 5 or symbol == 2 or symbol == 4 or symbol == 6 or symbol == 12 or symbol == 13 or symbol == 14:
		for i in range(delta1):
	 		RightWholeIQs[length - delta1 + i][1] = -1 * RightWholeIQs[length - delta1 + i][1]

	approxIY = []
	approxQY = []
	for g in range(Groups):
		complexIQs = []
		if ALIGNMENT[g] == 0:
			for i in range(0, WITHCP - delta):
				complexIQs.append(np.complex64(LeftWholeIQs[g*groupsize + i][1]*1j))
		if ALIGNMENT[g] == 1:
			for i in range(delta, WITHCP):
				complexIQs.append(np.complex64(RightWholeIQs[g*groupsize + i][1]*1j))

		complexIQs = np.array(complexIQs)
		tempsp = np.fft.fft(complexIQs)
		tempsp = np.fft.fftshift(tempsp)

		tempSignals = []
		for jj in range(len(tempsp)):
			if ALIGNMENT[g] == 0:
				comangle = 1*2*jj*np.pi*delta1*1.0/WITHOUTCP
			if ALIGNMENT[g] == 1:
				comangle = -1*2*jj*np.pi*delta1*1.0/WITHOUTCP

			offset = [np.cos(comangle), np.sin(comangle)]
			temp = complexmultiply([tempsp[jj].real, tempsp[jj].imag],offset)

			if ALIGNMENT[g] == 0:
				comangle = 1*2*jj*np.pi*delta*1.0/WITHOUTCP
			if ALIGNMENT[g] == 1:
				comangle = 0
			offset = [np.cos(comangle), np.sin(comangle)]
			tempSignals.append(complexmultiply(temp,offset))

		sp = []
		for jj in range(groupbeforecp):
			sp.append(np.complex64(tempSignals[jj][0]+tempSignals[jj][1]*1j))

		for i in range(len(sp)):
			if abs(i - len(sp)/2) <= subc:
				WholeSignals.append([sp[i].real,sp[i].imag])
			else:
				WholeSignals.append([0,0])
	return WholeSignals


def generateIFFTSignal(approxfftIQs):
	length = len(approxfftIQs)
	newIQs = []
	complexfftIQs = []
	groupsize = WITHOUTCP
	Groups = length / groupsize
	for g in range(Groups):
		fftIQs = [[0, 0] for i in range(groupsize)]
		for i in range(groupsize):
			fftIQs[i][0] = approxfftIQs[g*groupsize + i][0]
			fftIQs[i][1] = approxfftIQs[g*groupsize + i][1]

		length = len(fftIQs)
		complexfftIQs = []
		for i in range(length):
			Isample = fftIQs[i][0]
			Qsample = fftIQs[i][1]
			complexfftIQs.append(np.complex64(Isample+Qsample*1j))

		#print complexfftIQs
		complexfftIQs = np.array(complexfftIQs)
		complexfftIQs = np.fft.fftshift(complexfftIQs)
		sp = np.fft.ifft(complexfftIQs)
		
		
		#spec = np.sqrt(sp.real*sp.real + sp.imag*sp.imag)
		for i in range(len(sp)):
 			newIQs.append([sp[i].real,sp[i].imag])

	return newIQs




def compensateCFO(IQs, deltaf, Fs):
	N = len(IQs)
	newIQs = [[0,0] for i in range(N)]
	for i in range(N):
		comangle = float(2*np.pi*deltaf*i) / Fs 
		offset = [np.cos(comangle), np.sin(comangle)]
		sample = [IQs[i][0], IQs[i][1]]
		com = complexmultiply(sample,offset)
		newIQs[i][0] = com[0]
		newIQs[i][1] = com[1]
	return newIQs

def generateMultipleSignal(count, chips, ratio):
	Groups = 5
	GroupSize = 48
	subc = 5
	starti = [0,13,25,38]
	channels = [-21,-7,7,21]
	WholeSignals = [[0,0] for i in range(Groups * GroupSize)]
	comdeltaf = [-0.4375,0.1875,0.8125,1.4375]
	#comdeltaf = [0,0,0,0]
	for cc in range(count):
		chip = chips[cc]
		#subchannels = channels[cc]
		WholeIQs = generateIQ(chip, ratio)
		deltaf = comdeltaf[cc]
		WholeIQs = compensateCFO(WholeIQs,deltaf,15)
		approxIY = []
		approxQY = []
		for g in range(Groups):
			IQs = [[0, 0] for i in range(GroupSize)]
			for i in range(GroupSize):
				IQs[i][0] = WholeIQs[g*GroupSize + i][0]
				IQs[i][1] = WholeIQs[g*GroupSize + i][1]

			length = len(IQs)
			complexIQs = []
			for i in range(length):
				Isample = IQs[i][0]
				Qsample = IQs[i][1]
				complexIQs.append(np.complex64(Isample+Qsample*1j))


			complexIQs = np.array(complexIQs)
			sp = np.fft.fft(complexIQs)
			#spec = np.sqrt(sp.real*sp.real + sp.imag*sp.imag)

			fftIQs = []
			for i in range(len(sp)):
 				fftIQs.append([sp[i].real,sp[i].imag])


			qam = generateQAM(64,1.0801)
			qam.append([0,0])

			approxfftIQs = approxQAM(qam, fftIQs)

			for i in range(subc):
				loc = starti[cc] + subc + i
				WholeSignals[g*GroupSize + loc][0] = approxfftIQs[i+1][0]
				WholeSignals[g*GroupSize + loc][1] = approxfftIQs[i+1][1]
			for i in range(subc):
				loc = starti[cc] + i
				WholeSignals[g*GroupSize + loc][0] = approxfftIQs[GroupSize - subc + i - 1][0]
				WholeSignals[g*GroupSize + loc][1] = approxfftIQs[GroupSize - subc + i - 1][1]

	return WholeSignals
