"""
Webhook Handler Example

This shows how to receive and process PayPal webhook notifications.
Use this as a starting point for your webhook endpoint.

Requirements:
    pip install flask
    
Usage:
    python webhook_handler.py
    
    # For local testing, use ngrok to expose your local server:
    # ngrok http 5000
    # Then set your PayPal webhook URL to: https://xxx.ngrok.io/webhooks/paypal
"""

from flask import Flask, request, jsonify
from paypal_agent import PayPalAgent
import json
import os

app = Flask(__name__)
paypal = PayPalAgent()

# In-memory store for received webhooks (use database in production!)
received_events = []


@app.route('/')
def index():
    """Simple status page"""
    return jsonify({
        "status": "PayPal Webhook Handler Running",
        "mode": paypal.mode,
        "received_events": len(received_events)
    })


@app.route('/webhooks/paypal', methods=['POST'])
def paypal_webhook():
    """
    PayPal webhook endpoint.
    
    PayPal will POST webhook events to this URL.
    """
    # Get raw body (important for signature verification!)
    raw_body = request.get_data()
    headers = dict(request.headers)
    
    # Log incoming webhook
    print(f"\n📥 Webhook received!")
    print(f"   Event Type: {request.headers.get('paypal-event-type', 'unknown')}")
    print(f"   Transmission ID: {request.headers.get('paypal-transmission-id', 'unknown')}")
    
    # Verify webhook signature (security!)
    if not paypal.verify_webhook(headers, raw_body):
        print("❌ Webhook signature verification failed!")
        # In production, you might want to reject unverified webhooks
        # return jsonify({"error": "Invalid signature"}), 400
        print("⚠️ Proceeding anyway (set PAYPAL_WEBHOOK_ID for verification)")
    else:
        print("✅ Webhook signature verified")
    
    # Parse and process webhook
    try:
        payload = request.get_json()
        result = paypal.handle_webhook(payload)
        
        # Store event
        received_events.append({
            "event_type": result['event_type'],
            "order_id": result.get('order_id'),
            "received_at": result.get('create_time'),
            "payload": payload
        })
        
        # Handle specific event types
        handle_event(result, payload)
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500


def handle_event(result: dict, payload: dict):
    """
    Handle different PayPal webhook event types.
    
    This is where you implement your business logic!
    """
    event_type = result['event_type']
    
    print(f"\n🔄 Processing event: {event_type}")
    
    if event_type == "CHECKOUT.ORDER.APPROVED":
        # Customer has approved the payment on PayPal
        print(f"   ✅ Order approved by customer")
        print(f"   📋 Order ID: {result.get('order_id')}")
        print(f"   👤 Payer: {result.get('payer_email')}")
        print(f"   💰 Amount: {result.get('amount')} {result.get('currency')}")
        
        # Auto-capture if desired
        # capture = paypal.capture_payment(result['order_id'])
        # print(f"   💳 Payment captured: {capture['capture_id']}")
        
        # TODO: Send confirmation email, update order status, etc.
        
    elif event_type == "PAYMENT.CAPTURE.COMPLETED":
        # Payment successfully captured!
        print(f"   ✅ Payment captured!")
        print(f"   📋 Capture ID: {result.get('capture_id')}")
        print(f"   💰 Amount: {result.get('amount')} {result.get('currency')}")
        
        # TODO: Fulfill the order, deliver product, activate service, etc.
        # send_order_confirmation(result.get('payer_email'), result)
        # activate_customer_account(result.get('custom_id'))
        
    elif event_type == "PAYMENT.CAPTURE.DENIED":
        # Payment was denied
        print(f"   ❌ Payment denied!")
        print(f"   📋 Capture ID: {result.get('capture_id')}")
        
        # TODO: Notify customer, update order status, etc.
        
    elif event_type == "PAYMENT.CAPTURE.REFUNDED":
        # Payment was refunded
        print(f"   ↩️ Payment refunded")
        print(f"   📋 Capture ID: {result.get('capture_id')}")
        
        # TODO: Update records, revoke access if needed, etc.
        
    elif event_type == "CHECKOUT.ORDER.VOIDED":
        # Order was cancelled
        print(f"   🚫 Order cancelled")
        print(f"   📋 Order ID: {result.get('order_id')}")
        
    else:
        print(f"   ℹ️ Unhandled event type: {event_type}")
        print(f"   Full payload logged")


@app.route('/webhooks/events', methods=['GET'])
def list_events():
    """List received webhook events (for debugging)"""
    return jsonify({
        "count": len(received_events),
        "events": received_events
    })


@app.route('/webhooks/events/clear', methods=['POST'])
def clear_events():
    """Clear event history (for debugging)"""
    received_events.clear()
    return jsonify({"status": "cleared"})


def send_order_confirmation(email: str, payment_details: dict):
    """
    Example: Send order confirmation email.
    
    In production, integrate with your email service:
    - SendGrid
    - Mailgun
    - AWS SES
    - etc.
    """
    print(f"\n📧 Sending confirmation to {email}")
    print(f"   Order: {payment_details.get('order_id')}")
    print(f"   Amount: {payment_details.get('amount')} {payment_details.get('currency')}")
    # TODO: Implement actual email sending


def activate_customer_account(customer_id: str):
    """
    Example: Activate customer account after payment.
    """
    print(f"\n🔓 Activating account for customer: {customer_id}")
    # TODO: Implement your activation logic


if __name__ == '__main__':
    print("=" * 60)
    print("PayPal Webhook Handler")
    print("=" * 60)
    print(f"\nMode: {paypal.mode}")
    print(f"Client ID: {paypal.client_id[:10]}...")
    print(f"Webhook ID: {paypal.webhook_id or 'Not configured (verification disabled)'}")
    
    print("\n📖 Endpoints:")
    print("   GET  /                    - Status check")
    print("   POST /webhooks/paypal     - PayPal webhook receiver")
    print("   GET  /webhooks/events     - List received events")
    print("   POST /webhooks/events/clear - Clear event history")
    
    print("\n🚀 Starting server on http://localhost:5000")
    print("\nFor local testing with PayPal webhooks:")
    print("   1. Install ngrok: npm install -g ngrok")
    print("   2. Run: ngrok http 5000")
    print("   3. Copy the HTTPS URL from ngrok")
    print("   4. Set it as your webhook URL in PayPal Developer Dashboard")
    print("   5. Subscribe to events: CHECKOUT.ORDER.APPROVED, PAYMENT.CAPTURE.COMPLETED")
    
    print("\nPress Ctrl+C to stop\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
