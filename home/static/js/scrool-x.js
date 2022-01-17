
 // side scrool function

// Maintain scrool position
// https://stackoverflow.com/questions/17642872/refresh-page-and-keep-scroll-position

 document.addEventListener("DOMContentLoaded", function(event) { 
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) window.scrollTo(0, scrollpos);

    const scrolling = document.querySelector(".scroll-wrapper");

    let left= false;
    let right = false;
    
    document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft += 300);
    document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft -= 300);
});

window.onbeforeunload = function(e) {
    localStorage.setItem('scrollpos', window.scrollY);
};
