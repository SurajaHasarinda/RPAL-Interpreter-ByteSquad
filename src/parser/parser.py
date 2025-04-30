from src.lexer.token_filter import filter_tokens
from src.parser.stack import Stack
from src.parser.node import *

ast_builder = Stack("AST")  # Stack for building the AST

def build_ATS(label, child_count):
    node = Node(label)
    node.children = [None] * child_count
    for idx in range(child_count):
        if ast_builder.is_empty():
            print("Error: AST stack is empty during node creation.")
            exit(1)
        node.children[child_count - idx - 1] = ast_builder.pop()
    ast_builder.push(node)

def expect(token_value):
    if tokens[0].content != token_value:
        print(f"Syntax error at line {tokens[0].line}: Expected '{token_value}', found '{tokens[0].content}'")
        exit(1)
    if not tokens[0].is_last_token:
        del tokens[0]
    else:
        if tokens[0].type != ")":
            tokens[0].type = ")"

def parse(file_path):
    global tokens
    tokens, has_invalid, bad_token = filter_tokens(file_path)
    if has_invalid:
        print(f"Invalid token at line {bad_token.line}: {bad_token.content}")
        exit(1)
    E()
    if not ast_builder.is_empty():
        return ast_builder.pop()
    else:
        print("Error: AST stack is empty after parsing.")
        exit(1)

def E():
    if tokens[0].content == "let":
        expect("let")
        D()
        if tokens[0].content == "in":
            expect("in")
            E()
            build_ATS("let", 2)
        else:
            print(f"Syntax error at line {tokens[0].line}: Missing 'in' after 'let'")
            exit(1)
    elif tokens[0].content == "fn":
        expect("fn")
        vb_count = 0
        while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(":
            Vb()
            vb_count += 1
        if vb_count == 0:
            print(f"Syntax error at line {tokens[0].line}: Expected identifier or '(' after 'fn'")
            exit(1)
        if tokens[0].content == ".":
            expect(".")
            E()
            build_ATS("lambda", vb_count + 1)
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected '.' after variable bindings")
            exit(1)
    else:
        Ew()

def Ew():
    T()
    if tokens[0].content == "where":
        expect("where")
        Dr()
        build_ATS("where", 2)

def T():
    Ta()
    tau_count = 0
    while tokens[0].content == ",":
        expect(",")
        Ta()
        tau_count += 1
    if tau_count > 0:
        build_ATS("tau", tau_count + 1)

def Ta():
    Tc()
    while tokens[0].content == "aug":
        expect("aug")
        Tc()
        build_ATS("aug", 2)

def Tc():
    B()
    if tokens[0].content == "->":
        expect("->")
        Tc()
        if tokens[0].content == "|":
            expect("|")
            Tc()
            build_ATS("->", 3)
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected '|' after '->'")
            exit(1)

def B():
    Bt()
    while tokens[0].content == "or":
        expect("or")
        Bt()
        build_ATS("or", 2)

def Bt():
    Bs()
    while tokens[0].content == "&":
        expect("&")
        Bs()
        build_ATS("&", 2)

def Bs():
    if tokens[0].content == "not":
        expect("not")
        Bp()
        build_ATS("not", 1)
    else:
        Bp()

def Bp():
    A()
    if tokens[0].content in ["gr", ">", "ge", ">=", "ls", "<", "le", "<=", "eq", "ne"]:
        op = tokens[0].content
        expect(op)
        A()
        op_map = {
            "gr": "gr", ">": "gr",
            "ge": "ge", ">=": "ge",
            "ls": "ls", "<": "ls",
            "le": "le", "<=": "le",
            "eq": "eq", "ne": "ne"
        }
        build_ATS(op_map[op], 2)

def A():
    if tokens[0].content == "+":
        expect("+")
        At()
    elif tokens[0].content == "-":
        expect("-")
        At()
        build_ATS("neg", 1)
    else:
        At()
    while tokens[0].content in ["+", "-"]:
        op = tokens[0].content
        expect(op)
        At()
        build_ATS(op, 2)

def At():
    Af()
    while tokens[0].content in ["*", "/"]:
        op = tokens[0].content
        expect(op)
        Af()
        build_ATS(op, 2)

def Af():
    Ap()
    if tokens[0].content == "**":
        expect("**")
        Af()
        build_ATS("**", 2)

def Ap():
    R()
    while tokens[0].content == "@":
        expect("@")
        if tokens[0].type == "<IDENTIFIER>":
            build_ATS(f"<ID:{tokens[0].content}>", 0)
            expect(tokens[0].content)
            R()
            build_ATS("@", 3)
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected identifier after '@'")
            exit(1)

def R():
    Rn()
    while tokens[0].type in ["<IDENTIFIER>", "<INTEGER>", "<STRING>"] or tokens[0].content in ["true", "false", "nil", "(", "dummy"]:
        Rn()
        build_ATS("gamma", 2)

def Rn():
    val = tokens[0].content
    if tokens[0].type == "<IDENTIFIER>":
        expect(val)
        build_ATS(f"<ID:{val}>", 0)
    elif tokens[0].type == "<INTEGER>":
        expect(val)
        build_ATS(f"<INT:{val}>", 0)
    elif tokens[0].type == "<STRING>":
        expect(val)
        build_ATS(f"<STR:{val}>", 0)
    elif val in ["true", "false", "nil", "dummy"]:
        expect(val)
        build_ATS(f"<{val}>", 0)
    elif val == "(":
        expect("(")
        E()
        if tokens[0].content == ")":
            expect(")")
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected ')'")
            exit(1)
    else:
        print(f"Syntax error at line {tokens[0].line}: Unexpected token '{val}' in Rn")
        exit(1)

def D():
    Da()
    if tokens[0].content == "within":
        expect("within")
        D()
        build_ATS("within", 2)

def Da():
    Dr()
    and_count = 0
    while tokens[0].content == "and":
        expect("and")
        Dr()
        and_count += 1
    if and_count > 0:
        build_ATS("and", and_count + 1)

def Dr():
    if tokens[0].content == "rec":
        expect("rec")
        Db()
        build_ATS("rec", 1)
    else:
        Db()

def Db():
    val = tokens[0].content
    if val == "(":
        expect("(")
        D()
        if tokens[0].content == ")":
            expect(")")
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected ')' in Db")
            exit(1)
    elif tokens[0].type == "<IDENTIFIER>":
        expect(val)
        build_ATS(f"<ID:{val}>", 0)
        if tokens[0].content in [",", "="]:
            Vl()
            expect("=")
            E()
            build_ATS("=", 2)
        else:
            vb_count = 0
            while tokens[0].type == "<IDENTIFIER>" or tokens[0].type == "(":
                Vb()
                vb_count += 1
            if vb_count == 0:
                print(f"Syntax error at line {tokens[0].line}: Expected identifier or '(' in Db")
                exit(1)
            if tokens[0].content == "=":
                expect("=")
                E()
                build_ATS("function_form", vb_count + 2)
            else:
                print(f"Syntax error at line {tokens[0].line}: Expected '=' in function binding")
                exit(1)

def Vb():
    val1 = tokens[0].content
    if tokens[0].type == "<IDENTIFIER>":
        expect(val1)
        build_ATS(f"<ID:{val1}>", 0)
    elif val1 == "(":
        expect("(")
        val2 = tokens[0].content
        if val2 == ")":
            expect(")")
            build_ATS("()", 0)
        elif tokens[0].type == "<IDENTIFIER>":
            expect(val2)
            build_ATS(f"<ID:{val2}>", 0)
            Vl()
            if tokens[0].content == ")":
                expect(")")
            else:
                print(f"Syntax error at line {tokens[0].line}: Expected ')' after variable list")
                exit(1)
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected identifier or ')' in variable binding")
            exit(1)
    else:
        print(f"Syntax error at line {tokens[0].line}: Expected identifier or '(' in variable binding")
        exit(1)

def Vl():
    comma_count = 0
    while tokens[0].content == ",":
        expect(",")
        if tokens[0].type == "<IDENTIFIER>":
            val = tokens[0].content
            expect(val)
            build_ATS(f"<ID:{val}>", 0)
            comma_count += 1
        else:
            print(f"Syntax error at line {tokens[0].line}: Expected identifier after ','")
    if comma_count > 0:
        build_ATS(",", comma_count + 1)