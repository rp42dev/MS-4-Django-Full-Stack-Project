// Maintain scroll position
// https://stackoverflow.com/questions/17642872/refresh-page-and-keep-scroll-position

document.addEventListener("DOMContentLoaded", function (event) {
    var scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos) {
        window.scrollTo(0, scrollpos);
        localStorage.removeItem('scrollpos');
    } 
});

function setPos() {
    window.onbeforeunload = function (e) {
        localStorage.setItem('scrollpos', window.scrollY);
    };
}
