import sys

# Opening input kauro puzzle file in read mode
inputFile = open(sys.argv[1], 'r')
rows = 0
columns = 0

# Two seperate matrices for horizontal and vertical parts
HorizontalMat = []
VertMat = []
i = 0
j = 0 

# Reading data from input file
for lineNo, line in enumerate(inputFile):
    if (lineNo == 0):
        rowsV = line.strip().split('=')
        rows = int(rowsV[1])                # rows will give no of rows in kakuro puzzle
    elif(lineNo == 1):
        cols = line.strip().split('=')
        columns = int(cols[1])              # columns will give no of columns in kakuro puzzle
    else:
        if(lineNo == 2 or lineNo == (3+rows)):      # lines having strings as horizontal and vertical
            continue
        else:
            cell = line.strip().split(',')
            if (cell == ['']):              #EOF
                break

            inputcol = []
            for num in cell:
                if(num == '#'):
                    inputcol.append('#')
                else:
                    inputcol.append(int(num))       # if it is a number then we have to convert string "num" to num
                j = j+1
            if (lineNo < (3 + rows)):
                HorizontalMat.append(inputcol)         # adding row to matrix
            else:
                VertMat.append(inputcol)
