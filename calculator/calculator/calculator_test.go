package calculator

import (
	"testing"
)

func TestAdd(t *testing.T) {
	result := Add(1, 2)
	expected := 3.0
	if result != expected {
		t.Errorf("Add(1, 2) = %f; want %f", result, expected)
	}

	result = Add(-1, -2)
	expected = -3.0
	if result != expected {
		t.Errorf("Add(-1, -2) = %f; want %f", result, expected)
	}

	result = Add(1.5, 2.5)
	expected = 4.0
	if result != expected {
		t.Errorf("Add(1.5, 2.5) = %f; want %f", result, expected)
	}

	result = Add(0, 0)
	expected = 0.0
	if result != expected {
		t.Errorf("Add(0, 0) = %f; want %f", result, expected)
	}
}

func TestSubtract(t *testing.T) {
	result := Subtract(5, 3)
	expected := 2.0
	if result != expected {
		t.Errorf("Subtract(5, 3) = %f; want %f", result, expected)
	}

	result = Subtract(-5, -3)
	expected = -2.0
	if result != expected {
		t.Errorf("Subtract(-5, -3) = %f; want %f", result, expected)
	}

	result = Subtract(5.5, 3.5)
	expected = 2.0
	if result != expected {
		t.Errorf("Subtract(5.5, 3.5) = %f; want %f", result, expected)
	}

	result = Subtract(0, 0)
	expected = 0.0
	if result != expected {
		t.Errorf("Subtract(0, 0) = %f; want %f", result, expected)
	}
}

func TestMultiply(t *testing.T) {
	result := Multiply(2, 3)
	expected := 6.0
	if result != expected {
		t.Errorf("Multiply(2, 3) = %f; want %f", result, expected)
	}

	result = Multiply(-2, 3)
	expected = -6.0
	if result != expected {
		t.Errorf("Multiply(-2, 3) = %f; want %f", result, expected)
	}

	result = Multiply(2.5, 2)
	expected = 5.0
	if result != expected {
		t.Errorf("Multiply(2.5, 2) = %f; want %f", result, expected)
	}

	result = Multiply(0, 5)
	expected = 0.0
	if result != expected {
		t.Errorf("Multiply(0, 5) = %f; want %f", result, expected)
	}
}

func TestDivide(t *testing.T) {
	result := Divide(6, 3)
	expected := 2.0
	if result != expected {
		t.Errorf("Divide(6, 3) = %f; want %f", result, expected)
	}

	result = Divide(6, 0)
	expected = 0.0
	if result != expected {
		t.Errorf("Divide(6, 0) = %f; want %f", result, expected)
	}

	result = Divide(-6, 3)
	expected = -2.0
	if result != expected {
		t.Errorf("Divide(-6, 3) = %f; want %f", result, expected)
	}

	result = Divide(7.5, 2.5)
	expected = 3.0
	if result != expected {
		t.Errorf("Divide(7.5, 2.5) = %f; want %f", result, expected)
	}

	result = Divide(0, 5)
	expected = 0.0
	if result != expected {
		t.Errorf("Divide(0, 5) = %f; want %f", result, expected)
	}
}

func TestCalculatePi(t *testing.T) {
	result := CalculatePi(5)
	expected := "3.14159"
	if result != expected {
		t.Errorf("CalculatePi(5) = %s; want %s", result, expected)
	}

	result = CalculatePi(10)
	expected = "3.1415926535"
	if result != expected {
		t.Errorf("CalculatePi(10) = %s; want %s", result, expected)
	}
}
