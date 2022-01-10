// Support form validation
// Add gray color class to the form placeholders
// Add or remove product sellect option

let path = window.location.pathname;

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
        if (item.value == '') {
            item.classList.add('text-gray');
        } else {
            item.classList.remove('text-gray');
        }
    }

    // Add or remove product sellect option
    function myFuncIssue() {
        if (issue.value == 'Product') {
            itemGroup.classList.remove('d-none');
            itemGroup.classList.add('d-block');
        } else {
            itemGroup.classList.add('d-none');
            itemGroup.classList.remove('d-block');
        }
        if (issue.value == 'Select') {
            issue.classList.add('text-gray');
        } else {
            issue.classList.remove('text-gray');
        }
    }
}

// Add gray color class to the form placeholders
function supportFunction(){
    let issue = document.querySelector('#id_support-issue')
    issue.addEventListener("change", myFuncIssue);
    issue.classList.add('text-gray');

    function myFuncIssue() {
        if (issue.value == 'Select') {
            issue.classList.add('text-gray');
        } else {
            issue.classList.remove('text-gray');
        }
    }
}

// Do not show if on certain pages
if (path === '/support/') {
    supportFunction();
} else {
    mainFunction();
}
