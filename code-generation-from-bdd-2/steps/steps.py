from behave import given, when, then
from online_shop import Customer, Product, Warehouse, OnlineShop

@given('I am a customer with the email {email}')
def step_impl_given_customer(context, email):
    context.customer = Customer(email)

@given('I visit the online shop')
def step_impl_given_online_shop(context):
    context.online_shop = OnlineShop()

@given('the warehouse has {quantity:d} products with the name "{product_name}"')
def step_impl_given_warehouse(context, quantity, product_name):
    product = Product(product_name, quantity)
    context.online_shop.warehouse.add_product(product)

@when('I buy {quantity:d} products with the name "{product_name}"')
def step_impl_when_buy_product(context, quantity, product_name):
    context.result = context.online_shop.buy_product(context.customer, product_name, quantity)

@then('I should have {remaining_quantity:d} products with the name "{product_name}" in the warehouse')
def step_impl_then_remaining_quantity(context, remaining_quantity, product_name):
    product = context.online_shop.warehouse.get_product(product_name)
    assert product is not None, f"No product found with name '{product_name}'"
    assert product.quantity == remaining_quantity, f"Expected {remaining_quantity} products with name '{product_name}', but found {product.quantity}"