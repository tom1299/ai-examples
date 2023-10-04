# Prompt: Implement the steps for this specification using the file calculator.py
import re

from behave import given, when, then
from calculator import Calculator

@given('I create a calculator instance')
def step_impl(context):
  context.calculator = Calculator()

@when(u'I call the method calculate with the parameters {number_a:d}, {number_b:d} and the {sign}')
def step_impl(context, number_a, number_b, sign):
  context.result = context.calculator.calculate(number_a, number_b, sign)

@then(u'Then the method should return {result:d}')
def step_impl(context, result):
  assert context.result == result
