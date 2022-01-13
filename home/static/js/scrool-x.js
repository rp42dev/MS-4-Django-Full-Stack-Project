
// scrool horisontal
if (window.scrollY > 300) {
const scrolling = document.querySelector(".scroll-wrapper");
scrolling.scrollLeft = 130;
scrolling.addEventListener("wheel", (evt) => {
    evt.preventDefault();
    scrolling.scrollLeft += evt.deltaY;
});
}