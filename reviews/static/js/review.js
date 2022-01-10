// get all Review Stars add class specified
// depending on range input based function below
function Stars(value) {
    starz = document.querySelectorAll('.starz');
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('active');
    for (let i = 0; i < value; i++)
        starz[i].classList.add('active')
}

// Review stars get start position and calculate
// mouse position to match range input 
// then add starr color class if mouse over
// I'm using invisible range input to 
// sellect rating based on 5 stars
const container = document.querySelector("#star");

// Validate review form
const button = document.querySelector('#review-submit');
const star = document.querySelector('#star');

// Disabled submit button
// enable on clicking stars element
button.disabled = true
star.addEventListener('click', function (){ 
    button.disabled = false
})

// Change star color baser on mouse position
container.addEventListener("mousemove", (e) => {
    let rect = container.getBoundingClientRect();
    xp = parseInt(((e.clientX - rect.left) / (rect.right - rect.left)) * 100)
    starz = document.querySelectorAll('.starz');
    if (xp <= 20) {
        value = 1
    } else if (xp <= 40) {
        value = 2
    } else if (xp <= 60) {
        value = 3
    } else if (xp <= 80) {
        value = 4
    } else {
        value = 5
    }
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('star_hover');
    for (let i = 0; i < value; i++)
        starz[i].classList.add('star_hover')
});

// Rmove color class when mouse out
container.addEventListener("mouseout", (e) => {
    // Do math
    starz = document.querySelectorAll('.starz');
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('star_hover');
});
