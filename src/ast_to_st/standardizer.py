from src.parser.parser import *

# Convert the AST to a standardized tree
def standardize(file_name):
    ast = parse(file_name)
    st = get_standardized_tree(ast)
    
    return st

def get_standardized_tree(root):
    for child in root.children:
        get_standardized_tree(child)

    # let
    if root.value == "let" and root.children[0].value == "=":
        child_0 = root.children[0]
        child_1 = root.children[1]

        root.children[1] = child_0.children[1]
        root.children[0].children[1] = child_1
        root.children[0].value = "lambda"
        root.value = "gamma"

    # where
    elif root.value == "where" and root.children[1].value == "=":
        child_0 = root.children[0] 
        child_1 = root.children[1] 

        root.children[0] = child_1.children[1]
        root.children[1].children[1] = child_0
        root.children[1].value = "lambda"
        root.children[0], root.children[1] = root.children[1], root.children[0]
        root.value = "gamma"

    # fcn_from
    elif root.value == "fcn_from":
        expression = root.children.pop()

        current_node = root
        for i in range(len(root.children) - 1):
            lambda_node = Node("lambda")
            child = root.children.pop(1)
            lambda_node.children.append(child)
            current_node.children.append(lambda_node)
            current_node = lambda_node

        current_node.children.append(expression)
        root.value = "="

    # gamma
    elif root.value == "gamma" and len(root.children) > 2:
        expression = root.children.pop()

        current_node = root
        for i in range(len(root.children) - 1):
            lambda_node = Node("lambda")
            child = root.children.pop(1)
            lambda_node.children.append(child)
            current_node.children.append(lambda_node)
            current_node = lambda_node

        current_node.children.append(expression)

    # within
    elif root.value == "within" and root.children[0].value == root.children[1].value == "=":
        child_0 = root.children[1].children[0]
        child_1 = Node("gamma")

        child_1.children.append(Node("lambda"))
        child_1.children.append(root.children[0].children[1])
        child_1.children[0].children.append(root.children[0].children[0])
        child_1.children[0].children.append(root.children[1].children[1])

        root.children[0] = child_0
        root.children[1] = child_1
        root.value = "="

    # @
    elif root.value == "@":             
        expression = root.children.pop(0)
        identifier = root.children[0]

        gamma_node = Node("gamma")
        gamma_node.children.append(identifier)
        gamma_node.children.append(expression)

        root.children[0] = gamma_node

        root.value = "gamma"

    # and
    elif root.value == "and":
        child_0 = Node(",")
        child_1 = Node("tau")

        for child in root.children:
            child_0.children.append(child.children[0])
            child_1.children.append(child.children[1])

        root.children.clear()

        root.children.append(child_0)
        root.children.append(child_1)

        root.value = "="

    # rec
    elif root.value == "rec":
        temp = root.children.pop()
        temp.value = "lambda"

        gamma_node = Node("gamma")
        gamma_node.children.append(Node("<Y*>"))
        gamma_node.children.append(temp)

        root.children.append(temp.children[0])
        root.children.append(gamma_node)

        root.value = "="

    return root