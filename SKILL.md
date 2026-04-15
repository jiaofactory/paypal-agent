# PayPal Payment Agent

A minimal viable PayPal payment integration skill for OpenClaw that enables AI agents to accept payments via PayPal, generate payment links, check payment status, and receive payment notifications.

**Version:** 0.1.0 (MVP)  
**Author:** Jiao Factory  
**Price:** $9.99  
**Target:** B2B, AI Agents, Freelancers

---

## Overview

This skill provides a simple interface to integrate PayPal payments into your AI agent workflows. It's designed for quick validation and fills a critical gap - **no payment skills currently exist on ClawHub!**

### Core Features

1. ✅ **Create Payment Links** - Generate reusable PayPal payment URLs
2. ✅ **Check Payment Status** - Query order/payment status in real-time
3. ✅ **Webhook Notifications** - Receive instant payment confirmations
4. ✅ **Sandbox Support** - Test mode for safe development

### Use Cases

- AI agents accepting payments for services
- Freelancers invoicing clients automatically
- Content creators selling digital products
- Developers monetizing bot interactions
- Micro-saas accepting one-time payments

---

## Installation

```bash
clawhub install paypal-agent
```

### Prerequisites

1. PayPal Business Account (use existing: `99.jiaojiao.99@gmail.com`)
2. PayPal Developer App with Client ID and Secret
3. Webhook endpoint URL (for notifications)

### Setup

1. Go to [PayPal Developer Dashboard](https://developer.paypal.com/)
2. Create a new REST API App
3. Get your **Client ID** and **Secret**
4. Configure webhook URL: `https://your-domain.com/webhooks/paypal`
5. Set environment variables (see Configuration)

---

## Configuration

Create a `.env` file or set these environment variables:

```bash
# PayPal API Credentials
PAYPAL_CLIENT_ID=your_client_id_here
PAYPAL_CLIENT_SECRET=your_client_secret_here

# Environment: sandbox or live
PAYPAL_MODE=sandbox

# Webhook ID (from PayPal dashboard)
PAYPAL_WEBHOOK_ID=your_webhook_id_here

# Optional: Custom return/cancel URLs
PAYPAL_RETURN_URL=https://your-domain.com/payment/success
PAYPAL_CANCEL_URL=https://your-domain.com/payment/cancel
```

---

## Quick Start

```python
from paypal_agent import PayPalAgent

# Initialize
paypal = PayPalAgent()

# Create a payment link
link = paypal.create_payment_link(
    amount="29.99",
    currency="USD",
    description="AI Agent Consultation Service",
    product_name="1-Hour AI Consultation"
)

print(f"Payment link: {link['url']}")
# Send this link to your customer!

# Check payment status
status = paypal.check_payment_status(link['order_id'])
print(f"Payment status: {status}")
```

---

## API Reference

### PayPalAgent Class

#### `create_payment_link(amount, currency, description, product_name, **options)`

Creates a reusable PayPal payment link.

**Parameters:**
- `amount` (str): Payment amount (e.g., "29.99")
- `currency` (str): Currency code (e.g., "USD", "EUR", "GBP")
- `description` (str): Product/service description
- `product_name` (str): Display name for the product
- `return_url` (str, optional): Post-payment redirect URL
- `cancel_url` (str, optional): Cancel redirect URL
- `custom_id` (str, optional): Your internal order/customer ID

**Returns:**
```python
{
    "order_id": "5O190127TN364715T",
    "url": "https://www.paypal.com/checkoutnow?token=5O190127TN364715T",
    "status": "CREATED",
    "amount": "29.99",
    "currency": "USD"
}
```

#### `check_payment_status(order_id)`

Check the current status of a payment.

**Parameters:**
- `order_id` (str): PayPal order ID

**Returns:**
```python
{
    "status": "APPROVED",  # CREATED, APPROVED, CAPTURED, VOIDED
    "amount": "29.99",
    "currency": "USD",
    "payer_email": "customer@example.com",
    "payer_name": "John Doe",
    "create_time": "2024-01-15T10:30:00Z"
}
```

#### `capture_payment(order_id)`

Capture an approved payment (for authorized payments).

**Parameters:**
- `order_id` (str): PayPal order ID

**Returns:**
```python
{
    "status": "COMPLETED",
    "capture_id": "CAP-123456",
    "amount": "29.99",
    "fee": "1.26"
}
```

#### `verify_webhook(headers, body)`

Verify that a webhook notification is genuinely from PayPal.

**Parameters:**
- `headers` (dict): HTTP headers from the webhook request
- `body` (str): Raw request body

**Returns:** `bool` - True if verified

#### `handle_webhook(payload)`

Process a webhook notification.

**Parameters:**
- `payload` (dict): Parsed webhook payload

**Returns:**
```python
{
    "event_type": "PAYMENT.CAPTURE.COMPLETED",
    "order_id": "5O190127TN364715T",
    "amount": "29.99",
    "payer_email": "customer@example.com",
    "custom_id": "your-internal-id"
}
```

---

## Webhook Events

The skill handles these PayPal webhook events:

| Event | Description |
|-------|-------------|
| `CHECKOUT.ORDER.APPROVED` | Customer approved the payment |
| `PAYMENT.CAPTURE.COMPLETED` | Payment successfully captured |
| `PAYMENT.CAPTURE.DENIED` | Payment was denied |
| `PAYMENT.CAPTURE.REFUNDED` | Payment was refunded |

### Webhook Handler Example (Flask)

```python
from flask import Flask, request, jsonify
from paypal_agent import PayPalAgent

app = Flask(__name__)
paypal = PayPalAgent()

@app.route('/webhooks/paypal', methods=['POST'])
def paypal_webhook():
    # Verify webhook authenticity
    if not paypal.verify_webhook(request.headers, request.data):
        return jsonify({"error": "Invalid signature"}), 400
    
    # Process the webhook
    payload = request.get_json()
    result = paypal.handle_webhook(payload)
    
    # Handle different event types
    if result['event_type'] == 'PAYMENT.CAPTURE.COMPLETED':
        # Fulfill the order!
        print(f"Payment received: {result['amount']} from {result['payer_email']}")
        # TODO: Send confirmation email, deliver product, etc.
    
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(port=5000)
```

---

## Example: Complete Payment Flow

```python
from paypal_agent import PayPalAgent
import time

paypal = PayPalAgent()

# Step 1: Create payment link
link = paypal.create_payment_link(
    amount="99.00",
    currency="USD",
    product_name="Premium AI Agent Setup",
    description="Complete setup and configuration of custom AI agent",
    custom_id="ORDER-12345"
)

print(f"✅ Payment link created: {link['url']}")
print(f"📋 Order ID: {link['order_id']}")

# Step 2: Send link to customer (via email, chat, etc.)
# ... your code here ...

# Step 3: Poll for payment status (or use webhooks for real-time)
print("⏳ Waiting for payment...")
for i in range(60):  # Check for 5 minutes
    status = paypal.check_payment_status(link['order_id'])
    
    if status['status'] == 'APPROVED':
        print("✅ Payment approved! Capturing...")
        capture = paypal.capture_payment(link['order_id'])
        print(f"✅ Payment captured! Fee: ${capture['fee']}")
        break
    elif status['status'] == 'VOIDED':
        print("❌ Payment cancelled")
        break
    
    time.sleep(5)

print("🎉 Transaction complete!")
```

---

## Testing

### Using PayPal Sandbox

1. Set `PAYPAL_MODE=sandbox` in your config
2. Use [PayPal Sandbox Accounts](https://developer.paypal.com/dashboard/accounts) to create test buyer/seller accounts
3. Use these test credit card numbers:
   - Visa: `4111111111111111`
   - MasterCard: `5555555555554444`
   - Any future expiry date, any CVV

### Webhook Testing (Local Development)

Use [ngrok](https://ngrok.com/) or [localtunnel](https://localtunnel.me/) to expose your local server:

```bash
# Install ngrok
npm install -g ngrok

# Expose port 5000
ngrok http 5000

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
# Set webhook URL in PayPal dashboard to: https://abc123.ngrok.io/webhooks/paypal
```

---

## Pricing & Revenue Model

**Skill Price:** $9.99 (one-time)

**Value Proposition:**
- Save 10+ hours of integration time
- Production-ready code
- Webhook security included
- Active maintenance

**B2B Potential:**
- Agencies can deploy for multiple clients
- AI agent builders can monetize services
- Freelancers can automate invoicing

---

## Roadmap

### v0.1.0 (Current MVP)
- ✅ Create payment links
- ✅ Check payment status  
- ✅ Webhook handling
- ✅ Sandbox support

### v1.0.0 (Planned)
- 🔄 Recurring payments/subscriptions
- 🔄 Refund processing
- 🔄 Invoice generation
- 🔄 Multi-currency support
- 🔄 Payouts to vendors

---

## Support

**Issues:** [GitHub Issues](https://github.com/yourusername/paypal-agent/issues)  
**Documentation:** This file + inline code comments  
**PayPal API Docs:** https://developer.paypal.com/api/rest/

---

## License

MIT License - Commercial use allowed

---

## ClawHub Metadata

```yaml
skill_id: paypal-agent
version: 0.1.0
category: payments
subcategory: paypal
tags: [paypal, payments, invoicing, ecommerce, b2b]
author: Jiao Factory
price: 9.99
currency: USD
clawhub_compatible: true
entry_point: paypal_agent.py
dependencies:
  - requests>=2.28.0
  - python-dotenv>=0.19.0
```
