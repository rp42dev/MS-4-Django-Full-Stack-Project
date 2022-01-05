// Srool hide and unhide shop nav with help from here
// https://codepen.io/lehollandaisvolant/pen/ryrrGx
let st = 0;

var shopNavbarShrink = function () {
    const shopNav = document.body.querySelector('#shop-nav')

    if ((document.body.getBoundingClientRect()).top > st){
        shopNav.classList.add('extra-navbar-grow')
        shopNav.classList.remove('extra-navbar-shrink')
    } else {
        shopNav.classList.add('extra-navbar-shrink')
        shopNav.classList.remove('extra-navbar-grow')
    }
    st = (document.body.getBoundingClientRect()).top;
};

// Shrink the navbar when page is scrolled
document.addEventListener('scroll', shopNavbarShrink);

const searchIcon = document.querySelector('#search_icon')

// Srool hide and unhide shop searck bar

var searchShrink = function () {
    console.log('here')
    let = searchBody = document.querySelector('#search_body')
    let theClass = document.getElementsByClassName('search-shrink')[0]
    if (theClass){
        console.log('here')
        searchBody.classList.add('search-grow')
        searchBody.classList.remove('search-shrink')
    } else {
        searchBody.classList.add('search-shrink')
        searchBody.classList.remove('search-grow')
    }
};

// Shrink the navbar when page is scrolled
searchIcon.addEventListener('click', searchShrink);