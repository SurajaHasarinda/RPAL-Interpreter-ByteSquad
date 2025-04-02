from src.lexer.lexical_analyzer import tokenize

def filter_tokens(file_name):
    # RPAL keywords 
    keywords = ["let", "in", "where", "rec", "fn", "aug", "or", "not", "gr", "ge", "ls", "le", "eq", "ne", "true", "false", "nil", "dummy", "within", "and"]
    
    characters = []
    token_list = []
    invalid_token_present = False
    invalid_token = None
    
    try:
        with open(file_name, 'r') as file:
            for line in file:
                for character in line:
                    characters.append(character)
            token_list = tokenize(characters)

    except FileNotFoundError:
        print("File not found.")
        exit(1)
    except Exception as e:
        print("An error occurred:", e)
        exit(1)
    
    # Iterate through token list in reverse order. This reverse iteration will correctly handle the consequent <DELETE>s
    for i in range(len(token_list) - 1, -1, -1):
        token = token_list[i]
        
        # If the token is an identifier and it is a keyword, it should be marked as a keyword.
        if token.type == "<IDENTIFIER>" and token.content in keywords:
            token.make_keyword()
        
        # If the token is should be deleted, it should be removed from the list.
        if token.type == "<DELETE>" or token.content == "\n":            
            token_list.remove(token)
            
        # If there are invalid tokens, the first invalid token will be marked as the invalid token.    
        if token.type == "<INVALID>":
            if invalid_token_present == False:
                invalid_token = token
                
            invalid_token_present = True
            
    # If the previous last token is removed in the previous loop, the last token will be the last token in the list.
    if len(token_list) > 0:
        token_list[-1].is_last_token = True
        
    return token_list, invalid_token_present, invalid_token