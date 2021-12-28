// Stripe elements
// Get stripe public and client keys
const stripe_public_key = document.querySelector('#id_stripe_public_key').innerText.slice(1, -1);
const client_secret = document.querySelector('#id_client_secret').innerText.slice(1, -1);

// The items the customer wants to buy
const stripe = Stripe(stripe_public_key);

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
        border: '1px solid #d2042d',
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

var form = document.getElementById("payment-form");
form.addEventListener("submit", function (event) {
    event.preventDefault();
    // Complete payment when the submit button is clicked
    payWithCard(stripe, card, data.clientSecret);
});