/*
Script to create a dropdown menu containing links to every
article of the main category clicked in the index of the KB.
If the category is clicked again, the menu disappears.
Used to improve the readability and presentation of the KB
articles.
*/


var defendscat = document.getElementsByClassName("defends-category");
var i;
for (i = 0; i < defendscat.length; i++) {
  defendscat[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var defendspanel = this.nextElementSibling;
    if (defendspanel.style.maxHeight){
      defendspanel.style.maxHeight = null;
    } else {
      defendspanel.style.maxHeight = "fit-content";
    }
  });
}

// Function to activate menu when redirected with an URL cotaining an anchor
$(document).ready(function () {
  var anchor = window.location.hash;
  if (anchor != "") {
    var span = document.getElementById(anchor.replace('#',''));
    var defendscat = span.parentNode.parentNode;
    var defendspanel = defendscat.nextElementSibling;
    defendscat.classList.toggle("active");
    if (defendspanel.style.maxHeight){
      defendspanel.style.maxHeight = null;
    } else {
      defendspanel.style.maxHeight = "fit-content";
    }
  }
});
