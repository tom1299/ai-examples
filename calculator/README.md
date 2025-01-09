# Calculator Command Line Application

This project is a simple command line calculator application written in Go. It supports basic arithmetic operations such as addition, subtraction, multiplication, and division.

## Project Structure

```
calculator
├── cmd
│   └── main.go
├── pkg
│   └── calculator
│       └── calculator.go
├── go.mod
└── README.md
```

## Installation

To install the application, clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd calculator
```

## Build

To build the application, run the following command:

```bash
go build -o calculator ./cmd
```

## Usage

To run the calculator application, use the following command:

```bash
./calculator
```

### Examples

- Addition: `add 5 3` will return `8`
- Subtraction: `subtract 5 3` will return `2`
- Multiplication: `multiply 5 3` will return `15`
- Division: `divide 6 3` will return `2`

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.