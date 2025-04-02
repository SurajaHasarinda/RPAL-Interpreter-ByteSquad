from src.lexer.token import Token

def tokenize(characters):
    letters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    digits = set('0123456789')
    operators = set('+-*<>&.@/:=~|$!#%^_[]{}"?')
    punctuation = set('();,')
    whitespace = {' ', '\t'}
    newline = '\n'
    
    tokens, token_names, line_numbers = [], [], []
    line_number = 1
    
    def add_token(value, token_type, line):
        tokens.append(value)
        token_names.append(token_type)
        line_numbers.append(line)
    
    i = 0
    n = len(characters)
    while i < n:
        current_char = characters[i]
        
        # Identifier
        if current_char in letters:
            start = i
            i += 1
            while i < n and (characters[i] in letters or characters[i] in digits or characters[i] == '_'):
                i += 1
            add_token("".join(characters[start:i]), '<IDENTIFIER>', line_number)
        
        # Integer or Invalid
        elif current_char in digits:
            start = i
            i += 1
            while i < n and characters[i] in digits:
                i += 1
            if i < n and characters[i] in letters:  # Invalid token
                while i < n and (characters[i] in letters or characters[i] in digits):
                    i += 1
                add_token("".join(characters[start:i]), '<INVALID>', line_number)
            else:
                add_token("".join(characters[start:i]), '<INTEGER>', line_number)
        
        # Comment
        elif current_char == '/' and i + 1 < n and characters[i + 1] == '/':
            start = i
            i += 2
            while i < n and characters[i] != '\n':
                i += 1
            add_token("".join(characters[start:i]), '<DELETE>', line_number)
        
        # String
        elif current_char == "'":
            start = i
            i += 1
            while i < n and characters[i] != "'":
                if characters[i] == '\n':
                    line_number += 1
                i += 1
            if i < n:  # Properly closed string
                i += 1
                add_token("".join(characters[start:i]), '<STRING>', line_number)
            else:
                print("String is not closed properly.")
                exit(1)
        
        # Punctuation
        elif current_char in punctuation:
            add_token(current_char, current_char, line_number)
            i += 1
        
        # Whitespace
        elif current_char in whitespace:
            start = i
            i += 1
            while i < n and characters[i] in whitespace:
                i += 1
            add_token(' ', '<DELETE>', line_number)
        
        # Newline
        elif current_char == '\n':
            add_token(newline, '<DELETE>', line_number)
            line_number += 1
            i += 1
        
        # Operator
        elif current_char in operators:
            start = i
            i += 1
            while i < n and characters[i] in operators:
                if characters[i] == '/' and i + 1 < n and characters[i + 1] == '/':
                    break  # Comment detected
                i += 1
            add_token("".join(characters[start:i]), '<OPERATOR>', line_number)
        
        # Invalid character
        else:
            print(f"Invalid character: {current_char} at position {i}")
            exit(1)
    
    # Convert tokens into Token objects
    token_objects = []
    for idx, token_value in enumerate(tokens):
        token_obj = Token(token_value, token_names[idx], line_numbers[idx])
        if idx == 0:
            token_obj.make_first_token()
        if idx == len(tokens) - 1:
            token_obj.make_last_token()
        token_objects.append(token_obj)
    
    return token_objects