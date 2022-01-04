window.addEventListener('DOMContentLoaded', event => {
    let FormToast = document.querySelector('#form-error')
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

    // Show / autohide bootstarp toasts
    var toasts = function () {
        var toastElList = [].slice.call(document.querySelectorAll('.toast'))
        var toastList = toastElList.map(function (toastEl) {
            return new bootstrap.Toast(toastEl)
        })
        toastList.forEach(toast => toast.show());
    }
    toasts();

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }
    };

    // Shrink the navbar 
    navbarShrink();
    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);
    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            offset: 74,
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});