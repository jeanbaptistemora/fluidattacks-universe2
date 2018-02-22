/*
Script to create a dropdown menu containing links to every
article of the main category clicked in the index of the KB.
If the category is clicked again, the menu disappears.
Used to improve the readability and presentation of the KB
articles.
*/

var hardenscat = document.getElementsByClassName("hardens-category");
var i;
for (i = 0; i < hardenscat.length; i++) {
  hardenscat[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var hardenspanel = this.nextElementSibling;
    if (hardenspanel.style.maxHeight){
      hardenspanel.style.maxHeight = null;
    } else {
      hardenspanel.style.maxHeight = hardenspanel.scrollHeight + "px";
    }
  });
}

$(document).ready(function () {
  var anchor = window.location.hash;
  if (anchor != "") {
    var span = document.getElementById(anchor.replace('#',''));
    var hardenscat = span.parentNode.parentNode;
    var hardenspanel = hardenscat.nextElementSibling;
    hardenscat.classList.toggle("active");
    if (hardenspanel.style.maxHeight){
      hardenspanel.style.maxHeight = null;
    } else {
      hardenspanel.style.maxHeight = hardenspanel.scrollHeight + "px";
    }
  }
});
