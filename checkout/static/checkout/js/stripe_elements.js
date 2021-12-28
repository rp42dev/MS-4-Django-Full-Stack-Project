// Stripe elements
// Get stripe public and client keys
const stripePublicKey = document.querySelector('#id_stripe_public_key').innerText.slice(1, -1);
const clientSecret = document.querySelector('#id_client_secret').innerText.slice(1, -1);

// The items the customer wants to buy
const stripe = Stripe(stripePublicKey);

// Disable the button until we have Stripe set up on the page
document.querySelector("button").disabled = true;

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

var card = elements.create("card", {
    style: style
});
// Stripe injects an iframe into the DOM
card.mount("#card-element");

card.on("change", function (event) {
    // Disable the Pay button if there are no card details in the Element
    document.querySelector("button").disabled = event.empty;
    document.querySelector("#card-error").textContent = event.error ? event.error.message : "";
});

var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({
        'disabled': true
    });
    document.querySelector('#btn-submit').disabled = true;
    // If the client secret was rendered server-side as a data-secret attribute
    // on the <form> element, you can retrieve it here by calling `form.dataset.secret`
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: 'Jenny Rosen'
            }
        }
    }).then(function (result) {
        if (result.error) {
            // Show error to your customer (for example, insufficient funds)
            document.querySelector("#card-error").textContent = result.error ? result.error.message : "";
            card.update({
                'disabled': false
            });
            document.querySelector('#submit').disabled = false;
        } else {
            // The payment has been processed!
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});