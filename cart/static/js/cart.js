
// show cart content toast on hover
function outerFunction(){
  let cartItems = [].slice.call(document.querySelectorAll('.cart'));
    cartItems.map(function (cart) {
        cart.addEventListener('mouseover', MyFunction);
    });

    // If mouse over disable moureover listener
    // Enable mouseover once mouse leaves the cart icon
    function MyFunction() {
        cartItems.map(function (cart) {
            cart.removeEventListener("mouseover", MyFunction);
        });
        let toaster = document.querySelector('#cart_toast');

        toaster.classList.remove('d-none');

        let NewToast = new bootstrap.Toast(toaster);
        NewToast.show();

        toaster.addEventListener("hidden.bs.toast", function () {
            cartItems.map(function (cart) {
                cart.addEventListener('mouseover', MyFunction);
            });
        });
    }
 }
 
// Do not show on cart and checkout pages
let path = window.location.pathname;

if ( !(path === '/cart/' || path === '/checkout/') ) {
    outerFunction();
}