window.addEventListener('scroll', parallax);

function parallax() {
  var scrolled = window.pageYOffset;
  var parallax = document.querySelector(".parallax");
  var parallax2 = document.querySelector(".parallax2");
  var scrool = (scrolled * 0.7) + 'px'
  parallax.style.transform = 'translateY(' + scrool + ')';
  var scrool2 = (scrolled * 0.4) + 'px'
  parallax2.style.transform = 'translateY(' + scrool2 + ')';
};