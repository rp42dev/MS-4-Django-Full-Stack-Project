// Srool hide and unhide shop nav with help from here
// https://codepen.io/lehollandaisvolant/pen/ryrrGx

document.addEventListener("DOMContentLoaded", function(event) { 
    // https://stackoverflow.com/questions/17642872/refresh-page-and-keep-scroll-position
    // Maintain scrool position
        var scrollpos = localStorage.getItem('scrollpos');
        if (scrollpos) window.scrollTo(0, scrollpos);

    let st = 0;
    var shopNavbarShrink = function () {
        const shopNav = document.body.querySelector('#shop-nav');
        // Srool hide and unhide shop search bar
        let searchBody = document.querySelector('#search_body');
        if ((document.body.getBoundingClientRect()).top > st) {
            shopNav.classList.add('extra-navbar-grow');
            shopNav.classList.remove('extra-navbar-shrink');

        } else {
            searchBody.classList.add('search-shrink');
            searchBody.classList.remove('search-grow');
            shopNav.classList.add('extra-navbar-shrink');
            shopNav.classList.remove('extra-navbar-grow');
        }
        st = (document.body.getBoundingClientRect()).top;

    };

    document.addEventListener('scroll', shopNavbarShrink);

    // Show, hide search bar on click
    let searchIcons = document.querySelectorAll('.search_icon');
    var searchShrink = function () {
        let searchBody = document.querySelector('#search_body');
        let theClass = document.getElementsByClassName('search-shrink')[0];
        if (theClass) {
            searchBody.classList.add('search-grow');
            searchBody.classList.remove('search-shrink');
        } else {
            searchBody.classList.add('search-shrink');
            searchBody.classList.remove('search-grow');
        }
    };

    Array.prototype.filter.call(searchIcons, function (icon) {
        icon.addEventListener('click', searchShrink);
    }, false);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};
