class Stack:
    def __init__(self, stack_type):
        self.stack = []
        self.type = stack_type

    # Debugging by returning the stack as a string
    def __repr__(self):
        return str(self.stack)

    # Enables indexing into the stack
    def __getitem__(self, index):
        return self.stack[index]

    def __setitem__(self, index, value):
        self.stack[index] = value

    # Enables reversed iteration over the stack
    def __reversed__(self):
        return reversed(self.stack)

    # Adds an element to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # Removes and returns the top element of the stack
    def pop(self):
        if self.is_empty():
            if self.type == "CSE":
                print("Error: CSE stack is unexpectedly empty.")
            else:
                print("Error: AST stack is unexpectedly empty.")
            exit(1)
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0
