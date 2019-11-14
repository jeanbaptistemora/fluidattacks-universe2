// Delighted snippet, get Email, Name and Company of the person being surveyed
var i;

function pushElement() {
  return function (e) {
    return function () {
      var t=Array.prototype.slice.call(arguments);
      i.push([e,t]);
    }
  }
}

!function(e,t,r,n,a){if(!e[a]){for(i=e[a]=[],s=0;s<r.length;s++){var c=r[s];i[c]=i[c]||pushElement()(c)}i.SNIPPET_VERSION="1.0.1";var o=t.createElement("script");o.type="text/javascript",o.async=!0,o.src="https://d2yyd1h5u9mauk.cloudfront.net/integrations/web/v1/library/"+n+"/"+a+".js";var p=t.getElementsByTagName("script")[0];p.parentNode.insertBefore(o,p)}}(window,document,["survey","reset","config","init","set","get","event","identify","track","page","screen","group","alias"],"C2IiXJX4CW06goZ8","delighted");
if(!userEmail.includes('fluidattacks.com')) {
	delighted.survey({
      email: userEmail,
      name: userName,
      properties: {
        company: userOrganization
      }
    });
}
