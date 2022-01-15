
 // side scrool function
 const scrolling = document.querySelector(".scroll-wrapper");

 console.log('working')
 let left= false;
 let right = false;
 
 document.querySelector('#left').addEventListener('mousedown', () => scrolling.scrollLeft += 300);
 document.querySelector("#right").addEventListener('mousedown', () => scrolling.scrollLeft -= 300);