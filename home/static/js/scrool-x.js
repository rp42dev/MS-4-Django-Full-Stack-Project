 // side scrool function
const scrolling = document.querySelector(".scroll-wrapper");


if (window.innerWidth < 400) {
    scrolling.scrollLeft = 80;
}

let left= false;
let right = false;

document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft += 300);
document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft -= 300);
