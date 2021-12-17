function Stars(value) {
    starz = document.querySelectorAll('.starz');
    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('active');
    for (let i = 0; i < value; i++)
        starz[i].classList.add('active')
}

const container = document.querySelector("#star");
let rect = container.getBoundingClientRect();

container.addEventListener("mousemove", (e) => {

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
container.addEventListener("mouseout", (e) => {
    // Do math
    starz = document.querySelectorAll('.starz');

    for (let i = 0; i < 5; i++)
        starz[i].classList.remove('star_hover');

});