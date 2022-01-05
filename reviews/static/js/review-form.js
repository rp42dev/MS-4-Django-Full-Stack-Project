// Falidate review form
const form = document.querySelector('#review-submit')

form.addEventListener('submit', function (event) {
    let star = document.querySelector('#star')
    input.classList.remove('is-invalid')
    input.classList.remove('is-valid')
    if (star.value <= 0) {
        event.preventDefault()
        event.stopPropagation()
        star.nextSibling.classList.add('is-invalid')
    }

    form.classList.add('was-validated')
}, false)