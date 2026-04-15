"""
Example: PayPal Payment Agent Usage

This file demonstrates various ways to use the PayPal Payment Agent.
Copy and adapt these examples for your use case.
"""

from paypal_agent import PayPalAgent
import time


def example_create_payment_link():
    """Example 1: Create a simple payment link"""
    print("=" * 50)
    print("Example 1: Create Payment Link")
    print("=" * 50)
    
    paypal = PayPalAgent()
    
    link = paypal.create_payment_link(
        amount="29.99",
        currency="USD",
        description="AI Consultation Service - 1 Hour",
        product_name="1-Hour AI Consultation",
        custom_id="ORDER-12345"
    )
    
    print(f"✅ Order ID: {link['order_id']}")
    print(f"🔗 Payment URL: {link['url']}")
    print(f"💰 Amount: {link['amount']} {link['currency']}")
    print(f"📋 Status: {link['status']}")
    
    return link


def example_check_payment_status(order_id: str):
    """Example 2: Check payment status"""
    print("\n" + "=" * 50)
    print("Example 2: Check Payment Status")
    print("=" * 50)
    
    paypal = PayPalAgent()
    status = paypal.check_payment_status(order_id)
    
    print(f"📊 Order ID: {status['order_id']}")
    print(f"📊 Status: {status['status']}")
    print(f"💰 Amount: {status.get('amount')} {status.get('currency')}")
    
    if status.get('payer_email'):
        print(f"👤 Payer: {status['payer_name']} ({status['payer_email']})")
    
    return status


def example_full_payment_flow():
    """Example 3: Complete payment flow with polling"""
    print("\n" + "=" * 50)
    print("Example 3: Full Payment Flow")
    print("=" * 50)
    
    paypal = PayPalAgent()
    
    # Step 1: Create payment
    link = paypal.create_payment_link(
        amount="99.00",
        currency="USD",
        product_name="Premium AI Agent Setup",
        description="Complete AI agent configuration and deployment",
        custom_id="PROJECT-ABC-123"
    )
    
    print(f"✅ Payment link created!")
    print(f"🔗 {link['url']}")
    print(f"📋 Order ID: {link['order_id']}")
    print("\n👉 Send this link to your customer!")
    
    # Step 2: Poll for payment (in real app, use webhooks)
    print("\n⏳ Polling for payment (Ctrl+C to skip)...")
    try:
        for i in range(60):  # Check for 5 minutes
            status = paypal.check_payment_status(link['order_id'])
            
            if status['status'] == 'APPROVED':
                print(f"\n✅ Payment approved by customer!")
                print("💳 Capturing payment...")
                
                capture = paypal.capture_payment(link['order_id'])
                print(f"✅ Payment captured!")
                print(f"   Capture ID: {capture['capture_id']}")
                print(f"   Net Amount: {capture['net_amount']}")
                print(f"   Fee: {capture['fee']}")
                break
                
            elif status['status'] == 'VOIDED':
                print(f"\n❌ Payment cancelled by customer")
                break
            elif status['status'] == 'COMPLETED':
                print(f"\n✅ Payment already completed!")
                break
            
            print(f"   Status: {status['status']}... (checking again in 5s)")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n⚠️ Polling interrupted")
    
    return link


def example_create_invoice_style():
    """Example 4: Create invoice-style payment"""
    print("\n" + "=" * 50)
    print("Example 4: Invoice-Style Payment")
    print("=" * 50)
    
    paypal = PayPalAgent()
    
    # Invoice-style with business branding
    link = paypal.create_payment_link(
        amount="499.00",
        currency="USD",
        product_name="Custom AI Automation System",
        description="Full-stack AI automation with OpenClaw integration",
        brand_name="Jiao Factory AI",
        custom_id="INV-2024-001"
    )
    
    print(f"✅ Invoice created!")
    print(f"🔗 {link['url']}")
    print(f"📧 Send this link to your client")
    
    return link


def example_multi_currency():
    """Example 5: Multi-currency support"""
    print("\n" + "=" * 50)
    print("Example 5: Multi-Currency Payments")
    print("=" * 50)
    
    paypal = PayPalAgent()
    
    currencies = [
        ("29.99", "USD", "US Customer"),
        ("24.99", "EUR", "EU Customer"),
        ("21.99", "GBP", "UK Customer"),
        ("3999", "JPY", "Japan Customer"),
    ]
    
    for amount, currency, customer in currencies:
        link = paypal.create_payment_link(
            amount=amount,
            currency=currency,
            product_name="AI Service",
            description=f"Service for {customer}"
        )
        print(f"  {currency}: {amount} - {link['url'][:60]}...")


def example_list_recent_transactions():
    """Example 6: List recent transactions"""
    print("\n" + "=" * 50)
    print("Example 6: Recent Transactions")
    print("=" * 50)
    
    paypal = PayPalAgent()
    transactions = paypal.list_recent_payments(limit=5)
    
    if transactions:
        for tx in transactions:
            info = tx.get('transaction_info', {})
            print(f"  {info.get('transaction_id')}: "
                  f"{info.get('transaction_amount', {}).get('value')} "
                  f"{info.get('transaction_amount', {}).get('currency_code')} - "
                  f"{info.get('transaction_status')}")
    else:
        print("  No recent transactions found")


if __name__ == "__main__":
    print("PayPal Payment Agent - Usage Examples")
    print("=" * 50)
    print("\nMake sure you have set these environment variables:")
    print("  - PAYPAL_CLIENT_ID")
    print("  - PAYPAL_CLIENT_SECRET")
    print("  - PAYPAL_MODE (sandbox or live)")
    print()
    
    try:
        # Run examples
        link = example_create_payment_link()
        example_check_payment_status(link['order_id'])
        # example_full_payment_flow()  # Uncomment to test full flow
        example_create_invoice_style()
        example_multi_currency()
        example_list_recent_transactions()
        
        print("\n" + "=" * 50)
        print("All examples completed! ✅")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure your PayPal credentials are configured correctly.")
