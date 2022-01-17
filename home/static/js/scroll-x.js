
// side scroll function

document.addEventListener("DOMContentLoaded", function (event) {

    const scrolling = document.querySelector(".scroll-wrapper");

    let left = false;
    let right = false;

    document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft += 300);
    document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft -= 300);
});

