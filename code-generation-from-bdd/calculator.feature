Feature: A simple calculator

Scenario Outline: Basic calculation
  Given I create a calculator instance
  When I call the method calculate with the parameters <number_a>, <number_b> and the <sign>
  Then Then the method should return <result>
  Examples:
  | number_a | number_b | sign | result |
  |        1 |        1 |    + |      2 |
  |        1 |        1 |    - |      0 |
