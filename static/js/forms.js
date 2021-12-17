(function () {
    'use strict'

    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    var forms = document.querySelectorAll('form')

    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    FormTrigger()
                    event.preventDefault()
                    event.stopPropagation()
                    let star = document.querySelector('#star')
                }

                form.classList.add('was-validated')
            }, false)
        })
})()

function FormTrigger() {
    // Fetch all the forms we want to apply custom validation styles
    var inputs = document.querySelectorAll('.form-control')
    let file = document.querySelectorAll('.form-control-file')
    
    // Loop over each input and watch blue event
    var validation = Array.prototype.filter.call(inputs, function (input) {
        // Image input gray placeholder
        if (input.name === 'image') {
            file = input
            file.classList.add('text-gray')
        }
        input.addEventListener('blur', function (event) {
            // reset
            input.classList.remove('is-invalid')
            input.classList.remove('is-valid')
            //Display required message if not valid
            if (input.checkValidity() === false) {
                input.classList.add('is-invalid')
                let parent = this.parentElement;
                let elem = parent.getElementsByTagName('p')

                if (elem[0]) {

                } else {
                    var para = document.createElement("P");
                    para.classList.add('text-danger');
                    let str = `${input.placeholder} Field is Required.`
                    para.innerHTML = str;
                    parent.append(para);
                }

            } else {
                input.classList.add('is-valid')
                let parent = this.parentElement;
                let elem = parent.getElementsByTagName('p')
                file.classList.remove('text-gray')
                if (elem[0]) {
                    elem[0].remove()
                }
            }
        }, false);
    });
}