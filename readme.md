---

# SendGrid Billing Notification

This repository contains a script for sending billing notification emails using the SendGrid API.

## Setup

1. Clone the repository:
   ```shell
   $ git clone https://github.com/amit-successive/sendgrid-billing-notification.git
   ```

2. Navigate to the project directory:
   ```shell
   $ cd sendgrid-billing-notification
   ```

3. Create a virtual environment and activate it:
   ```shell
   $ pip install virtualenv
   $ virtualenv venv
   $ source venv/bin/activate
   ```

4. Install the required packages:
   ```shell
   $ pip install -r requirements.txt
   ```

5. Configure environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following variables to the `.env` file and replace the placeholder values with your own:
     ```
     SENDGRID_API_KEY=your_sendgrid_api_key
     SMTP_EMAIL=your_smtp_email
     SMTP_PASSWORD=your_smtp_password
     RECEIVER_EMAIL=your_receiver_email
     ```

6. Run the script:
   ```shell
   $ python sendgrid.py
   ```

---

You can customize the instructions based on your specific project setup and requirements. Make sure to provide accurate information and include any additional setup steps or configuration details if necessary.

Remember to keep the README up-to-date with any changes to the project setup or instructions to help users understand how to use and set up your script.
