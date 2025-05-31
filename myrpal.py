from src.parser.parser import parse
from src.parser.node import preorder_traversal
from src.ast_to_st.standardizer import *
from cse_machine.cse_machine import *
import sys

def main():
    arguments = sys.argv
    
    if len(arguments) < 2:
        print("Invalid command. Usage: python ./myrpal.py [-l] [-ast] [-st] filename")
        sys.exit(1)
        
    else:
        if len(arguments) == 2: 
            file_name = arguments[1]
            get_result(file_name)
            
        else:
            flags = arguments[1 : -1] # Get the switches from the command line arguments.
            file_name = arguments[-1] # Get the file name from the command line arguments.
            
            if any(flag in flags for flag in ["-l", "-ast", "-st"]): # Check if any of the flags are present.

                # If '-l' is in the switches, we must print the file as it is.
                if "-l" in flags:
                    with open(file_name, "r") as file:
                        print(file.read())
                        
                    print()
                    
                # If '-ast' is in the switches, we must print the abstract syntax tree.
                if "-ast" in flags:
                    ast = parse(file_name)
                    preorder_traversal(ast)
                    
                    print()
                    
                    if "-st" in flags:
                        st = get_standardized_tree(ast)
                        preorder_traversal(st)
                        
                        print() 
                        exit()
                
                # If '-st' is in the switches, we must print the standardized tree.    
                elif "-st" in flags:
                    st = standardize(file_name)  
                    preorder_traversal(st)
                    
                    print()
                    exit()
            
            else:
                print("Invalid command. Usage: python ./myrpal.py [-l] [-ast] [-st] filename")
                sys.exit(1)

if __name__ == "__main__":
    main()
    