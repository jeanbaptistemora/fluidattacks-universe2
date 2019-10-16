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
