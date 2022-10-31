// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

let securityHeaders = {
  "Content-Security-Policy" : "script-src "
                              + "'self' "
                              + "'unsafe-inline' "
                              + "'unsafe-eval' "
                              + "fluidattacks.matomo.cloud "
                              + "googleads.g.doubleclick.net/pagead/viewthroughconversion/ "
                              + "script.hotjar.com "
                              + "snap.licdn.com "
                              + "static.hotjar.com "
                              + "www.google-analytics.com/analytics.js "
                              + "www.googleadservices.com/pagead/conversion_async.js "
                              + "www.googletagmanager.com/gtm.js "
                              + "www.googletagmanager.com/gtag/js "
                              + "*.cloudflareinsights.com; "
                              + "frame-ancestors "
                              + "'self'; "
                              + "object-src "
                              + "'none'; "
                              + "upgrade-insecure-requests;",
  "Strict-Transport-Security" : "max-age=31536000",
  "X-Xss-Protection" : "0",
  "X-Frame-Options" : "DENY",
  "X-Content-Type-Options" : "nosniff",
  "X-Permitted-Cross-Domain-Policies": "none",
  "Referrer-Policy" : "strict-origin-when-cross-origin",
  "Permissions-Policy" : "geolocation=(self), "
                         + "midi=(self), "
                         + "push=(self), "
                         + "sync-xhr=(self), "
                         + "microphone=(self), "
                         + "camera=(self), "
                         + "magnetometer=(self), "
                         + "gyroscope=(self), "
                         + "speaker=(self), "
                         + "vibrate=(self), "
                         + "fullscreen=(self), "
                         + "payment=(self)",
}

const homeURL = "https://docs.fluidattacks.com/";
const redirectMap = new Map([
  ["/criteria/compliance/owaspten/", homeURL,],
  ["/criteria/compliance/owaspten", homeURL,],
  ["/criteria/source/345/", homeURL,],
  ["/criteria/source/345", homeURL,],
  ["/types/", homeURL,],
  ["/types", homeURL,],
  ["/assets/images/common-arch.dot-23d1c323fd7c4dec12982d13779cfc60.svg/", "https://docs.fluidattacks.com/development/common/"],
  ["/assets/images/common-arch.dot-23d1c323fd7c4dec12982d13779cfc60.svg", "https://docs.fluidattacks.com/development/common/"],
]);

let sanitiseHeaders = {}

let removeHeaders = [
  "Public-Key-Pins",
]

addEventListener('fetch', event => {
  event.respondWith(addHeaders(event.request))
})

async function addHeaders(req) {
  let response = await fetch(req)
  let newHdrs = new Headers(response.headers)

  const requestURL = new URL(response.url);
  const path = requestURL.pathname;
  const location = redirectMap.get(path);

  if (location) {
    return Response.redirect(location, 301);
  }

  if (newHdrs.has("Content-Type") && !newHdrs.get("Content-Type").includes("text/html")) {
    return new Response(response.body , {
      status: response.status,
      statusText: response.statusText,
      headers: newHdrs
    })
  }

  Object.keys(securityHeaders).forEach((name) => {
    newHdrs.set(name, securityHeaders[name]);
  });

  Object.keys(sanitiseHeaders).forEach((name) => {
    newHdrs.set(name, sanitiseHeaders[name]);
  });

  removeHeaders.forEach(function(name){
    newHdrs.delete(name)
  })

  return new Response(response.body , {
    status: response.status,
    statusText: response.statusText,
    headers: newHdrs
  })
}
