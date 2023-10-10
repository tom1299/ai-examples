Feature: Customer buys a product

Scenario Outline: Customer buys a product
    Given I am a customer with the email <customer_email>
    And the warehouse has <stock_quantity> products with the name "<product_name>"
    When I buy <quantity> products with the name "<product_name>"
    Then I should have <remaining_quantity> products with the name "<product_name>" in the warehouse
    Examples:
        | customer_email | stock_quantity | product_name | quantity | remaining_quantity |
        | customer1@online.com | 10 | "Product 1" | 2 | 8 |
        | customer2@online.com | 10 | "Product 2" | 2 | 8 |
