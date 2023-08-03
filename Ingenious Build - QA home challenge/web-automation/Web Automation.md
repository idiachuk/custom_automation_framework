[Instructions](../INSTRUCTIONS.md) > [Web Automation](Web%20Automation.md)

# Web Automation
## Requirements:
- Solve challenge with JS/TS language. Use any libraries or frameworks you want
  - Make sure that your choices are compatible with different OSes.
- Provide a `README.md` file for each challenge explaining:
  - How to set it up
  - How to execute it

- Apply patterns to design your solution. We will evaluate:
  - Code repetition
  - Maintainability
  - Readability

  **Tip:** Do not over engineer

- Add comments to:
  - Register improvement opportunities, if any

## Forbidden:
- No record and play tool can be used
- No tool generated locators can be used

## Website to automate
[Saucedemo.com](https://www.saucedemo.com/)

## Tasks

### Validation 1:
  - Log in as a `standard user`
  - Find an item by name, then add it to the cart
  - Find a second item by name, and add it to the cart as well
  - Go to the cart
  - Find an item by name, then remove it from the cart
  - Validate in the Checkout Overview that:
    - It only contains the items that you want to purchase
    - The Item Total is right
  - Finish the purchase
  - Validate that the website confirms the order

### Validation 2:
  - Log in as a `standard user`
  - Sort products by name
  - Validate that the sorting is right

### Validation 3:
  - Log in as a `standard user`
  - Sort products by price
  - Validate that the sorting is right

### Validation 4:
  - Log in as a `locked_out_user`
  - The validation should fail
  - Add capabilities to your program so it can create reports with screenshots when something fails

