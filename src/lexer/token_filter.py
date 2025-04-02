from src.lexer.lexical_analyzer import tokenize

# Processes a file to tokenize its contents, filters out unwanted tokens, and identifies invalid ones.
def filter_tokens(file_name):

    # RPAL keywords
    keywords = {"let", "in", "where", "rec", "fn", "aug", "or", "not", "gr", "ge", 
                "ls", "le", "eq", "ne", "true", "false", "nil", "dummy", "within", "and"}

    try:
        with open(file_name, 'r') as file:
            characters = list(file.read())  # Read file content as a list of characters
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

    token_list = tokenize(characters)
    filtered_tokens = []
    invalid_token = None
    invalid_token_found = False

    for token in token_list:
        # Mark identifiers that match keywords as actual keywords
        if token.type == "<IDENTIFIER>" and token.content in keywords:
            token.type = "<KEYWORD>"

        # Skip tokens that should be deleted
        if token.type in {"<DELETE>", "<INVALID>"} or token.content == "\n":
            if token.type == "<INVALID>" and not invalid_token_found:
                invalid_token = token
                invalid_token_found = True
            continue
        
        filtered_tokens.append(token)

    # Mark the last token if the list is not empty
    if filtered_tokens:
        filtered_tokens[-1].is_last_token = True

    return filtered_tokens, invalid_token_found, invalid_token
