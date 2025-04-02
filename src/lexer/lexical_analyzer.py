from src.lexer.token import Token

def tokenize(characters):
    letters = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    digits = set('0123456789')
    operators = set('+-*<>&.@/:=~|$!#%^_[]{}"?')
    punctuation = set('();,')
    whitespace = {' ', '\t'}
    newline = '\n'
    
    tokens = []
    line_number = 1
    
    def add_token(value, token_type):
        tokens.append(Token(value, token_type, line_number))
    
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
            add_token("".join(characters[start:i]), '<IDENTIFIER>')
        
        # Integer or Invalid
        elif current_char in digits:
            start = i
            i += 1
            while i < n and characters[i] in digits:
                i += 1
            if i < n and characters[i] in letters:  # Invalid token
                while i < n and (characters[i] in letters or characters[i] in digits):
                    i += 1
                add_token("".join(characters[start:i]), '<INVALID>')
            else:
                add_token("".join(characters[start:i]), '<INTEGER>')
        
        # Comment
        elif current_char == '/' and i + 1 < n and characters[i + 1] == '/':
            i += 2
            while i < n and characters[i] != '\n':
                i += 1
            add_token("//", '<DELETE>')  # Marking as <DELETE>
        
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
                add_token("".join(characters[start:i]), '<STRING>')
            else:
                print("Error: String is not closed properly.")
                exit(1)
        
        # Punctuation
        elif current_char in punctuation:
            add_token(current_char, current_char)
            i += 1
        
        # Whitespace
        elif current_char in whitespace:
            i += 1  # Skip whitespace
        
        # Newline
        elif current_char == newline:
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
            add_token("".join(characters[start:i]), '<OPERATOR>')
        
        # Invalid character
        else:
            print(f"Error: Invalid character '{current_char}' at position {i}")
            exit(1)
    
    # Mark first and last tokens
    if tokens:
        tokens[0].make_first_token()
        tokens[-1].make_last_token()
    
    return tokens