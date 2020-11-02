# Compiler Design Coursework.

import sys
from datetime import datetime
from graphviz import Digraph

# Opens the file.
rawInputFile = sys.argv[1]
with open(rawInputFile, "r") as inputFile:

    # Reads in each line.
    for line in inputFile:
        # Splits the individual line elements into an array.
        lineArray = line.split()
        if lineArray[0] == 'variables:':
            variables = lineArray[1:]
        elif lineArray[0] == 'constants:':
            constants = lineArray[1:]
        elif lineArray[0] == 'predicates:':
            predicates = []
            predicatesSize = {}

            # Stores the predicate as a dictionary. The key is the predicate name and value
            for item in lineArray[1:]:
                # Find where the [] are
                for i, j in enumerate(item):
                    if j == '[':
                        leftBracket = i
                    if j == ']':
                        rightBracket = i

                name = item[:leftBracket]
                size = item[leftBracket+1:rightBracket]
                predicates.append(name)
                predicatesSize[name] = size

        elif lineArray[0] == 'equality:':
            equality = lineArray[1:]
        elif lineArray[0] == 'connectives:':
            connectives = lineArray[1:]
        elif lineArray[0] == 'quantifiers:':
            quantifiers = lineArray[1:]
        elif lineArray[0] == 'formula:':
            rawFormula = lineArray[1:]
        else:
            rawFormula += lineArray

    # Checks for formulae which are predicates.
    index = 0
    formula = []
    while index < len(rawFormula):
        if rawFormula[index][-1] == ',':
            inc = 0
            temp = ''
            while rawFormula[index+inc][-1] == ',':
                temp += rawFormula[index + inc]
                inc += 1
            temp += rawFormula[index + inc]
            formula.append(temp)
            index += inc + 1
        else:
            formula.append(rawFormula[index])
            index += 1

def grammar():
    # Creates grammar file.
    grammarFile = open('{0}-Grammar.txt'.format(rawInputFile.replace('.txt', '')), "w")

    # All rules are stored in P. Each rule stored as an array [Rule Name, [Rule(s)]]
    P = [['S', ['F']]]

    # Start (S) Rule.

    # Adding Form (F) Rules.
    F = []

    R = []
    for element in predicates:
        size = ''
        if int(predicatesSize[element]) > 1:
            size = 'V, ' * (int(predicatesSize[element]) - 1)
        R.append('{0}({1})'.format(element, size + 'V').lower())

    F.append('(F)')
    F.append('R')
    F.append('QVF')
    F.append('G')
    F.append("FDF")

    D = []
    for element in connectives:
        if "\\neg" == element:
            F.append("{0} F".format(element))
        else:
            D.append("{0}".format(element))

    F.append("\\epsilon")

    Q = []
    for element in quantifiers:
        Q.append("{0}".format(element))

    P.append(['F', F])
    P.append(['R', R])
    P.append(['Q', Q])
    P.append(['D', D])

    # Equals (E) Rules.
    G = []
    for element in equality:
        G.append("T {0} T".format(element))
    P.append(['G', G])

    # Term (T) Rules.
    P.append(['T', ['C', 'V']])

    # Constant (C) Rules.
    C = []
    for element in constants:
        C.append(element.lower())
    P.append(['C', C])

    # Variable (V) Rules.
    V = []
    for element in variables:
        V.append(element)
    P.append(['V', V])

    for rule in P:
        rhsString = ''
        for rhs in range(len(rule[1])):
            if rhs == 0 and len(rule[1]) == 1:
                rhsString += rule[1][rhs]
            elif rhs == (len(rule[1]) - 1):
                rhsString += rule[1][rhs]
            else:
                rhsString += '{0} | '.format(rule[1][rhs])

        # Prints the rule to the grammar file.
        output = rule[0] + ' -> ' + rhsString + '\n'
        grammarFile.write(output)

    # closes the grammar file.
    grammarFile.close()

def parser():
    left, right = 1, 1
    valid = [False] * len(formula)
    for element in range(len(formula)):
        if formula[element] in variables:
            valid[element] = True
        elif formula[element] in constants:
            valid[element] = True
        elif formula[element] in connectives:
            valid[element] = True
        elif formula[element] in quantifiers:
            valid[element] = True
        elif formula[element] == '(':
            valid[element] = True
            left += 1
        elif formula[element] == ')':
            valid[element] = True
            right += 1
        elif formula[element] in equality:
            valid[element] = True
            # Checks the element before and after.
            if formula[element-1][0] == '(' and ((formula[element-1][1:] in constants) or (formula[element-1][1:] in variables)):
                valid[element-1] = True
            else:
                return False, 'Error - invalid equality i.e. {0} {1} {2}'.format(formula[element-1], formula[element], formula[element+1])
            if formula[element+1][-1] == ')' and ((formula[element+1][:-1] in constants) or (formula[element+1][:-1] in variables)):
                valid[element+1] = True
            else:
                return False, 'Error - invalid equality i.e. {0} {1} {2}'.format(formula[element-1], formula[element], formula[element+1])
        # exempts before and after equality from checks.
        elif formula[element-1] in equality or formula[element+1] in equality:
            continue
        # Check Predicate.
        else:
            leftBracket, rightBracket = 0, 0
            for x, y in enumerate(formula[element]):
                if y == '[' or y == '(':
                    leftBracket = x
                if y == ']' or y == ')':
                    rightBracket = x

            elementName = formula[element][:leftBracket]
            if elementName in predicates:
                valid[element] = True

                # Checks argument.
                args = formula[element][leftBracket + 1:rightBracket]
                argsValue = []
                prev = 0
                for x, y in enumerate(args):
                    if y == ',':
                        argsValue.append(args[prev:x])
                        prev = x
                if prev == 0:
                    argsValue.append(args[prev:len(args)])
                else:
                    argsValue.append(args[prev+1:len(args)])

                for argsElement in argsValue:
                    if argsElement not in variables:
                        return False, 'Error - invalid predicate i.e. {0}'.format(formula[element])

            # Could be before an equality.
            elif (formula[element+1] in equality) or (formula[element-1] in equality):
                continue
            else:
                return False, 'Error - invalid predicate i.e. {0}'.format(formula[element])

    if False in valid:
        return False, 'Error - Error Parsing'
    elif left != right:
        return False, 'Error - Invalid Bracket Pairs. i.e (())) is not allowed'
    else:
        return True, 'No Errors Calculated.'

def ADTBuilder(formula):
    # Prepend '(' & postpend ')' to formula.
    formula.insert(0, '(')
    formula.append(')')

    stack = []
    subGraph = 0

    # Assign every element in the formula a node.
    dot = Digraph(comment='ADT Graph')

    # List of connectives for the different subgraphs.
    interConnectives = []

    for index in range(0, len(formula)):
        # Checks predicates
        isPred = False
        for predicate in predicates:
            if predicate in formula[index]:
                stack.append(formula[index])
                isPred = True
        if not isPred:
            # Adding rules for equality splitting the () sign. (x = y)
            if formula[index][0] == '(' and formula[index+2][-1] == ')':
                stack.append('(')
                stack.append(formula[index][1:])
            elif formula[index][-1] == ')' and formula[index-2][0] == '(':
                stack.append(formula[index][:-1])
                stack.append(')')
            else:
                stack.append(formula[index])

        if stack[-1] is ')':
            subFormulae = []
            while stack[-1] is not "(":
                toAdd = stack.pop()
                if toAdd != '':
                    subFormulae.append(toAdd)
            subFormulae.append(stack.pop())
            subFormulae.reverse()

            # Find connectives adn equality but not Neg
            middle = []
            for i, j in enumerate(subFormulae):
                if j in connectives and j not in ['\\neg', 'NOT', 'not']:
                    middle.append(i)
                if j == '\\neg':
                    subFormulae[i] = 'neg'
                if j in equality:
                    middle.append(i)

            # If no connectives must be a quantifier.
            if not middle:
                # Create last nodes
                for element in range(1, len(subFormulae)-2):
                    name = 'A{0}'.format(element)
                    dot.node(name, subFormulae[element])
                # link last nodes
                for element in range(1, len(subFormulae)-3):
                    dot.edge('A{0}'.format(element), 'A{0}'.format(element+1))
                dot.edge('A{0}'.format(element+1), '{0}0'.format(subFormulae[element+2][1]))
            # Creates the Sub Tree
            else:
                if len(middle) == 1:
                    middle = middle[0]
                    # The connective is the root.
                    middleName = '{0}{1}'.format(subGraph, 0)
                    dot.node(middleName, subFormulae[middle])

                    # Create Nodes:
                    LHSFlag, LHSFirstFlag = 0, 0
                    prevName = middleName
                    for LHS in range(1, middle):
                        name = '{0}L{1}'.format(subGraph, LHS)
                        if subFormulae[LHS][0] == '#':
                            interConnectives.append([prevName, '{0}0'.format(subFormulae[LHS][1])])
                            LHSFlag = 1

                            # Checks if it is the first one.
                            if LHS == 1:
                                LHSFirstFlag = 1
                        else:
                            dot.node(name, subFormulae[LHS])
                            prevName = name

                    RHSFlag, RHSFirstFlag = 0, 0
                    prevName = middleName
                    for RHS in range(middle+1, len(subFormulae)-1):
                        name = '{0}R{1}'.format(subGraph, RHS)
                        if subFormulae[RHS][0] == '#':
                            interConnectives.append([prevName, '{0}0'.format(subFormulae[RHS][1])])
                            RHSFlag = 1

                            # Checks if it is the first one.
                            if RHS == middle+1:
                                RHSFirstFlag = 1
                        else:
                            dot.node(name, subFormulae[RHS])
                            prevName = name

                    # To middle node
                    lhsMain = '{0}L{1}'.format(subGraph, 1)
                    rhsMain = '{0}R{1}'.format(subGraph, middle + 1)
                    if LHSFirstFlag != 1:
                        dot.edge(middleName, lhsMain)
                    if RHSFirstFlag != 1:
                        dot.edge(middleName, rhsMain)

                    # LHS
                    LHSRange = middle
                    if LHSFlag == 1:
                        LHSRange -= 1
                    prevName = lhsMain
                    for LHS in range(2, LHSRange, 1):
                        currentName = '{0}L{1}'.format(subGraph, LHS)
                        dot.edge(prevName, currentName)
                        prevName = currentName

                    # RHS
                    RHSRange = len(subFormulae)-1
                    if RHSFlag == 1:
                        RHSRange -= 1
                    prevName = rhsMain
                    for RHS in range(middle+2, RHSRange, 1):
                        currentName = '{0}R{1}'.format(subGraph, RHS)
                        dot.edge(prevName, currentName)
                        prevName = currentName

                stack.append('#{0}'.format(str(subGraph)))
                subGraph += 1

    # Connect all sub graphs.
    for x in interConnectives:
        dot.edge(x[0], x[1])

    # Prints to file name-ADT.
    dot.render('{0}-ADT'.format(rawInputFile.replace('.txt', '')), view=True)

def logger(inputFile, status, message):
    logFile = open('log.txt', "a")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logFile.write("| Input File: {0} | Time: {1} | Status: {2} | Message: {3} |\n".format(inputFile, time, status, message))
    logFile.close()

grammar()
status, message = parser()
ADTBuilder(formula)
logger(rawInputFile, status, message)
