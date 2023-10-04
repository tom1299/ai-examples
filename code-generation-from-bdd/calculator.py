# Prompt: Creata a python class that only fulfills this specification (calculator.feature)
# "Only" is important because otherwise a full calculator implementation would get generated
class Calculator:
    def calculate(self, number_a, number_b, sign):
        if sign == '+':
            return number_a + number_b
        elif sign == '-':
            return number_a - number_b
        else:
            raise ValueError("Invalid sign")