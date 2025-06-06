# 🚀 RPAL Interpreter

This is the final group project done for the CS3513 - Programming Languages module in Semester 04.

## 📝 Description

This project is an interpreter for the RPAL programming language, which is a functional programming language. The interpreter is implemented in Python to demonstrate the concepts of parsing, abstract syntax trees, and evaluation.

## 💻 Usage

Run the program using the following command:

```bash
python .\myrpal.py <file_name>
```

Where `file_name` is the path to your RPAL program file.

## 🧪 Running Tests

To run the tests, execute the following command:

```bash
python test.py
```

### 🔧 Command Line Switches

The following switches are available:

| Switch | Description |
|--------|-------------|
| `-ast` | Prints the abstract syntax tree |
| `-st`  | Prints the standardized tree |
| `-l`   | Prints the input file content |

#### Example:
```bash
python .\myrpal.py input.rpal -ast
```