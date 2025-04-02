from src.lexer.token import Token

def tokenize(characters):
    letters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    digits = set('0123456789')
    operators = set('+-*<>&.@/:=~|$!#%^_[]{}"?')
    punctuation = set('();,')
    whitespace = {' ', '\t'}
    newline = '\n'
    
    tokens, token_names, line_numbers = [], [], []
    i, line_number = 0, 1
    
    def add_token(value, token_type, line):
        tokens.append(value)
        token_names.append(token_type)
        line_numbers.append(line)
    
    while i < len(characters):
        current_char = characters[i]
        
        if current_char in letters:  # Identifier
            start = i
            while i < len(characters) and (characters[i] in letters or characters[i] in digits or characters[i] == '_'):
                i += 1
            add_token("".join(characters[start:i]), '<IDENTIFIER>', line_number)
        
        elif current_char in digits:  # Integer or Invalid
            start = i
            while i < len(characters) and characters[i] in digits:
                i += 1
            if i < len(characters) and characters[i] in letters:  # Invalid token
                while i < len(characters) and (characters[i] in letters or characters[i] in digits):
                    i += 1
                add_token("".join(characters[start:i]), '<INVALID>', line_number)
            else:
                add_token("".join(characters[start:i]), '<INTEGER>', line_number)
        
        elif current_char == '/' and i + 1 < len(characters) and characters[i + 1] == '/':  # Comment
            start = i
            while i < len(characters) and characters[i] != '\n':
                i += 1
            add_token("".join(characters[start:i]), '<DELETE>', line_number)
        
        elif current_char == "'":  # String
            start = i
            i += 1
            while i < len(characters) and characters[i] != "'":
                if characters[i] == '\n':
                    line_number += 1
                i += 1
            if i < len(characters):  # Properly closed string
                i += 1
                add_token("".join(characters[start:i]), '<STRING>', line_number)
            else:
                print("String is not closed properly.")
                exit(1)
        
        elif current_char in punctuation:  # Punctuation
            add_token(current_char, current_char, line_number)
            i += 1
        
        elif current_char in whitespace:  # Whitespace (Deleted)
            while i < len(characters) and characters[i] in whitespace:
                i += 1
            add_token(' ', '<DELETE>', line_number)
        
        elif current_char == '\n':  # Newline (Deleted)
            add_token(newline, '<DELETE>', line_number)
            line_number += 1
            i += 1
        
        elif current_char in operators:  # Operator
            start = i
            while i < len(characters) and characters[i] in operators:
                if characters[i] == '/' and i + 1 < len(characters) and characters[i + 1] == '/':
                    break  # Comment detected, handled above
                i += 1
            add_token("".join(characters[start:i]), '<OPERATOR>', line_number)
        
        else:  # Invalid character
            print(f"Invalid character: {current_char} at position {i}")
            exit(1)
    
    # Convert tokens into Token objects
    for idx, token_value in enumerate(tokens):
        token_obj = Token(token_value, token_names[idx], line_numbers[idx])
        if idx == 0:
            token_obj.make_first_token()
        if idx == len(tokens) - 1:
            token_obj.make_last_token()
        tokens[idx] = token_obj
    
    return tokens