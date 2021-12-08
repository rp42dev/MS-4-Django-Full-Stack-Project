(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom validation styles
        var inputs = document.querySelectorAll('.form-control')
        let file = document.querySelectorAll('.form-control-file')

        // Loop over each input and watch blue event
        var validation = Array.prototype.filter.call(inputs, function (input) {
            if (input.name === 'image') {
                file = input
                file.classList.add('text-gray')
            }
            input.addEventListener('blur', function (event) {
                // reset
                input.classList.remove('is-invalid')
                input.classList.remove('is-valid')

                if (input.checkValidity() === false) {
                    input.classList.add('is-invalid')
                    let parent = this.parentElement;
                    let elem = parent.getElementsByTagName('p')

                    if (elem[0]) {

                    } else {
                        var para = document.createElement("P");
                        para.classList.add('text-danger');
                        para.innerHTML = "This Field is Required.";
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
    }, false);
})()