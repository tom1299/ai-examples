package cmd

import (
	"calculator/calculator"
	"fmt"
	"os"
	"strconv"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "calculator",
	Short: "A simple calculator CLI",
	Long:  `A simple calculator CLI to perform basic arithmetic operations and calculate Pi.`,
}

var addCmd = &cobra.Command{
	Use:   "add [num1] [num2]",
	Short: "Add two numbers",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		num1, _ := strconv.ParseFloat(args[0], 64)
		num2, _ := strconv.ParseFloat(args[1], 64)
		result := calculator.Add(num1, num2)
		fmt.Printf("Result: %f\n", result)
	},
}

var subtractCmd = &cobra.Command{
	Use:   "subtract [num1] [num2]",
	Short: "Subtract two numbers",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		num1, _ := strconv.ParseFloat(args[0], 64)
		num2, _ := strconv.ParseFloat(args[1], 64)
		result := calculator.Subtract(num1, num2)
		fmt.Printf("Result: %f\n", result)
	},
}

var multiplyCmd = &cobra.Command{
	Use:   "multiply [num1] [num2]",
	Short: "Multiply two numbers",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		num1, _ := strconv.ParseFloat(args[0], 64)
		num2, _ := strconv.ParseFloat(args[1], 64)
		result := calculator.Multiply(num1, num2)
		fmt.Printf("Result: %f\n", result)
	},
}

var divideCmd = &cobra.Command{
	Use:   "divide [num1] [num2]",
	Short: "Divide two numbers",
	Args:  cobra.ExactArgs(2),
	Run: func(cmd *cobra.Command, args []string) {
		num1, _ := strconv.ParseFloat(args[0], 64)
		num2, _ := strconv.ParseFloat(args[1], 64)
		if num2 == 0 {
			fmt.Println("Error: Division by zero.")
			os.Exit(1)
		}
		result := calculator.Divide(num1, num2)
		fmt.Printf("Result: %f\n", result)
	},
}

func Execute() {
	rootCmd.AddCommand(addCmd, subtractCmd, multiplyCmd, divideCmd)
	if err := rootCmd.Execute(); err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
