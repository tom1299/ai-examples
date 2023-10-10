        # FILEPATH: steps/steps.py
from behave import given, when, then
from online_shop import OnlineShop

@given('I am a customer with the email {customer_email}')
def step_impl(context, customer_email):
    context.shop = OnlineShop(customer_email)

@given('the warehouse has {stock_quantity:d} products with the name "{product_name}"')
def step_impl(context, stock_quantity, product_name):
    context.shop.add_product(product_name, stock_quantity)

@when('I buy {quantity:d} products with the name "{product_name}"')
def step_impl(context, quantity, product_name):
    context.shop.buy_product(product_name, quantity)

@then('I should have {remaining_quantity:d} products with the name "{product_name}" in the warehouse')
def step_impl(context, remaining_quantity, product_name):
    assert context.shop.get_product_quantity(product_name) == remaining_quantity