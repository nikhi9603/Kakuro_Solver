import itertools
import inputPuzzle

#readng the input (kakuro puzzle) and storing it in HorizontalMat and VerticalMat
rows = inputPuzzle.rows
columns = inputPuzzle.columns
HorizontalMat = inputPuzzle.HorizontalMat
VertMat = inputPuzzle.VertMat


# varDict is a dictionary which have information about unassigned variables of input kakuro puzzle
# keys are (i,j) where X(i,j) = 0   i.e. blocks which are to be filled
 

varDict = {}
unassignedVariable_num = 0  

# constraintVar_dict is a dictionary which have information about variables which are newly added to convert n-ary constraint to binary constraints
# keys are new variable names which are nothing constraint numbers
constraintVar_dict = {}
constraintVar_num = 0 

# Identifying variables which are unassigned ( which are filled and given as 0 in matrices )
# domain of these variables is initialised to 0
for x in range(rows) :
    for y in range(columns) :
        if ( ( HorizontalMat[x][y] == 0 ) or ( VertMat[x][y] == 0 ) ) :
            unassignedVariable_num = unassignedVariable_num + 1
            varDict[(x,y)] = { "unassignedVariable_num" : unassignedVariable_num , "domain" : [ 1, 2, 3, 4, 5, 6, 7, 8, 9 ] }

# Identifying row and column constraints 
# And adding newVariables to convert n-ary constraint to binary constraint
for i in range(rows) :
    for j in range(columns) :

        # row constraint
        if ( HorizontalMat[i][j] != 0 and HorizontalMat[i][j] != "#" ) :
            constraintVar_num = constraintVar_num + 1 
            constraintVar_dict[ constraintVar_num ] = { "sum" : HorizontalMat[i][j] , "neighbours" : [] }

            # Finidng variables invloved in this constraint
            # next elements of that row which are 0 comes under this constraint
            x = i
            y = j + 1 
            while ( y < columns and HorizontalMat[x][y] == 0 ):
                constraintVar_dict[constraintVar_num]['neighbours'].append((x,y))
                y = y + 1
            
            # Adding domain to newly added variable
            # Domain is the permutations of variables involved in this constraint following the sum constraint
            possiblePermutations = list( itertools.permutations( range(1,10) , len(constraintVar_dict[constraintVar_num]['neighbours']) ))
            domain = []

            # Finding permutations out of possible permutations which follow the sum constraint
            for x in range(len(possiblePermutations)) :
                sum = 0
                for y in range(len(constraintVar_dict[constraintVar_num]['neighbours'])) :
                    sum = sum + possiblePermutations[x][y]

                if ( constraintVar_dict[constraintVar_num]['sum'] == sum ) :
                    domain.append(possiblePermutations[x])

            constraintVar_dict[constraintVar_num]["domain"] = domain
            
        # column constraint
        if ( VertMat[i][j] != 0 and VertMat[i][j] != "#" ) :
            constraintVar_num = constraintVar_num + 1 
            constraintVar_dict[ constraintVar_num ] = { "sum" : VertMat[i][j] , "neighbours" : [] }

            # Finidng variables invloved in this constraint
            # next elements of that column which are 0 comes under this constraint
            x = i + 1
            y = j 
            while ( x < rows and VertMat[x][y] == 0 ):
                constraintVar_dict[constraintVar_num]['neighbours'].append((x,y))
                x = x + 1

            domain = list( itertools.permutations( range(1,10) , len(constraintVar_dict[constraintVar_num]['neighbours']) ))
            constraintVar_dict[constraintVar_num]["domain"] = domain

            # Adding domain to newly added variable
            possiblePermutations = list( itertools.permutations( range(1,10) , len(constraintVar_dict[constraintVar_num]['neighbours']) ))
            domain = []

            # Finding permutations out of possible permutations which follow the sum constraint
            for x in range(len(possiblePermutations)) :
                
                sum = 0
                for y in range(len(constraintVar_dict[constraintVar_num]['neighbours'])) :
                    sum = sum + possiblePermutations[x][y]

                if ( constraintVar_dict[constraintVar_num]['sum'] == sum ) :
                    domain.append(possiblePermutations[x])

            constraintVar_dict[constraintVar_num]["domain"] = domain


# Creating constraint matrix
constraint_matrix = []

for x in range( constraintVar_num ) :       # Initialising full matrix as null matrix
    rowOfCM = []
    for i in range( 1 , unassignedVariable_num + 1 ) :
        rowOfCM.append(0)
    constraint_matrix.append(rowOfCM)

# changing values of matrix to 1 if that particular constraint and var are interconnected
for x in range( 1 , constraintVar_num + 1 ) :
    for var in varDict.keys() :
        if var in constraintVar_dict[x]['neighbours'] :
            constraint_matrix[x - 1][ varDict[var]['unassignedVariable_num'] - 1 ] = 1 
