class Token:
    def __init__(self, content, type, line):
        self.content = content
        self.type = type
        self.line = line
        self.is_first_token = False
        self.is_last_token = False
     
    # This function is used to print the token.
    # It is important when debugging.    
    def __str__(self):
        return f"{self.content} : {self.type}"
    
    # This function is used to mark the token as the first token.
    def make_first_token(self):
        self.is_first_token = True
        
    # This function is used to mark the token as the last token.
    # Marking the last token is important for the parsing process.    
    def make_last_token(self):
        self.is_last_token = True
        
    # This function is used to mark the token as a keyword.
    # This is used in the filter_tokens.    
    def make_keyword(self):
        self.type = "<KEYWORD>"