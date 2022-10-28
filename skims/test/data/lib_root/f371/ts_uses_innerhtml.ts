const rootDiv = document.getElementById('root');
const hash = decodeURIComponent(location.hash.substr(1));
if (rootDiv != null){
  rootDiv.innerHTML = hash;
}
