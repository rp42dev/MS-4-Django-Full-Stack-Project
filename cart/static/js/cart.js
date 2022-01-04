path = window.location.pathname

// show cart content toast on hover
// Do not show if on certain pages
if ( !(path === '/cart/' || path === '/checkout/') ) {
    let cartItems = [].slice.call(document.querySelectorAll('.cart'))
    cartItems.map(function (cart) {
        cart.addEventListener('mouseover', MyFunction)
    })
    function MyFunction() {
        cartItems.map(function (cart) {
            cart.removeEventListener("mouseover", MyFunction);
        })
        toaster = document.querySelector('#cart_toast');

        toaster.classList.remove('d-none');

        NewToast = new bootstrap.Toast(toaster);
        NewToast.show();

        toaster.addEventListener("hidden.bs.toast", function () {
            cartItems.map(function (cart) {
                cart.addEventListener('mouseover', MyFunction)
            })
        });
    }
}
