# Release Notes

## Version 1.0.0

### New Features
- **Addition Function**: Added the `Add` function to perform addition of two float64 numbers. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Subtraction Function**: Added the `Subtract` function to perform subtraction of two float64 numbers. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Multiplication Function**: Added the `Multiply` function to perform multiplication of two float64 numbers. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Division Function**: Added the `Divide` function to perform division of two float64 numbers with division by zero handling. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Calculate Pi Function**: Added the `CalculatePi` function to return a string representation of Pi to the specified number of digits. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Prime Calculation Function**: Added the `calculatePrime` function to check if a number is prime. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Compound Interest Calculation**: Added the `CalculateCompoundInterest` function to calculate compound interest. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)
- **Simple Interest Calculation**: Added the `CalculateSimpleInterest` function to calculate simple interest. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)

### Improvements
- **Command Line Interface**: Implemented a command line interface to perform basic arithmetic operations and calculate Pi. [calculator/cmd/main.go](calculator/cmd/main.go)

### Bug Fixes
- **Division by Zero**: Handled division by zero in the `Divide` function by returning 0 and printing an error message. [calculator/pkg/calculator/calculator.go](calculator/pkg/calculator/calculator.go)

### Tests
- **Unit Tests**: Added unit tests for all arithmetic functions and Pi calculation. [calculator/pkg/calculator/calculator_test.go](calculator/pkg/calculator/calculator_test.go)

### Documentation
- **README**: Added a README file with project structure, installation, build, usage instructions, and examples. [calculator/README.md](calculator/README.md)

### Docker
- **Dockerfile**: Added a Dockerfile to build and run the calculator application in a container. [calculator/Dockerfile](calculator/Dockerfile)