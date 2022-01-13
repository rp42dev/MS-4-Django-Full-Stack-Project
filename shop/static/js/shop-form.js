// Get file inputs and add gray color css
// class to placeholder if file net sellected
var fileInputs = document.querySelectorAll('input[type=file]');
Array.prototype.filter.call(fileInputs, function (input) {
    input.classList.add('text-gray');
}, false);