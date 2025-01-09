package main

import (
	"calculator/pkg/calculator"
	"fmt"
	"os"
	"strconv"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: calculator <operation> [<num1> <num2>] or calculator pi <digits>")
		return
	}

	operation := os.Args[1]

	if operation == "pi" {
		if len(os.Args) < 3 {
			fmt.Println("Usage: calculator pi <digits>")
			return
		}
		digits, err := strconv.Atoi(os.Args[2])
		if err != nil {
			fmt.Println("Invalid number of digits. Please provide a valid integer.")
			return
		}
		result := calculator.CalculatePi(digits)
		fmt.Printf("Pi to %d digits: %s\n", digits, result)
		return
	}

	if len(os.Args) < 4 {
		fmt.Println("Usage: calculator <operation> <num1> <num2>")
		return
	}

	num1, err1 := strconv.ParseFloat(os.Args[2], 64)
	num2, err2 := strconv.ParseFloat(os.Args[3], 64)

	if err1 != nil || err2 != nil {
		fmt.Println("Invalid numbers. Please provide valid float64 values.")
		return
	}

	var result float64

	operations := map[string]func(float64, float64) float64{
		"add":      calculator.Add,
		"subtract": calculator.Subtract,
		"multiply": calculator.Multiply,
		"divide": func(a, b float64) float64 {
			if b == 0 {
				fmt.Println("Error: Division by zero.")
				os.Exit(1)
			}
			return calculator.Divide(a, b)
		},
	}

	operationFunc, exists := operations[operation]
	if !exists {
		fmt.Println("Unknown operation. Please use add, subtract, multiply, or divide.")
		return
	}

	result = operationFunc(num1, num2)

	fmt.Printf("Result: %f\n", result)
}
