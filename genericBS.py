import sys
import time
import inputPuzzle
import DomainConstraints

#importing required variables
rows = inputPuzzle.rows
columns = inputPuzzle.columns
HorizontalMat = inputPuzzle.HorizontalMat
VertMat = inputPuzzle.VertMat

#importing required variables
constraint_matrix = DomainConstraints.constraint_matrix
varDict = DomainConstraints.varDict
constraintVar_dict = DomainConstraints.constraintVar_dict
constraintVar_num = DomainConstraints.constraintVar_num


# ARC CONSISTENCY

# Remove_Inconsistent functions removes values from domain of X,Y which doesnt follow constraint between them 
def Remove_Inconsistent(X, Y) :
    removed = False

    # variable X can be any of the two types of variables we have : inputted unassigned variable or newly added constraint variable
    # If X is inputted unassigned variable
    if X in varDict.keys() :

        inTuple = constraintVar_dict[Y]['neighbours']
        Index = inTuple.index(X)
        for x in varDict[X]['domain'] :
            count = 0 
            for a in constraintVar_dict[Y]['domain'] :
                y = a[Index]

                if ( y == x ) :
                    count = count + 1
                    break 

            if ( count == 0 ) :
                varDict[X]['domain'].remove(x)
                removed = True
        return removed
    else :
        inTuple = constraintVar_dict[X]['neighbours']
        Index = inTuple.index(Y)
        for a in constraintVar_dict[X]['domain'] :
            x = a[Index]

            if x not in varDict[Y]['domain'] :
                constraintVar_dict[X]['domain'].remove(a)
                removed = True
        return removed


# AC3 algorithm implementation
def AC3(arcList) :
    while ( len(arcList) != 0 ) :       # when no element is present in queue , AC3 is completed
        Tuple = arcList.pop()           # Arclist will contain variables X,Y which are neighbours of each other
        
        # If domain of variables gets changed then we have to consider their neighbours again for consistency  
        if Remove_Inconsistent( Tuple[0] , Tuple[1] ) :
            if Tuple[0] in varDict.keys() :
                for i in range(constraintVar_num) :
                    j = varDict[Tuple[0]]['unassignedVariable_num']

                    # Checking neighbours from constraint matrix where the value is 1 which means there is a constraint between both of those variables
                    if ( constraint_matrix[i][j-1] == 1 ) :     
                        arcList.append(( i+1 , Tuple[0]))
            else :
                for var in constraintVar_dict[Tuple[0]]['neighbours'] :         # directly checking its neighbours from the dictionary of newly added variables (constraintVar_dict)
                    arcList.append((var , Tuple[0]))


# We will perform recursing backtracking by checking consistency before assigning a value to variable at that point of time
# If we find inconsistency further we will  remove that assignment

# Backtracking Search 
numberOfBackTracks = [0]            # Keeping the count of no of backtracks
assignmentList = []                 # AssignmentList is a list of dictionary where dictionaries are assignments in each step
dict1 = {}                          # keys are inputted unassigned variables
for elem in varDict.keys():
    dict1[elem] = 0                 # Initially no variable is assigned so giving the value for all them as 0
assignmentList.append(dict1)



def Recursive_Backtracking() :

    numberOfBackTracks[0] = numberOfBackTracks[0] + 1       # count of backtracks

    if (len(assignmentList) == constraintVar_num + 1):      # Assignment is complete for every variable
        return True

    var = len(assignmentList)       # var to be assigned (constraintvar i.e. newly added variables)

    for value in constraintVar_dict[var]['domain']:         # Assigning value to variable 'var'
        assignment = assignmentList[len(assignmentList) - 1].copy()    # current assignment is last dict of assignmentList
        
        # Checking whether assigning value to var gets any conflicts with the previous assignment of variables
        flag = 0
        for i in range(len(value)) :
            if((value[i] == assignment[constraintVar_dict[var]['neighbours'][i]]) or (assignment[constraintVar_dict[var]['neighbours'][i]] == 0)):
                flag = flag +1

        # If there is no conflict with any value of assigning variables by taking this tuple we will consider this assignment as valid assignment
        # Otherwise igonre this tuple 
        if (flag == len(value)):        # consistency
            for j in range(len(value)) :
                assignment[constraintVar_dict[var]['neighbours'][j]] = value[j]        
            assignmentList.append(assignment)       # Adding this assignment as valid assignment 

            result = Recursive_Backtracking()       # Continuing backtracking search further
            if (result != False) :
                return result
            
            assignmentList.pop()    # If result is false then our previous assignment is not valid . So popping off from assignmentList

    # If there is no tuple for this var satisying constraints then there is wrong with the previous assignment
    return False


def printMetrics():
    print(assignmentList[len(assignmentList) - 1])      # Final values of unasigned variables
    print("\nNumber Of Backtracks " , numberOfBackTracks[0])


# Calculating time for arc consistency and regular back tracking search
start = time.time()    

arcList = [] 
# Creating arcLists
for i in range( 1 , constraintVar_num + 1 ) :
    for j in constraintVar_dict[i]['neighbours'] :
        arcList.append( (j , i) )
        arcList.append( (i , j) )


# Calling AC3 function 
AC3(arcList)


# Calling backtracking search
Recursive_Backtracking()

end = time.time()           # ending time 
print( "time" , end - start)        # printing time 
print("\n")

printMetrics()

# Outputting to a text file

outputFile = open(sys.argv[2], 'w')

    #writing first three lines same as input text file 
outputFile = open(sys.argv[2], 'w')

    #writing first three lines same as input text file 
RowsLine = "rows=" + str(rows) + "\n"
ColumnsLine = "columns=" + str(columns) + "\n"

outputFile.write(RowsLine)
outputFile.write(ColumnsLine)
outputFile.write("Horizontal\n")

    # Changing values of unassigned variables in horizontal and vertical matrices from assignment 
for var in varDict.keys():
    HorizontalMat[var[0]][var[1]] = assignmentList[-1][var]
    VertMat[var[0]][var[1]] = assignmentList[-1][var]

    # wrting horizontal matrix
for row in range(rows):
    for col in range(columns):
        if(col == 0):
            outputFile.write(str(HorizontalMat[row][col]))
        else:
            outputFile.write(","+ str(HorizontalMat[row][col]))
    outputFile.write("\n")

    # writing vertical matrix
outputFile.write("Vertical\n")
for row in range(rows):
    for col in range(columns):
        if(col == 0):
            outputFile.write(str(VertMat[row][col]))
        else:
            outputFile.write(","+ str(VertMat[row][col]))
    outputFile.write("\n")


