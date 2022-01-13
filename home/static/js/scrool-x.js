
const scrolling = document.querySelector(".scroll-wrapper");
scrolling.scrollLeft = 130;
// side scrool function

let left= false;
let right = false;

document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft += 300);

document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft -= 300);
