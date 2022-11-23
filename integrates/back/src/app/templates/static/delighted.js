// Delighted snippet, get Email, Name and Company of the person being surveyed
let i;

function pushElement() {
  return function (e) {
    return function () {
      let t = Array.prototype.slice.call(arguments);
      i.push([e, t]);
    }
  }
}

function delightedExecute(e, t, r, n, a) {
  if (!e[a]) {
    i = e[a] = []
    for (let c of r) {
      i[c] = i[c] || pushElement()(c) } i.SNIPPET_VERSION = "1.0.1";
      let o = t.createElement("script");
      o.type = "text/javascript";
      o.async = !0;
      o.src = "https://d2yyd1h5u9mauk.cloudfront.net/integrations/web/v1/library/" + n + "/" + a + ".js";
      let p = t.getElementsByTagName("script")[0];
      p.parentNode.insertBefore(o, p)
    }
  }

delightedExecute(window, document,
  ["survey", "reset", "config", "init", "set", "get",
  "event", "identify", "track", "page", "screen", "group", "alias"],
  "C2IiXJX4CW06goZ8", "delighted"
);
