var kbcat = document.getElementsByClassName("kb-category");
var i;
for (i = 0; i < kbcat.length; i++) {
  kbcat[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var kbpanel = this.nextElementSibling;
    if (kbpanel.style.maxHeight){
      kbpanel.style.maxHeight = null;
    } else {
      kbpanel.style.maxHeight = kbpanel.scrollHeight + "px";
    }
  });
}

$(document).ready(function () {
  var anchor = window.location.hash;
  if (anchor != "") {
    var span = document.getElementById(anchor.replace('#',''));
    var kbcat = span.parentNode.parentNode;
    var kbpanel = kbcat.nextElementSibling;
    kbcat.classList.toggle("active");
    if (kbpanel.style.maxHeight){
      kbpanel.style.maxHeight = null;
    } else {
      kbpanel.style.maxHeight = kbpanel.scrollHeight + "px";
    }
  }
});
