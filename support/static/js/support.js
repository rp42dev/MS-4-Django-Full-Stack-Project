// <!-- onchange="myFunc(this.value)" -->
path = window.location.pathname
// Do not show if on certain pages
if (path === '/support/') {
    let issue = document.querySelector('#id_support-issue')
    issue.addEventListener("change", myFuncIssue);
    issue.classList.add('text-gray')

    function myFuncIssue() {
        if (issue.value == 'Select') {
            issue.classList.add('text-gray')
        } else {
            issue.classList.remove('text-gray')
        }
    }
} else {
    let issue = document.querySelector('#id_support-issue')
    let item = document.querySelector('#sellect-product')
    let itemGroup = document.querySelector('#sellect-product-group')
    issue.addEventListener("change", myFuncIssue);
    item.addEventListener("change", myFuncItem);
    item.classList.add('text-gray')
    issue.classList.add('text-gray')

    checkSelected()

    function myFuncItem() {
        if (item.value == '') {
            item.classList.add('text-gray')
        } else {
            item.classList.remove('text-gray')
        }
    }

    function myFuncIssue() {
        if (issue.value == 'Product') {
            itemGroup.classList.remove('d-none')
            itemGroup.classList.add('d-block')
        } else {
            itemGroup.classList.add('d-none')
            itemGroup.classList.remove('d-block')
        }
        if (issue.value == 'Select') {
            issue.classList.add('text-gray')
        } else {
            issue.classList.remove('text-gray')
        }
    }
}