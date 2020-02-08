import numpy;

# tauscht zwei Zeilen
def changeRow(matrix, r1, r2):
	if r1 == r2:
		return matrix;
	tmp = matrix[r1].copy();
	matrix[r1] = matrix[r2];
	matrix[r2] = tmp;

	return matrix;

# tauscht zwei Spalten
def changeColumn(matrix, c1, c2):
	if c1 == c2: 
		return matrix;
	for i in range(matrix.shape[0]):
		tmp = matrix[i, c1];
		matrix[i, c1] = matrix[i, c2];
		matrix[i, c2] = tmp;

	return matrix;

# geben eine gegebenfalls transponierte Matrix zurueck,
# solange es mehr Spalten als Zeilen gibt.
def getBrightMatrix(matrix):
	m = matrix.copy();
	return numpy.transpose(m) if matrix.shape[0] > matrix.shape[1] else m;
	
# Gibt die Zeilen zurueck, bei den angegeben Spalte nicht 0 sind
def getNonZeroInColumn(matrix, column, start = 0):
	m, n = matrix.shape;
	return [j for j in range(start, m) if matrix[j, column] != 0];


# Gibt die Spalten zurueck, bei den angegeben Zeile nicht 0 sind
def getNonZeroInRow(matrix, row, start = 0):
	m, n = matrix.shape;
	return [i for i in range(start, n) if matrix[row, i] != 0];

#setzt Zeilenvektor in bestimmte Zeile
def setRow(matrix, row , rowVector):
	for i in range(len(rowVector)):
		matrix[row, i] = rowVector[i];

	return matrix;


def print_Matrix(matrix):
	for i in range(matrix.shape[0]):
		line ="";
		for j in range(matrix.shape[1]):
			line += str(matrix[i, j]);
		print line;
