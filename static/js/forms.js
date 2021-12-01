(function () {
    'use strict';
    window.addEventListener('load', function () {
        // Fetch all the forms we want to apply custom validation styles
        var inputs = document.getElementsByClassName('form-control')
        // Loop over each input and watch blue event
        var validation = Array.prototype.filter.call(inputs, function (input) {

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
                    if (elem[0]) {
                        elem[0].remove()
                    }

                    // parent.childNodes[3].remove();
                    console.log(elem);
                }
            }, false);
        });
    }, false);
})()