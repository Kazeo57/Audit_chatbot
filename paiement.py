import streamlit as st
import stripe
import os

# Stripe API key (Use your own keys from environment variables)
#stripe.api_key = os.getenv('STRIPE_API_KEY')
stripe.api_key="sk_test_51Pbk0qRv6eny3negpQrV8teSu3idY3aMzwAT6fhAxXuhFoYKBpqD8xL49PBX4jbkT8CGcMuZ5Whtyl1sB7h896Q90006gtYpG5"
# Check if the API key is set
if not stripe.api_key:
    st.error("Error: Stripe API key is not set.")
    st.stop()

# Configure the Streamlit page
st.title("Payment Page")
st.write("Please proceed with the payment to access the chatbot.")

try:
    # Create a Stripe payment session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Chatbot Access',
                },
                'unit_amount': 1000,  # Price in cents (10.00 USD)
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://auditchatbot-a8bczsbmrpnh947u7mvkrc.streamlit.app/?success=true',  # Redirect here after payment
        cancel_url='https://auditchatbot-a8bczsbmrpnh947u7mvkrc.streamlit.app/?cancel=true',   # Redirect here if payment is canceled
    )
    
    # Display the payment button
    if st.button('Pay'):
        # Redirect to the Stripe checkout session URL
        st.markdown(f'<a href="{session.url}" target="_blank">Pay now</a>', unsafe_allow_html=True)

except stripe.error.StripeError as e:
    st.error(f"Stripe error: {str(e)}")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

# Handle success and cancel pages
query_params = st.query_params
if "success" in query_params:
    st.success("Payment successful! You will be redirected to the chatbot.")
    st.markdown(f"[Access the Chatbot](https://auditchatbot-a8bczsbmrpnh947u7mvkrc.streamlit.app/)", unsafe_allow_html=True)

if "cancel" in query_params:
    st.error("Payment canceled. Please try again.")
