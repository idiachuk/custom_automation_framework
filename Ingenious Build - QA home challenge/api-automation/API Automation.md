[Instructions](../INSTRUCTIONS.md) > [API Automation](API%20Automation.md)

# API Automation
## Requirements:
- Solve challenge with JS/TS language. Use any libraries or frameworks you want
  - Make sure that your choices are compatible with different OSes.
- Provide a `README.md` file for each challenge explaining:
  - How to set it up
  - How to execute it
- Model entities used
- Apply patterns to design your solution. We will evaluate:
  - Code repetition
  - Maintainability
  - Readability

  **Tip:** Do not over engineer

- Add comments to:
  - Register improvement opportunities, if any

## Forbidden:
- No record and play tool can be used

## Website to automate
[Reqres.in](https://reqres.in/)

## Tasks

### Validation 1:
  - Get a list of users
  - Validate that the response code is `200`
  - Print all users with odd ID numbers

### Validation 2:
  - Create a new user
  - Validate that the response code is `201`
  - Validate that the creation date is today

### Validation 3:
  - Update a user
  - Validate that the response code is `200`
  - Validate that the response body matches the request body where applicable. Do a recursive comparison if possible.

### Validation 4:
  - Write a parameterized validation with the values `0` and `3`
  - Get a list of users passing a delay query parameter with the provided value for the validation
  - Validate that the response time is no longer than `1` second

### Validation 5:
  - Use whatever asynchronous technique you prefer to get `10` single users
  - Validate, asynchronously as well, that all response codes are `200s`
