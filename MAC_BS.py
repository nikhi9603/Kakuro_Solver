import sys
import time
import copy
import inputPuzzle
import DomainConstraints


#importing required variables
rows = inputPuzzle.rows
columns = inputPuzzle.columns
HorizontalMat = inputPuzzle.HorizontalMat
VertMat = inputPuzzle.VertMat

constraint_matrix = DomainConstraints.constraint_matrix
varDict = DomainConstraints.varDict
constraintVar_dict = DomainConstraints.constraintVar_dict
constraintVar_num = DomainConstraints.constraintVar_num



# Arc List
def Remove_Inconsistent(X, Y, var_Dict, constraintVar_Dict):
    removed = False

    if X in var_Dict.keys():

        inTuple = constraintVar_dict[Y]['neighbours']
        Index = inTuple.index(X)
        for x in var_Dict[X]:
            count = 0
            for a in constraintVar_Dict[Y]:
                y = a[Index]

                if (y == x):
                    count = count + 1
                    break

            if (count == 0):
                var_Dict[X].remove(x)
                removed = True
        return removed
    else:
        inTuple = constraintVar_dict[X]['neighbours']
        Index = inTuple.index(Y)
        for a in constraintVar_Dict[X]:
            x = a[Index]

            if x not in var_Dict[Y]:
                constraintVar_Dict[X].remove(a)
                removed = True
        return removed


def AC3(ArcList, var_Dict, constraintVar_Dict):
    # Arc consistency
    while (len(ArcList) != 0):
        Tuple = ArcList.pop()

        if Remove_Inconsistent(Tuple[0], Tuple[1], var_Dict, constraintVar_Dict):
            if Tuple[0] in var_Dict.keys():
                for i in range(constraintVar_num):
                    j = varDict[Tuple[0]]['unassignedVariable_num']
                    if (constraint_matrix[i][j - 1] == 1):
                        ArcList.append((i + 1, Tuple[0]))
            else:
                for var in constraintVar_dict[Tuple[0]]['neighbours']:
                    ArcList.append((var, Tuple[0]))



AC3arcList = []    

# Creating arcLists
for i in range( 1 , constraintVar_num + 1 ) :
    for j in constraintVar_dict[i]['neighbours'] :
        AC3arcList.append( (i , j) )
        AC3arcList.append( (j , i) )


# Backtracking search
assignmentList = []
list1 = []
dict1 = {}
dict2 = {}
for elem in varDict.keys():
    dict1[elem] = varDict[elem]['domain'].copy()
    varDict[elem]['neighbours'] = []
    for i in range(constraintVar_num):
        j = varDict[elem]['unassignedVariable_num']
        if (constraint_matrix[i][j - 1] == 1):
            varDict[elem]['neighbours'].append(i + 1)

for elem in constraintVar_dict.keys():
    dict2[elem] = constraintVar_dict[elem]['domain'].copy()

list1.append(dict1)
list1.append(dict2)
assignmentList = [list1]


AC3(AC3arcList , assignmentList[0][0] , assignmentList[0][1])
numberOfBacktracks = [0]

#We will assign a tuple for a constraint variable, then we will apply arc consistency for this node(var)
#if while applying, any of the variable's domain gets reduced to null set, then we will restore our previous assignment,
#from assignment list, which contains all consistent assignments only
#this backtracking will ultimately assign correct values to all variables
def MAC_BS():
    numberOfBacktracks[0] = numberOfBacktracks[0] + 1
    if (len(assignmentList) == constraintVar_num + 1):
        return True

    var = len(assignmentList)

    #making new assignment
    for value in assignmentList[len(assignmentList) - 1][1][var]:
        copiedList = copy.deepcopy(assignmentList)
        assignment = copiedList[len(copiedList) - 1]

        # reducing domain of var to value
        assignment[1][var] = [value]
        # creating arcList
        arcList = []

        #modifying Xis according to constraint variable assignment
        for x in constraintVar_dict[var]['neighbours']:
            assignment[0][x] = [value[constraintVar_dict[var]['neighbours'].index(x)]]
            for u in varDict[x]['neighbours']:
                if u != var:
                    arcList.append((u, x))

        #checking inconsistency of assigned variables with previous assignment
        flag = 0
        for x in constraintVar_dict[var]['neighbours']:

            if assignment[0][x][0] in assignmentList[len(assignmentList) - 1][0][x]:
                flag = flag + 1

        if (flag == len(constraintVar_dict[var]['neighbours'])):

            AC3(arcList, assignment[0], assignment[1])

            # Checking for inconsistencies ,whether while assigning domain of any variable gets reduced to zero or not
            count = 0
            for a in assignment[0]:
                if (len(assignment[0][a]) == 0):
                    count = count + 1

            for b in assignment[1]:
                if (len(assignment[1][b]) == 0):
                    count = count + 1

            if (count == 0):  # valid assignment
                assignmentList.append(assignment)

                result = MAC_BS()

                if (result != False):
                    return result

                assignmentList.pop()

    return False

start = time.time()
MAC_BS()
end = time.time()
print(assignmentList[len(assignmentList) - 1][0])
print("\nnumberOfbacktracks", numberOfBacktracks[0])
print("time", end - start)
# Outputting to a text file
outputFile = open(sys.argv[2], 'w')

# writing first three lines same as input text file
RowsLine = "rows=" + str(rows) + "\n"
ColumnsLine = "columns=" + str(columns) + "\n"

outputFile.write(RowsLine)
outputFile.write(ColumnsLine)
outputFile.write("Horizontal\n")

# Changing values of unassigned variables in horizontal and vertical matrices from assignment
for var in varDict.keys():
    HorizontalMat[var[0]][var[1]] = assignmentList[-1][0][var][0]
    VertMat[var[0]][var[1]] = assignmentList[-1][0][var][0]


# wrting horizontal matrix
for row in range(rows):
    for col in range(columns):
        if (col == 0):
            outputFile.write(str(HorizontalMat[row][col]))
        else:
            outputFile.write("," + str(HorizontalMat[row][col]))
    outputFile.write("\n")

# writing vertical matrix
outputFile.write("Vertical\n")
for row in range(rows):
    for col in range(columns):
        if (col == 0):
            outputFile.write(str(VertMat[row][col]))
        else:
            outputFile.write("," + str(VertMat[row][col]))
    outputFile.write("\n")