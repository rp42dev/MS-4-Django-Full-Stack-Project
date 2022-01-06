path = window.location.pathname

// show support message toast on hover
let messageIcons = document.querySelectorAll('.message-icon')

Array.prototype.filter.call(messageIcons, function (messageIcon) {
    messageIcon.addEventListener('mouseover', messageFunction)
}, false);


function messageFunction() {
    Array.prototype.filter.call(messageIcons, function (messageIcon) {
        messageIcon.removeEventListener("mouseover", messageFunction);
    }, false);
    
    toaster = document.querySelector('#message-toast');

    toaster.classList.remove('d-none');

    NewToast = new bootstrap.Toast(toaster);
    NewToast.show();

    toaster.addEventListener("hidden.bs.toast", function () {
        Array.prototype.filter.call(messageIcons, function (messageIcon) {
            messageIcon.addEventListener('mouseover', messageFunction)
        }, false);
    });
}