window.addEventListener('DOMContentLoaded', event => {
    let FormToast = document.querySelector('#form-error')

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
        if (window.location.pathname === '/') {
            if (window.scrollY < 350) {
                navbarCollapsible.classList.remove('transparent-none');
                navbarCollapsible.classList.add('transparent-bg');
            } else {
                navbarCollapsible.classList.remove('transparent-bg');
                navbarCollapsible.classList.add('transparent-none');
            }
        } else {

            if (window.scrollY === 0) {
                navbarCollapsible.classList.remove('navbar-shrink')

            } else {
                navbarCollapsible.classList.add('navbar-shrink')
            }
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

    let st = 0;
    var goUpFunc = function () {
        const goUp = document.body.querySelector('#go_up_active');
        const feature = document.body.querySelector('#feture');
        // Srool hide and unhide shop search bar
        if (window.scrollY === 0) {
            feature.classList.remove('feature-shrink');
            feature.classList.add('feature-grow');

        } else {
            feature.classList.remove('feature-grow');
            feature.classList.add('feature-shrink');

        }

        if ((document.body.getBoundingClientRect()).top > st) {
            goUp.classList.remove('go_up');
            goUp.classList.add('go_up_active');


        } else {
            goUp.classList.add('go_up');
            goUp.classList.remove('.go_up_active');

        }
        st = (document.body.getBoundingClientRect()).top;

    };

    document.addEventListener('scroll', goUpFunc);

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