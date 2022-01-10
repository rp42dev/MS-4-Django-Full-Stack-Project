// Stripe elements
// Get stripe public and client keys
const stripePublicKey = document.querySelector('#id_stripe_public_key').innerText.slice(1, -1);
const clientSecret = document.querySelector('#id_client_secret').innerText.slice(1, -1);

// The items the customer wants to buy
const stripe = Stripe(stripePublicKey);

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

// Stripe element styling
var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        fontFamily: 'Montserrat, sans-serif',
        fontWeight: '600',
        fontSmoothing: "antialiased",
        fontSize: "14px",
        "::placeholder": {
            color: "#c5c5c5"
        },
    },
    invalid: {
        fontFamily: 'Montserrat, sans-serif',
        color: "#d2042d",
        iconColor: "#d2042d",
    }
};

// create card element
var card = elements.create("card", {
    style: style
});

// Stripe injects an iframe into the DOM
card.mount("#card-element");

card.on("change", function (event) {
    // Disable the Pay button if there are no card details in the Element
    document.querySelector("#btn-submit").disabled = event.empty;
    document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
});

const form = document.getElementById('payment-form');
// event Listener for submit button
form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        setLoading(true);
        
        // Add shippind and billing form delails
        if (form.checkValidity()) {
        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: card,
                billing_details: {
                    name: form.elements['contact-full_name'].value,
                    email: form.elements['contact-email'].value,
                }
            },
            shipping: {
                name: form.elements['shipping-shipping_name'].value,
                address: {
                    line1: form.elements['shipping-address_line_1'].value,
                    line2: form.elements['shipping-address_line_2'].value,
                    city: form.elements['shipping-city'].value,
                    state: form.elements['shipping-county'].value,
                    postal_code: form.elements['shipping-postcode'].value,
                    country: form.elements['shipping-country'].value,
                }
            },
        
        }).then(function (result) {
            if (result.error) {
                // Show error to your customer (for example, insufficient funds)
                document.querySelector("#card-error").textContent = result.error ? result.error.message : "";
            } else {
                // The payment has been processed!
                if (result.paymentIntent.status === 'succeeded') {
                    form.submit();
                }
            }
            setLoading(false);
        });
    } else {
        setLoading(false);
    }
    });

// Show a spinner on payment submission
function setLoading(isLoading) {
    if (isLoading) {
        // Disable the button and show a spinner
        document.querySelector("#btn-submit").disabled = true;
        document.querySelector("#spinner").classList.remove("hidden");
        document.querySelector("#button-text").classList.add("hidden");
    } else {
        document.querySelector("#btn-submit").disabled = false;
        document.querySelector("#spinner").classList.add("hidden");
        document.querySelector("#button-text").classList.remove("hidden");
    }
}