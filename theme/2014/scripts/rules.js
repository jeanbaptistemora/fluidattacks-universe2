// This script creates a dropdown menu in rules index
// similar to Defends

var rulescat = document.getElementsByClassName("rulescat");
for (var i = 0; i < rulescat.length; i++ ){
  rulescat[i].addEventListener("click", function() {
    this.classList.toggle("bg-fluid-lightgray");
    this.children[1].classList.toggle("rotate-90");
    var ruleslist = this.nextElementSibling;
    ruleslist.classList.toggle("dn");
  });
}

//Activate the list when the category is referenced through the url
$(document).ready(function () {
  var anchor = window.location.hash;
  if (anchor != "") {
    var span = document.getElementById(anchor.replace('#',''));
    var category = span.parentNode.parentNode;
    category.classList.toggle("bg-fluid-lightgray");
    category.children[1].classList.toggle("rotate-90");
    var list = category.nextElementSibling;
    list.classList.toggle("dn");
  }
});
