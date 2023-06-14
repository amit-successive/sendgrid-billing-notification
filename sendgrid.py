import os
import requests
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

# Load environment variables from .env file
load_dotenv()

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

def get_invoices():
    headers = {
        'Authorization': f'Bearer {SENDGRID_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Get invoices API endpoint
    invoices_url = 'https://api.sendgrid.com/v3/billing/invoices'

    try:
        response = requests.get(invoices_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        invoices = response.json()
        return invoices
    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {e}')
        return None

def send_email_notification(email_address, invoice_number):
    # Get invoice details
    invoice_details = get_invoice_details(invoice_number)

    if invoice_details:
        invoice_number = invoice_details['invoice_number']
        due_date = invoice_details['due_date']
        balance = invoice_details['balance']
        date = invoice_details['date']
        unpaid_balance = invoice_details['unpaid_balance']

        # Create the email message
        msg = EmailMessage()
        msg.set_content(f'Dear Customer,\n\nThis is an urgent reminder that your invoice {invoice_number} is still unpaid. Please make the payment at your earliest convenience.\n\nInvoice Details:\nInvoice Number: {invoice_number}\nDue Date: {due_date}\nBalance: {balance}\nDate: {date}\nUnpaid Balance: {unpaid_balance}\n\nThank you.\nAmit Halder')

        msg['Subject'] = f'[SENDGRID] Payment Reminder - Invoice {invoice_number} (Due Date: {due_date})'
        msg['From'] = SMTP_EMAIL
        msg['To'] = email_address

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)

def get_invoice_details(invoice_number):
    headers = {
        'Authorization': f'Bearer {SENDGRID_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Get invoice details API endpoint
    invoice_details_url = 'https://api.sendgrid.com/v3/billing/invoices'

    try:
        response = requests.get(invoice_details_url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        invoices = response.json()
        invoice = next((inv for inv in invoices['result'] if inv['invoice_number'] == invoice_number), None)
        return invoice
    except requests.exceptions.RequestException as e:
        print(f'Error occurred: {e}')
        return None

# Main function
if __name__ == '__main__':
    invoices = get_invoices()

    if invoices:
        invoices_list = invoices['result']
        invoices_list.sort(key=lambda x: x['date'], reverse=True)  # Sort invoices based on date

        recent_invoices = invoices_list[:10]  # Get the most recent 10 invoices

        unpaid_invoices = [invoice for invoice in recent_invoices if invoice['balance'] > 0]

        if unpaid_invoices:
            print('Unpaid Invoices:')
            for invoice in unpaid_invoices:
                invoice_number = invoice['invoice_number']
                email_address = RECEIVER_EMAIL

                print(f'Invoice Number: {invoice_number}')
                send_email_notification(email_address, invoice_number)
                print(f'Email notification sent for invoice {invoice_number}')
        else:
            print('No unpaid invoices.')
    else:
        print('Failed to retrieve invoices.')
