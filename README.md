# 💰 PayPal Payment Agent

**The first payment skill on ClawHub!** Enable your AI agents to accept PayPal payments, generate payment links, and receive instant payment notifications.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/jiaofactory/paypal-agent)
[![Price](https://img.shields.io/badge/price-Free-green.svg)](https://github.com/jiaofactory/paypal-agent)
[![Python](https://img.shields.io/badge/python-3.8+-yellow.svg)](https://python.org)
[![PayPal](https://img.shields.io/badge/paypal-REST%20API-blue.svg)](https://developer.paypal.com)

---

## 🎯 Why This Skill?

**Critical Gap Filled:** Currently, NO payment processing skills exist on ClawHub. This skill enables:

- 🤖 AI agents that can accept payments for services
- 🧾 Automated invoicing for freelancers
- 🛒 Bot-driven product sales
- 💼 B2B payment automation
- 🎮 Game/micro-transaction integrations

**Target Users:**
- AI agent developers
- Freelancers & agencies
- Content creators
- SaaS builders
- Automation enthusiasts

---

## ⚡ Quick Start

```python
from paypal_agent import PayPalAgent

# Initialize
paypal = PayPalAgent()

# Create payment link
link = paypal.create_payment_link(
    amount="29.99",
    currency="USD",
    description="AI Consultation - 1 Hour",
    product_name="1-Hour AI Consultation"
)

print(f"🔗 Payment Link: {link['url']}")
# Send this to your customer!
```

---

## 🛠️ Installation

```bash
clawhub install paypal-agent
```

### Prerequisites

1. **PayPal Business Account** ([Sign up free](https://www.paypal.com/business))
2. **PayPal Developer App** ([Create here](https://developer.paypal.com/dashboard/applications))
3. **Python 3.8+**

### Configuration

Create `.env` file:

```bash
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_client_secret
PAYPAL_MODE=sandbox  # or 'live' for production
```

---

## 📖 API Reference

### `create_payment_link(amount, currency, description, product_name)`

Creates a PayPal payment link.

```python
link = paypal.create_payment_link(
    amount="99.00",
    currency="USD",
    description="Premium AI setup",
    product_name="AI Agent Configuration",
    custom_id="ORDER-123",  # Your internal ID
    return_url="https://yoursite.com/success",
    cancel_url="https://yoursite.com/cancel"
)

# Returns:
# {
#     "order_id": "5O190127TN364715T",
#     "url": "https://www.paypal.com/checkoutnow?token=...",
#     "status": "CREATED",
#     "amount": "99.00",
#     "currency": "USD"
# }
```

### `check_payment_status(order_id)`

Check payment status:

```python
status = paypal.check_payment_status("5O190127TN364715T")

# Returns:
# {
#     "order_id": "5O190127TN364715T",
#     "status": "APPROVED",  # CREATED, APPROVED, COMPLETED, VOIDED
#     "amount": "99.00",
#     "payer_email": "customer@example.com",
#     "payer_name": "John Doe"
# }
```

### `capture_payment(order_id)`

Capture an approved payment:

```python
capture = paypal.capture_payment("5O190127TN364715T")

# Returns:
# {
#     "capture_id": "CAP-123",
#     "status": "COMPLETED",
#     "amount": "99.00",
#     "fee": "3.20",
#     "net_amount": "95.80"
# }
```

---

## 🔔 Webhooks

Receive instant payment notifications:

```python
from flask import Flask, request
from paypal_agent import PayPalAgent

app = Flask(__name__)
paypal = PayPalAgent()

@app.route('/webhooks/paypal', methods=['POST'])
def handle_webhook():
    # Verify authenticity
    if not paypal.verify_webhook(request.headers, request.data):
        return "Invalid", 400
    
    # Process event
    payload = request.get_json()
    event = paypal.handle_webhook(payload)
    
    if event['event_type'] == 'PAYMENT.CAPTURE.COMPLETED':
        # 🎉 Payment received!
        print(f"Received ${event['amount']} from {event['payer_email']}")
        # Fulfill order, send email, etc.
    
    return "OK", 200
```

See `webhook_handler.py` for complete example.

---

## 💼 Use Cases

### 1. AI Agent Service

```python
# Your AI agent charges for consultations
def handle_consultation_request(user_message):
    if not user_has_credits(user):
        link = paypal.create_payment_link(
            amount="29.99",
            currency="USD",
            description="30-min AI consultation",
            product_name="AI Consultation"
        )
        return f"Please complete payment: {link['url']}"
    
    return process_consultation(user_message)
```

### 2. Automated Invoicing

```python
# Auto-generate invoice after project completion
def complete_project(project_id):
    project = get_project(project_id)
    
    link = paypal.create_payment_link(
        amount=str(project['price']),
        currency="USD",
        description=f"Project: {project['name']}",
        product_name=f"Invoice #{project['id']}",
        custom_id=project_id
    )
    
    send_email(project['client_email'], 
               subject="Invoice Ready",
               body=f"Pay here: {link['url']}")
```

### 3. Digital Product Sales

```python
# Sell digital products through your bot
def purchase_product(product_id, user_email):
    product = get_product(product_id)
    
    link = paypal.create_payment_link(
        amount=product['price'],
        currency="USD",
        description=product['description'],
        product_name=product['name'],
        custom_id=f"{user_email}:{product_id}"
    )
    
    return link['url']  # Send to user
```

---

## 🧪 Testing

### Sandbox Mode

```bash
# Use PayPal's test environment
PAYPAL_MODE=sandbox
```

Test credit cards:
- Visa: `4111111111111111`
- MasterCard: `5555555555554444`
- Any future expiry, any CVV

### Local Webhook Testing

```bash
# Install ngrok
npm install -g ngrok

# Expose local server
ngrok http 5000

# Copy HTTPS URL to PayPal webhook settings
# Example: https://abc123.ngrok.io/webhooks/paypal
```

---

## 💰 Pricing

| License | Price | Includes |
|---------|-------|----------|
| **Open Source** | Free | Full source code on GitHub |
| **Gumroad** | $4.99 | Packaged zip, quick install, updates |

**ROI Calculation:**
- Time saved: ~10 hours of integration
- Developer cost: $50-150/hour
- **Your savings: $500-1500**

---

## 🗺️ Roadmap

### v0.1.0 (Current) ✅
- Create payment links
- Check payment status
- Webhook handling
- Sandbox/live modes

### v1.0.0 (Planned) 🚧
- Recurring payments/subscriptions
- Refund processing
- Invoice PDF generation
- Multi-currency optimization
- Payouts to vendors

---

## 📚 Documentation

- [SKILL.md](SKILL.md) - Full documentation
- [examples.py](examples.py) - Usage examples
- [webhook_handler.py](webhook_handler.py) - Webhook setup
- [PayPal API Docs](https://developer.paypal.com/api/rest/)

---

## 🤝 Support

- 📧 Email: 99.jiaojiao.99@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/jiaofactory/paypal-agent/issues)
- 💬 Discussions: [ClawHub Community](https://clawhub.ai/community)

---

## 📄 License

MIT License - Commercial use allowed

---

## ⭐ Star This Skill!

If this skill helps you monetize your AI agents, please star it on ClawHub!

**Built with ❤️ by Jiao Factory**

---

## 🏆 Why Buy This Skill?

1. **⏰ Save Time** - 10+ hours of dev work done
2. **🔒 Production Ready** - Security best practices included
3. **📈 Monetize Fast** - Start accepting payments today
4. **🤖 AI-Native** - Built for agent workflows
5. **🌐 First-Mover** - No competition on ClawHub!

**[Buy on Gumroad - $4.99](https://gumroad.com)**

*💙 Love this project? Support us on Gumroad for the packaged version with one-click installation!*
