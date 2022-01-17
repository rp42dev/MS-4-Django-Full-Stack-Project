// Header paralax scrool effect
window.addEventListener('load', (event) => {
  window.addEventListener('scroll', parallax);
  function parallax() {
    var scrolled = window.pageYOffset;
    var parallax2 = document.querySelector(".parallax2");
    var scrool2 = (scrolled * 0.4) + 'px';
    parallax2.style.transform = 'translateY(' + scrool2 + ')';
  }
});