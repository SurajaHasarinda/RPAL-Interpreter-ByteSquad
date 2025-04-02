class Token:
    def __init__(self, content, type, line):
        self.content = content
        self.type = type
        self.line = line
        self.is_first_token = False
        self.is_last_token = False
     
    # Print the token.
    def __str__(self):
        return f"{self.content} : {self.type}"
    
    # Mark the token as the first token.
    def make_first_token(self):
        self.is_first_token = True
        
    # Mark the token as the last token (important for the parsing process).    
    def make_last_token(self):
        self.is_last_token = True