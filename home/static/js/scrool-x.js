
// side scrool function
window.addEventListener('load', (event) => {

    const scrolling = document.querySelector(".scroll-wrapper");
    scrolling.scrollLeft = 130;
    scrolling.addEventListener("wheel", (evt) => {
        evt.preventDefault();
        scrolling.scrollLeft += evt.deltaY;
    });
});