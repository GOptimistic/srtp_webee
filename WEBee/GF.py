#!/usr/bin/env python
from numpyExtend import getNonZeroInRow;
from numpyExtend import getNonZeroInColumn;
from numpyExtend import changeRow;
from numpyExtend import changeColumn;
from numpyExtend import getBrightMatrix;
from numpyExtend import setRow;
from numpyExtend import print_Matrix;

class GF:
	def __init__(self, gf):
		self.galoisField = gf;

	def add(self, a, b):
		if isinstance(a,int) and isinstance(b,int):
			return (a + b) % self.galoisField;
		
		if isinstance(a, list) and isinstance(b, list):
			r = [];
			for i in range(len(a)):
				r.append(self.add(a[i], b[i]));
			return r;

		raise NameError('Wrong Input');
	
	def matrix_rank(self, originalMatrix):
		matrix = getBrightMatrix(originalMatrix);
		column=0;
		zeroRows = [];
		# es gibt mehr spalten als Zeilen,
		# deswegen jede Spalte quer bis zum Zeilenende runter
		while column < matrix.shape[0]:
			rows = getNonZeroInColumn(matrix, column, column);
			# es muss mindestens ein eins geben, und zwar die auf dem quer Vektor
			if rows == []:
				columns = getNonZeroInRow(matrix, column, column);
				# wenn es keine weitere eins in der Zeile gibt, ist der Zeilenvektor ein Nullvektor
				if columns == []:
					zeroRows.append(column);
					column+=1;
					continue;

				changeColumn(matrix, column, columns.pop());
				
				continue;

			if rows[0] != column:
				matrix = changeRow(matrix, column, rows[0]);

			rows.pop(0);

			#alle weiteren werden aufsummiert
			for row in rows:
				sumRow = self.add(matrix[column].tolist()[0], matrix[row].tolist()[0]);
				matrix = setRow(matrix, row, sumRow);
			
			column+=1;

		return column - len(zeroRows);
