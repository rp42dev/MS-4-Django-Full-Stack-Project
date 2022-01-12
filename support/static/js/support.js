// Support form validation
// Add gray color class to the form placeholders
// Add or remove product sellect option

function mainFunction() {
    let issue = document.querySelector('#id_support-issue');
    let item = document.querySelector('#sellect-product');
    let itemGroup = document.querySelector('#sellect-product-group')
    issue.addEventListener("change", myFuncIssue);
    item.addEventListener("change", myFuncItem);
    item.classList.add('text-gray');
    issue.classList.add('text-gray');

    // Add gray color class to the form placeholders
    function myFuncItem() {
        if (this.value == '') {
            this.classList.add('text-gray');
        } else {
            this.classList.remove('text-gray');
        }
    }

    // Add product sellect option if option is product
    function myFuncIssue() {
        if (this.value == 'Product') {
            itemGroup.classList.remove('d-none');
            itemGroup.classList.add('d-block');
        } else {
            itemGroup.classList.add('d-none');
            itemGroup.classList.remove('d-block');
        }
        if (this.value == 'Select') {
            this.classList.add('text-gray');
        } else {
            this.classList.remove('text-gray');
        }
    }
}

// Add gray color class to the form placeholders
function supportFunction(){
    let issue = document.querySelector('#id_support-issue')
    issue.addEventListener("change", myFuncIssue);
    issue.classList.add('text-gray');

    function myFuncIssue() {
        if (this.value == 'Select') {
            this.classList.add('text-gray');
        } else {
            this.classList.remove('text-gray');
        }
    }
}

// Do not show if on certain pages
if (path === '/support/') {
    supportFunction();
} else {
    mainFunction();
}
