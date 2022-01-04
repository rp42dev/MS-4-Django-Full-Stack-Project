path = window.location.pathname

// show support message toast on hover
let messageIcon = document.querySelector('#message-icon')
messageIcon.addEventListener('mouseover', messageFunction)

function messageFunction() {
    messageIcon.removeEventListener("mouseover", messageFunction);
  
    toaster = document.querySelector('#message-toast');

    toaster.classList.remove('d-none');

    NewToast = new bootstrap.Toast(toaster);
    NewToast.show();

    toaster.addEventListener("hidden.bs.toast", function () {
        messageIcon.addEventListener('mouseover', messageFunction)

    });
}