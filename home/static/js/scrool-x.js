
const scrolling = document.querySelector(".scroll-wrapper");

// side scrool function
let left= false;
let right = false;

document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft -= 250);
document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft += 250);
