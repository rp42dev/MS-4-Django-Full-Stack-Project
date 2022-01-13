// get all Review Stars add class specified

// depending on range input value onchange function
// Add or remove star symbol color class 'active'
// based on input value from 1 to 5
// Recycle function each time input changes
function Stars(value) {
    let starz = document.querySelectorAll('.starz');
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('active');
    for (let i = 0; i < value; i++)
        starz[i].classList.add('active')
}

const container = document.querySelector("#star");

// Validate review form
const button = document.querySelector('#review-submit');
const star = document.querySelector('#star');

// Disabled submit button
// enable on clicking stars element
if (button){
   button.disabled = true;
}

star.addEventListener('click', function (){ 
    button.disabled = false;
});

// Change star color based on mouse position.
// to get user input value on click based from 1 tp 5.
// I'm using range input hidden on top of the star symbols.
// This enables to get user value for POST to the database.
container.addEventListener("mousemove", (e) => {
    // Get star container left and right positions
    // Calculate mouse possition from left screen side
    // To the rect left and right possitions on the screen
    let rect = container.getBoundingClientRect();
    let xp = parseInt(((e.clientX - rect.left) / (rect.right - rect.left)) * 100);
    let starz = document.querySelectorAll('.starz');
  	let value;
    // Conteiner width == 100% then devide it to 5 units
    if (xp <= 20) {
        value = 1;
    } else if (xp <= 40) {
        value = 2;
    } else if (xp <= 60) {
        value = 3;
    } else if (xp <= 80) {
        value = 4;
    } else {
        value = 5;
    }
    // Change star color based on mouse position
    // based on value calculations above
    // add for each value class 'star_hover' effect
    // Recycle the function to remove 'star_hover' class
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('star_hover');
    for (let i = 0; i < value; i++)
        starz[i].classList.add('star_hover');
});

// Remove color class when mouse out
container.addEventListener("mouseout", (e) => {
    // Do math
    let starz = document.querySelectorAll('.starz');
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('star_hover');
});