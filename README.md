
# SyncStream

## Table of Contents

1. Project Overview
2. Demo Video
3. Prerequisites
4. Setup
5. Development
6. Testing with Postman



## This project implements a two-way integration between a local customer catalog and Stripe, with near real-time synchronization using Kafka as a message queue.
   
## [DEMO-VIDEO-LINK](https://drive.google.com/file/d/1KiVDRyxmWM5IIETU_HpkmmmoKU4eP7h-/view?usp=drive_link)


## Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher
- Ngrok (for exposing local API to Stripe webhook)
- Stripe account (for API key and webhook secret)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/harsh-kumar-patwa/SyncStream.git
   cd SyncStream
   ```

2. Create a `.env` file in the project root and add your Stripe credentials:
   ```
   STRIPE_API_KEY=your_stripe_api_key_here
   STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_here
   ```

3. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```

   This will start Zookeeper, Kafka, and the main application.

4. Once the application is running, use Ngrok to expose your local API:
   ```
   ngrok http 5000
   ```

   Note the HTTPS URL provided by Ngrok, you'll need this for setting up the Stripe webhook.

5. Set up a Stripe webhook:
   - Go to the Stripe Dashboard > Developers > Webhooks
   - Click "Add endpoint"
   - Use the Ngrok HTTPS URL + "/webhook/stripe" as the endpoint URL
   - Select the events you want to listen to (e.g., customer.created, customer.updated, customer.deleted)

6. The application should now be running and ready to handle two-way sync between your local customer catalog and Stripe.


## Development

To set up the development environment:

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. You can now run the application locally for development:
   ```
   python main.py
   ```

### Making Changes and Testing

When you make changes to your code and want to test them, follow these steps:

1. Stop the running containers:
   ```
   docker-compose down
   ```

2. Rebuild the containers:
   ```
   docker-compose build
   ```

3. Start the containers again:
   ```
   docker-compose up
   ```

This process ensures that your changes are included in the Docker image and that you're testing with a fresh environment each time.


## Testing with Postman

To test the API endpoints, you can use Postman. Here's how to set it up and test the main functionalities:

1. **Base URL:**
   - If using Ngrok: Use the Ngrok URL (e.g., `https://your-ngrok-url.ngrok.io`) and add it to the environment variable and name it base_url

3. **Endpoints to Test:**

   a. **Create a Customer**
   - Method: POST
   - URL: `{{base_url}}/customers`
   - Body (raw JSON):
     ```json
     {
         "name": "John Doe",
         "email": "john.doe@example.com"
     }
     ```

   b. **Get All Customers**
   - Method: GET
   - URL: `{{base_url}}/customers`

   c. **Get a Specific Customer**
   - Method: GET
   - URL: `{{base_url}}/customers/{customer_id}`

   d. **Update a Customer**
   - Method: PUT
   - URL: `{{base_url}}/customers/{customer_id}`
   - Body (raw JSON):
     ```json
     {
         "name": "John Updated",
         "email": "john.updated@example.com"
     }
     ```

   e. **Delete a Customer**
   - Method: DELETE
   - URL: `{{base_url}}/customers/{customer_id}`

4. **Testing Workflow:**
   - Create a new customer and note the returned ID
   - Retrieve all customers to verify the new addition
   - Get the specific customer using the ID
   - Update the customer's information
   - Verify the update by getting the customer again
   - Delete the customer
   - Confirm deletion by trying to get the customer (it  would return customer doesn't exist error)

5. **Verifying Stripe Sync:**
   - After each operation, check your Stripe dashboard to ensure the changes are reflected there as well
   - You will have need to refresh the Stripe dashboard to see the updates

Remember to replace `{customer_id}` with actual IDs returned from your create or get all customers requests.

