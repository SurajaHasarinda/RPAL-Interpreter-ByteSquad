from src.lexer.token_filter import filter_tokens
from src.parser.stack import Stack
from src.parser.node import *

stack = Stack("AST") # This stack is used to build the abstract syntax tree.

# Building AST (bottom-up)
def build_tree(value, num_children):
    node = Node(value)
    node.children = [None] * num_children
    
    for i in range (0, num_children):
        if stack.is_empty():
            print("Stack is empty")
            exit(1)
        node.children[num_children - i - 1] = stack.pop()
        
    stack.push(node)

# This function is used to read the expected token. 
def read(expected_token):
    if tokens[0].content != expected_token:
        print("Syntax error in line " + str(tokens[0].line) + ": Expected " + str(expected_token) + " but got " + str(tokens[0].content))
        exit(1)
     
    if not tokens[0].is_last_token:
        del tokens[0]   
        
    else:
        if tokens[0].type != ")":
            tokens[0].type = ")"    
            

def parse(file_name):
    global tokens
    tokens, invalid_flag, invalid_token = filter_tokens(file_name)
    
    # If there are invalid tokens, we cannot proceed with the parsing.
    if invalid_flag:
        print("Invalid token present in line " + str(invalid_token.line) + ": " + str(invalid_token.content))
        exit(1)
    
    procedure_E()
    
    if not stack.is_empty():
        root = stack.pop()
    else:
        print("Stack is empty")
        exit(1)
        
    return root
 
############################################################## 
def procedure_E():      
    # E -> 'let' D 'in' E 
    if tokens[0].content == "let":
        read("let")
        procedure_D()
        
        if tokens[0].content == "in":
            read("in")
            procedure_E()
            build_tree("let", 2)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": 'in' expected")
            exit(1)
    
    # E -> 'fn'  Vb+ '.' E    
    elif tokens[0].content == "fn":
        read("fn")
        n = 0

        while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(": 
            procedure_Vb()
            n += 1
            
        if n == 0:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
            exit(1)
            
        if tokens[0].content == ".":
            read(".")
            procedure_E()
            build_tree("lambda", n + 1)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": '.' expected")
            exit(1)
             
    # E  ->  Ew    
    else:
        procedure_Ew()

##############################################################
def procedure_Ew():
    # Ew -> T    
    procedure_T()
    
    # Ew -> T 'where' Dr   
    if tokens[0].content == "where":
        read("where")
        procedure_Dr()
        build_tree("where", 2)  
        
##############################################################
def procedure_T():     
    # T -> Ta
    procedure_Ta()
    
    # T -> Ta (','  Ta)+
    n = 0
    while tokens[0].content == ",":
        read(",")
        procedure_Ta()
        n += 1
        
    if n > 0:
        build_tree("tau", n+1)
        
##############################################################      
def procedure_Ta():  
    # Ta -> Tc
    procedure_Tc()
    
    # Ta -> Ta 'aug' Tc 
    while tokens[0].content == "aug":
        read("aug")
        procedure_Tc()
        build_tree("aug", 2)  
        
##############################################################
def procedure_Tc():   
    # Tc -> B
    procedure_B()
    
    # Tc -> B '->' Tc '|' Tc
    if tokens[0].content == "->":  
        read("->")
        procedure_Tc()
        
        if tokens[0].content == "|":
            read("|")
            procedure_Tc()
            build_tree("->", 3)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": '|' expected")
            exit(1)
            
##############################################################
def procedure_B():
    # B -> Bt
    procedure_Bt()
    
    # B -> B 'or' Bt
    while tokens[0].content == "or":
        read("or")
        procedure_Bt()
        build_tree("or", 2) 

##############################################################
def procedure_Bt():    
    # Bt -> Bs
    procedure_Bs()
    
    # Bt -> Bt '&' Bs
    while tokens[0].content == "&":
        read("&")
        procedure_Bs()
        build_tree("&", 2)
        
##############################################################
def procedure_Bs():
    # Bs -> 'not' Bp
    if tokens[0].content == "not":
        read("not")
        procedure_Bp()
        build_tree("not", 1)
        
    # Bs -> Bp
    else:
        procedure_Bp()
        
##############################################################
def procedure_Bp():           
    # Bp -> A
    procedure_A()
    
    # Bp -> A ('gr' | '>' ) A
    if tokens[0].content == "gr" or tokens[0].content == ">":
        read(tokens[0].content)
        procedure_A()
        build_tree("gr", 2)
        
    # Bp -> A ('ge' | '>=' ) A
    elif tokens[0].content == "ge" or tokens[0].content == ">=":
        read(tokens[0].content)
        procedure_A()
        build_tree("ge", 2)
        
    # Bp -> A ('ls' | '<' ) A
    elif tokens[0].content == "ls" or tokens[0].content == "<":
        read(tokens[0].content)
        procedure_A()
        build_tree("ls", 2)
        
    # Bp -> A ('le' | '<=' ) A
    elif tokens[0].content == "le" or tokens[0].content == "<=":
        read(tokens[0].content)
        procedure_A()
        build_tree("le", 2)
        
    # Bp -> A 'eq' A
    elif tokens[0].content == "eq":
        read("eq")
        procedure_A()
        build_tree("eq", 2)
        
    # Bp -> A 'ne' A
    elif tokens[0].content == "ne":
        read("ne")
        procedure_A()
        build_tree("ne", 2)

##############################################################
def procedure_A():
    # A -> '+' At
    if tokens[0].content=="+":
        read("+")
        procedure_At()
        
    # A -> '-' At
    elif tokens[0].content=="-":
        read("-")
        procedure_At()
        build_tree("neg", 1)
        
    # A -> At
    else:
        procedure_At()
        
    while tokens[0].content in ["+", "-"]:
        # A -> A '+' At
        if tokens[0].content=="+":
            read("+")
            procedure_At()
            build_tree("+", 2)
            
        # A -> A '-' At
        else:
            read("-")
            procedure_At()
            build_tree("-", 2)
    
##############################################################
def procedure_At():
    # At -> Af
    procedure_Af()
    
    while tokens[0].content in ["*", "/"]:
        # At -> At '*' Af
        if tokens[0].content=="*":
            read("*")
            procedure_Af()
            build_tree("*", 2)
            
        # At -> At '/' Af
        else:
            read("/")
            procedure_Af()
            build_tree("/", 2)

##############################################################
def procedure_Af():    
    # Af -> Ap 
    procedure_Ap()
    
    # Af -> Ap '**' Af
    if tokens[0].content == "**":     
        read("**")
        procedure_Af()
        build_tree("**", 2)
 
##############################################################    
def procedure_Ap():
    # Ap -> R
    procedure_R()
    
    # Ap -> Ap '@' <IDENTIFIER> R
    while tokens[0].content == "@":
        read("@")
        
        if tokens[0].type == "<IDENTIFIER>":
            build_tree("<ID:" + tokens[0].content + ">", 0)
            read(tokens[0].content)
            procedure_R()
            build_tree("@", 3)            
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier expected")
            exit(1)
    
##############################################################
def procedure_R():
    # R -> Rn
    procedure_Rn()
    
    # R -> R Rn
    while  tokens[0].type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false","nil", "(", "dummy"]: 
        procedure_Rn()
        build_tree("gamma", 2)

##############################################################
def procedure_Rn():   
    value = tokens[0].content
    
    # Rn -> <IDENTIFIER>
    if tokens[0].type == "<IDENTIFIER>":
        read(value)
        build_tree("<ID:" + value + ">", 0)
    
    # Rn -> <INTEGER>    
    elif tokens[0].type == "<INTEGER>":
        read(value)
        build_tree("<INT:" + value + ">", 0)
        
    # Rn -> <STRING>    
    elif tokens[0].type == "<STRING>":
        read(value)
        build_tree("<STR:" + value + ">", 0)
        
    # Rn -> 'true'
    #    -> 'false'
    #    -> 'nil'
    #    -> 'dummy'    
    elif value in ["true", "false", "nil", "dummy"]:
        read(value)
        build_tree("<" + value + ">", 0)
      
    # Rn -> '(' E ')'    
    elif value == "(":
        read("(")
        procedure_E()
        
        if tokens[0].content == ")":     
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
            exit(1)
            
    else:
        print("Syntax error in line " + str(tokens[0].line) + ": Identifier, Integer, String, 'true', 'false', 'nil', 'dummy' or '(' expected")
        exit(1)

##############################################################
def procedure_D():
    # D -> Da
    procedure_Da()
    
    # D -> Da 'within' D
    if tokens[0].content == "within":
        read("within")
        procedure_D()
        build_tree("within", 2)
    
##############################################################
def procedure_Da():
    # Da -> Dr
    procedure_Dr()
    
    # Da -> Dr ('and' Dr)+
    n = 0
    while tokens[0].content == "and":
        read("and")
        procedure_Dr()
        n += 1
        
    if n > 0:  
        build_tree("and", n + 1)
    
##############################################################
def procedure_Dr():
    # Dr -> 'rec' Db
    if tokens[0].content == "rec":
        read("rec")
        procedure_Db()
        build_tree("rec", 1)
        
    # Dr -> Db
    else:
        procedure_Db()
    
##############################################################
def procedure_Db():    
    value = tokens[0].content
    
    # Db -> '(' D ')'
    if value == "(":
        read("(")
        procedure_D()
        
        if tokens[0].content == ")":
            read(")")
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
            exit(1)

    elif tokens[0].type == "<IDENTIFIER>":
        read(value)
        build_tree("<ID:" + value + ">", 0)  

        # Db -> <IDENTIFIER> Vb+ '=' E
        if tokens[0].content in [",", "="]:  
            procedure_Vl()
            read("=")
            procedure_E()
            build_tree("=", 2)
        
        # Db -> Vl '=' E
        else: 
            n = 0
        
            while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(":
                procedure_Vb()
                n += 1
                
            if n == 0:
                print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
                exit(1)    
                
            if tokens[0].content == "=":
                read("=")
                procedure_E()
                build_tree("function_form", n + 2)
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": '=' expected")
                exit(1)

##############################################################
def procedure_Vb(): 
    # Vb -> <IDENTIFIER>
    #    -> '(' Vl ')'
    #    -> '(' ')' 
    
    value_1 = tokens[0].content 

    # Vb -> <IDENTIFIER>
    if tokens[0].type == "<IDENTIFIER>":
        read(value_1)
        build_tree("<ID:" + value_1 + ">", 0)     
        
    elif value_1 == "(":
        read("(")
        
        value_2 = tokens[0].content 
        
        # Vb -> '(' ')'
        if value_2 == ")":
            read(")")
            build_tree("()", 0)
        
        # Vb -> '(' Vl ')'
        elif tokens[0].type == "<IDENTIFIER>": 
            read(value_2)
            build_tree("<ID:" + value_2 + ">", 0)    
            procedure_Vl()
            
            if tokens[0].content == ")":
                read(")")
            else:
                print("Syntax error in line " + str(tokens[0].line) + ": ')' expected")
                exit(1)
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier or ')' expected")
            exit(1)
    else:
        print("Syntax error in line " + str(tokens[0].line) + ": Identifier or '(' expected")
        exit(1)
    
##############################################################
def procedure_Vl():
    # Vl -> <IDENTIFIER> (',' <IDENTIFIER>)*   
    n = 0
    
    while tokens[0].content == ",":
        read(",")
        
        if tokens[0].type == "<IDENTIFIER>":
            value = tokens[0].content
            read(value)
            build_tree("<ID:" + value + ">", 0)    
            n += 1
        else:
            print("Syntax error in line " + str(tokens[0].line) + ": Identifier expected")
            
    if n > 0:
        build_tree(",", n + 1) 