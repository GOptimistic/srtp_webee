import numpy as np
import copy
import random

def getBin(x):
	t={0:'0000',1:'0001',2:'0010',3:'0011',4:'0100',5:'0101',6:'0110',7:'0111',8:'1000',9:'1001',10:'1010',11:'1011',12:'1100',13:'1101',14:'1110',15:'1111'}
	return t[x]

def getSym(x):
	t={'0000':0,'0001':1,'0010':2,'0011':3,'0100':4,'0101':5,'0110':6,'0111':7,'1000':8,'1001':9,'1010':10,'1011':11,'1100':12,'1101':13,'1110':14,'1111':15}
	return t[x]

def getSym3(x):
	t={'000':0,'001':1,'010':2,'011':3,'100':4,'101':5,'110':6,'111':7}
	return t[x]

def getSymHex(x):
	t={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
	return t[x]

def getHex(x):
	t={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
	return t[x]


def bitxor(a,b):
	if a == b:
		return 0
	else:
		return 1

def XOR(bits):
	N = len(bits)
	resbit = 0
	for i in range(N):
		resbit = bitxor(resbit,bits[i])
	return resbit

def XOR2(bits1, bits2):
	N = len(bits1)
	temps = [0 for i in range(N)]
	for i in range(N):
		temps[i] = bits1[i]*bits2[i]

	return XOR(temps)

HAMN = 15
HAMK = 11
HAMC = HAMN - HAMK
checkMatrix = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1],[0,1,1,0],[0,1,0,1],[0,0,1,1],[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0],[1,1,1,1]]

# HAMN = 7
# HAMK = 4
# HAMC = HAMN - HAMK
# checkMatrix = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[0,1,1],[1,1,1]]


realcheckMatrix = [[0 for i in range(HAMN)] for j in range(HAMC)]
for j in range(HAMC):
	for i in range(HAMN):
		realcheckMatrix[j][i] = checkMatrix[i][j]

generatorMatrix = [[0 for i in range(HAMK)] for j in range(HAMN)]
generatorMatrix1 = [[0 for i in range(HAMN)] for j in range(HAMK)]
for i in range(HAMC):
	for j in range(HAMK):
		generatorMatrix1[j][i] = checkMatrix[HAMC+j][i]
for i in range(HAMK):
	generatorMatrix1[i][i+HAMC] = 1

for i in range(HAMN):
	for j in range(HAMK):
		generatorMatrix[i][j] = generatorMatrix1[j][i]


seed = 111
def interleaver(msg):
	M = len(msg)
	random.seed(seed)
	permtable = [0 for i in range(M)]
	intermsg = [0 for i in range(M)]
	resmsg = [0 for i in range(M)]
	index = 0
	permset = []
	while(index < M):
		ri = random.randint(0,M-1)
		if not ri in permset:
			permset.append(ri)
			permtable[index] = ri
			index = index + 1
	for i in range(M):
		intermsg[i] = msg[permtable[i]]

	resbits = [0 for i in range(M * 4)]
	bits = [[0 for i in range(4)] for j in range(M)]
	for i in range(M):
		binbits = getBin(intermsg[i])
		for j in range(4):
			bits[i][j] = int(binbits[j])
	for i in range(M):
		for j in range(4):
			resbits[j*M+i] = bits[i][j]

	for i in range(M):
		bitstr = ''
		for j in range(4):
			bitstr = bitstr + str(resbits[i*4+j])
		resmsg[i] = getSym(bitstr)

	return resmsg

def deinterleaver(msg):
	M = len(msg)
	bits = [0 for i in range(M * 4)]
	resbits = [[0 for i in range(4)] for j in range(M)]
	for i in range(M):
		binbits = getBin(msg[i])
		for j in range(4):
			bits[i*4+j] = int(binbits[j])
	for i in range(M):
		for j in range(4):
			resbits[i][j] = bits[j*M+i]

	intermsg = [0 for i in range(M)]
	for i in range(M):
		bitstr = ''
		for j in range(4):
			bitstr = bitstr + str(resbits[i][j])
		intermsg[i] = getSym(bitstr)

	random.seed(seed)
	reversepermtable = [0 for i in range(M)]
	resmsg = [0 for i in range(M)]
	index = 0
	permset = []
	while(index < M):
		ri = random.randint(0,M-1)
		if not ri in permset:
			permset.append(ri)
			reversepermtable[ri] = index
			index = index + 1
	for i in range(M):
		resmsg[i] = intermsg[reversepermtable[i]]
	return resmsg

def hammingcode(bits):
	M = len(bits)
	MG = M / HAMK
	resbits = [0 for i in range(MG*HAMN)]
	for i in range(MG):
		tempbits = [0 for j in range(HAMK)]
		for j in range(HAMK):
			tempbits[j] = bits[i*HAMK + j]
		for j in range(HAMN):
			resbit =  XOR2(generatorMatrix[j],tempbits)
			resbits[i*HAMN+j] = resbit
	return resbits

def encode(msg):
	ML =  len(msg)
	resbits = [0 for i in range(ML * 4)]
	bits = [[0 for i in range(4)] for j in range(ML)]
	for i in range(ML):
		binbits = getBin(msg[i])
		for j in range(4):
			bits[i][j] = int(binbits[j])
	for i in range(ML):
		for j in range(4):
			resbits[i*4+j] = bits[i][j]

	CodedBits = hammingcode(resbits)
	
	CL = len(CodedBits) / 4
	coded_msg = [0 for i in range(CL)]
	for i in range(CL):
		bitstr = ''
		for j in range(4):
			bitstr = bitstr + str(CodedBits[i*4+j])
		coded_msg[i] = getSym(bitstr)

	inter_msg = interleaver(coded_msg)
	print len(inter_msg)
	return inter_msg

def HammingDistance(sym1, sym2):
	M = len(sym1)
	bits1 = [0 for i in range(M*4)]
	bits2 = [0 for i in range(M*4)]
	for i in range(M):
		strbit1 = getBin(sym1[i])
		strbit2 = getBin(sym2[i])
		for j in range(4):
			bits1[i*4+j] = int(strbit1[j])
			bits2[i*4+j] = int(strbit2[j])
	distance = 0
	for i in range(M*4):
		distance = distance + bitxor(bits1[i], bits2[i])

	return distance

def findErrPos(pos, checkMatrix):
	CML = len(checkMatrix)
	for i in range(CML):
		strbit = ''
		for j in range(len(checkMatrix[i])):
			strbit = strbit + str(checkMatrix[i][j])
		#if pos == getSym3(strbit):
		if pos == getSym(strbit):
			return i

frameheader = [0,0,0,0,10,7]
threshold = 4

def decode(msg):
	ML = len(msg)
	pacdata = [0 for i in range(ML)]
	for i in range(ML):
		pacdata[i] = getSymHex(msg[i])
		if len(pacdata) < 6:
			return -1
	if HammingDistance(frameheader, pacdata[0:6]) <= threshold:
		paclen = (pacdata[6] * 16 + pacdata[7]) * 2
		realpacdata = pacdata[8:8+paclen]
		if len(realpacdata) < 6:
			return -1
		if HammingDistance(frameheader, realpacdata[0:6]) <= threshold:
			paclen = (realpacdata[6] * 16 + realpacdata[7]) * 2
			realpacdata = realpacdata[8:8+paclen]
	else:
		realpacdata = pacdata

	realL = len(realpacdata)
	if not realL == 18:
		return -1
	realpacdata[14] = realpacdata[15]
	realL = 15
	realpacdata = realpacdata[0:15]
	intermsg = deinterleaver(realpacdata)

	
	dibits = [0 for i in range(realL * 4)]
	for i in range(realL):
		binbits = getBin(intermsg[i])
		for j in range(4):
			dibits[i*4+j] = int(binbits[j])

	CM = int(float(realL * 4) / HAMN) 
	DecodedBits = []
	for i in range(CM):
		hammingbits = [0 for j in range(HAMN)]
		for j in range(HAMN):
			hammingbits[j] = dibits[i*HAMN+j]

		checkbits = [0 for k in range(HAMC)]
		for k in range(HAMC):
			checkbits[k] = XOR2(realcheckMatrix[k], hammingbits)

		strcheck = ''
		for k in range(HAMC):
			strcheck = strcheck + str(checkbits[k])
		#errpos = getSym3(strcheck)
		errpos = getSym(strcheck)
		errstr = strcheck
		if errpos > 0:
			realpos = findErrPos(errpos, checkMatrix)
			hammingbits[realpos] = 1 - hammingbits[realpos]
		for k in range(HAMC, HAMN):
			DecodedBits.append(hammingbits[k])

	SM = int(float(len(DecodedBits)) / 4)
	ressyms = [0 for i in range(SM)]
	for i in range(SM):
		strsym = ''
		for j in range(4):
			strsym = strsym + str(DecodedBits[i*4+j])
		ressyms[i] = getSym(strsym)

	return ressyms

