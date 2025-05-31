from src.ast_to_st.standardizer import standardize
from src.parser.node import *
from src.cse_machine.environment import Environment
from src.parser.stack import Stack
from src.cse_machine.structures import *

control_structures = []
count = 0
control = []
stack = Stack("CSE")
environments = [Environment(0, None)]
current_environment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction", "ItoS"]
output_flag  = False # To determine whether the output (Print) function is called in the program or not.


def generate_control_structure(root, i):
    global count
    
    while(len(control_structures) <= i):
        control_structures.append([])

    # Handle lambda expressions - create new control structure
    if (root.value == "lambda"):
        count += 1
        left_child = root.children[0]
        if (left_child.value == ","):
            temp = Lambda(count)
            
            x = ""
            for child in left_child.children:
                x += child.value[4:-1] + ","
            x = x[:-1]
            
            temp.bounded_variable = x
            control_structures[i].append(temp)
        else:
            temp = Lambda(count)
            temp.bounded_variable = left_child.value[4:-1]
            control_structures[i].append(temp)

        for child in root.children[1:]:
            generate_control_structure(child, count)

    # Handle conditional expressions
    elif (root.value == "->"):
        count += 1
        temp = Delta(count)
        control_structures[i].append(temp)
        generate_control_structure(root.children[1], count)
        count += 1
        temp = Delta(count)
        control_structures[i].append(temp)
        generate_control_structure(root.children[2], count)
        control_structures[i].append("beta")
        generate_control_structure(root.children[0], i)

    # Handle tuple construction
    elif (root.value == "tau"):
        n = len(root.children)
        temp = Tau(n)
        control_structures[i].append(temp)
        for child in root.children:
            generate_control_structure(child, i)

    else:
        control_structures[i].append(root.value)
        for child in root.children:
            generate_control_structure(child, i)

# Retrieve the value of a variable or constant.
def lookup(name):
    name = name[1:-1]
    info = name.split(":")
    
    if (len(info) == 1):
        value = info[0]
    else:
        data_type = info[0]
        value = info[1]
    
        if data_type == "INT":
            return int(value)
        elif data_type == "STR":
            return value.strip("'")
        elif data_type == "ID":
            if (value in builtInFunctions):
                return value
            else:
                try:
                    value = environments[current_environment].variables[value]
                except KeyError:
                    print("Undeclared Identifier: " + value)
                    exit(1)
                else:
                    return value
            
    if value == "Y*":
        return "Y*"
    elif value == "nil":
        return ()
    elif value == "true":
        return True
    elif value == "false":
        return False
    
def built_in(function, argument):
    global output_flag 
    
    # Order function - returns tuple length  
    if (function == "Order"):
        order = len(argument)
        stack.push(order)

    # Print functions - output to console.
    elif (function == "Print" or function == "print"):
        output_flag  = True
        
        # Handle escape sequences in strings
        if type(argument) == str:
            if "\\n" in argument:
                argument = argument.replace("\\n", "\n")
            if "\\t" in argument:
                argument = argument.replace("\\t", "\t")

        stack.push(argument)

    # Conc function - string concatenation
    elif (function == "Conc"):
        stack_symbol = stack.pop()
        control.pop()
        temp = argument + stack_symbol
        stack.push(temp)

    # Stern function - string without first character
    elif (function == "Stern"):
        stack.push(argument[1:])

    # Stem function - first character of string
    elif (function == "Stem"):
        stack.push(argument[0])

    # Type checking functions
    elif (function == "Isinteger"):
        if (type(argument) == int):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Istruthvalue"):
        if (type(argument) == bool):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Isstring"):
        if (type(argument) == str):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Istuple"):
        if (type(argument) == tuple):
            stack.push(True)
        else:
            stack.push(False)

    elif (function == "Isfunction"):
        if (argument in builtInFunctions):
            return True
        else:
            False
         
    elif (function == "ItoS"):
        if (type(argument) == int):
            stack.push(str(argument))
        else:
            print("Error: ItoS function can only accept integers.")
            exit()

# Apply the rules of the CSE machine to execute the program.
def execute_machine():
    op = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg", "not"]

    global control
    global current_environment

    while(len(control) > 0):
     
        symbol = control.pop()

        # Rule 1
        if type(symbol) == str and (symbol[0] == "<" and symbol[-1] == ">"):
            stack.push(lookup(symbol))

        # Rule 2
        elif type(symbol) == Lambda:
            temp = Lambda(symbol.number)
            temp.bounded_variable = symbol.bounded_variable
            temp.environment = current_environment
            stack.push(temp)

        # Rule 4
        elif (symbol == "gamma"):
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()

            if (type(stack_symbol_1) == Lambda):
                current_environment = len(environments)
                
                lambda_number = stack_symbol_1.number
                bounded_variable = stack_symbol_1.bounded_variable
                parent_environment_number = stack_symbol_1.environment

                parent = environments[parent_environment_number]
                child = Environment(current_environment, parent)
                parent.add_child(child)
                environments.append(child)

                # Rule 11
                variable_list = bounded_variable.split(",")
                
                if (len(variable_list) > 1):
                    for i in range(len(variable_list)):
                        child.add_variable(variable_list[i], stack_symbol_2[i])
                else:
                    child.add_variable(bounded_variable, stack_symbol_2)

                stack.push(child.name)
                control.append(child.name)
                control += control_structures[lambda_number]

            # Rule 10
            elif (type(stack_symbol_1) == tuple):
                stack.push(stack_symbol_1[stack_symbol_2 - 1])

            # Rule 12
            elif (stack_symbol_1 == "Y*"):
                temp = Eta(stack_symbol_2.number)
                temp.bounded_variable = stack_symbol_2.bounded_variable
                temp.environment = stack_symbol_2.environment
                stack.push(temp)

            # Rule 13
            elif (type(stack_symbol_1) == Eta):
                temp = Lambda(stack_symbol_1.number)
                temp.bounded_variable = stack_symbol_1.bounded_variable
                temp.environment = stack_symbol_1.environment
                
                control.append("gamma")
                control.append("gamma")
                stack.push(stack_symbol_2)
                stack.push(stack_symbol_1)
                stack.push(temp)

            # Built-in functions
            elif stack_symbol_1 in builtInFunctions:
                built_in(stack_symbol_1, stack_symbol_2)
              
        # Rule 5
        elif type(symbol) == str and (symbol[0:2] == "e_"):
            stack_symbol = stack.pop()
            stack.pop()
            
            if (current_environment != 0):
                for element in reversed(stack):
                    if (type(element) == str and element[0:2] == "e_"):
                        current_environment = int(element[2:])
                        break
            stack.push(stack_symbol)

        # Rule 6
        elif (symbol in op):
            rand_1 = stack.pop()
            rand_2 = stack.pop()
            if (symbol == "+"): 
                stack.push(rand_1 + rand_2)
            elif (symbol == "-"):
                stack.push(rand_1 - rand_2)
            elif (symbol == "*"):
                stack.push(rand_1 * rand_2)
            elif (symbol == "/"):
                stack.push(rand_1 // rand_2)
            elif (symbol == "**"):
                stack.push(rand_1 ** rand_2)
            elif (symbol == "gr"):
                stack.push(rand_1 > rand_2)
            elif (symbol == "ge"):
                stack.push(rand_1 >= rand_2)
            elif (symbol == "ls"):
                stack.push(rand_1 < rand_2)
            elif (symbol == "le"):
                stack.push(rand_1 <= rand_2)
            elif (symbol == "eq"):
                stack.push(rand_1 == rand_2)
            elif (symbol == "ne"):
                stack.push(rand_1 != rand_2)
            elif (symbol == "or"):
                stack.push(rand_1 or rand_2)
            elif (symbol == "&"):
                stack.push(rand_1 and rand_2)
            elif (symbol == "aug"):
                if (type(rand_2) == tuple):
                    stack.push(rand_1 + rand_2)
                else:
                    stack.push(rand_1 + (rand_2,))

        # Rule 7
        elif (symbol in uop):
            rand = stack.pop()
            if (symbol == "not"):
                stack.push(not rand)
            elif (symbol == "neg"):
                stack.push(-rand)

        # Rule 8
        elif (symbol == "beta"):
            B = stack.pop()
            else_part = control.pop()
            then_part = control.pop()
            if (B):
                control += control_structures[then_part.number]
            else:
                control += control_structures[else_part.number]

        # Rule 9
        elif type(symbol) == Tau:
            n = symbol.number
            tau_list = []
            for i in range(n):
                tau_list.append(stack.pop())
            tau_tuple = tuple(tau_list)
            stack.push(tau_tuple)

        elif (symbol == "Y*"):
            stack.push(symbol)

    # Lambda expression becomes a lambda closure when its environment is determined.
    if type(stack[0]) == Lambda:
        stack[0] = "[lambda closure: " + str(stack[0].bounded_variable) + ": " + str(stack[0].number) + "]"

    # Check if the top of the stack is a tuple
    if type(stack[0]) == tuple:          
        for i in range(len(stack[0])):
            # If the element is a boolean, convert it to lowercase string ('true'/'false')
            if type(stack[0][i]) == bool:
                stack[0] = list(stack[0])
                stack[0][i] = str(stack[0][i]).lower()
                stack[0] = tuple(stack[0])

        # If the tuple has only one element, format it with parentheses           
        if len(stack[0]) == 1:
            stack[0] = "(" + str(stack[0][0]) + ")"
        
       
        else: 
            # If the tuple contains any string elements, format the entire tuple as a string
            if any(type(element) == str for element in stack[0]):
                temp = "("
                for element in stack[0]:
                    temp += str(element) + ", "
                temp = temp[:-2] + ")"
                stack[0] = temp

    # Convert boolean values to lowercase strings.
    if stack[0] == True or stack[0] == False:
        stack[0] = str(stack[0]).lower()

# Get the result of the CSE machine execution for a given file.
def get_result(file_name):
    global control

    st = standardize(file_name)
    
    generate_control_structure(st,0) 
    
    control.append(environments[0].name)
    control += control_structures[0]

    stack.push(environments[0].name)

    execute_machine()

    if output_flag :
        print(stack[0])