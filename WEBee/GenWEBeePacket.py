import copy

def getBin(x):
	t={0:'0000',1:'0001',2:'0010',3:'0011',4:'0100',5:'0101',6:'0110',7:'0111',8:'1000',9:'1001',10:'1010',11:'1011',12:'1100',13:'1101',14:'1110',15:'1111'}
	return t[x]

def getSym(x):
	t={'0000':0,'0001':1,'0010':2,'0011':3,'0100':4,'0101':5,'0110':6,'0111':7,'1000':8,'1001':9,'1010':10,'1011':11,'1100':12,'1101':13,'1110':14,'1111':15}
	return t[x]

def getSymHex(x):
	t={'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}
	return t[x]

def getHex(x):
	t={0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}
	return t[x]

TotalBits = 216 * 4 * 48

wifiFiles = open("./webeepayload.txt", "w")
sourceFile = open("./data/WEBeeBits0.txt", "r")
SourceBits = []
for line in sourceFile.readlines():
	strline = line.split(',')
	for i in range(len(strline)):
		SourceBits.append(int(strline[i]))
sourceFile.close()

KK = len(SourceBits) / 8

#pad some bits
PADBITS = 8*27
for i in range(PADBITS):
	SourceBits.insert(0, 0)
M = len(SourceBits)

out_bits = [0 for i in range(M)]
state = [1,0,0,1,0,0,0]

for i in range(7, M):
	feedback = state[3] ^ state[6]
	out_bits[i] = SourceBits[i] ^ feedback
	state[1:7] = state[0:6]
	state[0] = feedback
	

ST = M / 8
wifiFiles.write("%d" %(ST-2))
wifiFiles.write("\r\n")

for qamkk in range(100):
	sourceFile = open("./data/WEBeeBits"+str(qamkk)+".txt", "r")
	SourceBits = []
	for line in sourceFile.readlines():
		strline = line.split(',')
		for i in range(len(strline)):
			SourceBits.append(int(strline[i]))
	sourceFile.close()

	KK = len(SourceBits) / 8

	#pad some bits
	PADBITS = 8*27
	for i in range(PADBITS):
		SourceBits.insert(0, 0)
	M = len(SourceBits)

	out_bits = [0 for i in range(M)]
	state = [1,0,0,1,0,0,0]

	for i in range(7, M):
		feedback = state[3] ^ state[6]
		out_bits[i] = SourceBits[i] ^ feedback
		state[1:7] = state[0:6]
		state[0] = feedback

	for i in range(2,ST):
		bits = [0 for j in range(8)]
		for j in range(8):
			bits[7-j] = out_bits[i*8 + j]
		strbit = ""
		for k in range(4):
			strbit =  strbit + str(bits[k])
		high = getSym(strbit)
		strbit = ""
		for k in range(4,8):
			strbit =  strbit + str(bits[k])
		low = getSym(strbit)
		strn = str(high * 16 + low)
		wifiFiles.write(strn+',')
	wifiFiles.write("\r\n")

wifiFiles.close()

