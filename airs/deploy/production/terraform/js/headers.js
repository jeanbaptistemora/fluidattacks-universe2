let securityHeaders = {
  "Content-Security-Policy" : "upgrade-insecure-requests",
  "Strict-Transport-Security" : "max-age=31536000",
  "X-Xss-Protection" : "1; mode=block",
  "X-Frame-Options" : "DENY",
  "X-Content-Type-Options" : "nosniff",
  "Referrer-Policy" : "strict-origin-when-cross-origin",
  "Permissions-Policy" : "geolocation=(self), \
                          midi=(self), \
                          push=(self), \
                          sync-xhr=(self), \
                          microphone=(self), \
                          camera=(self), \
                          magnetometer=(self), \
                          gyroscope=(self), \
                          speaker=(self), \
                          vibrate=(self), \
                          fullscreen=(self), \
                          payment=(self)",
}

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

  if (newHdrs.has("Content-Type") && !newHdrs.get("Content-Type").includes("text/html")) {
    return new Response(response.body , {
      status: response.status,
      statusText: response.statusText,
      headers: newHdrs
    })
  }

  Object.keys(securityHeaders).map(function(name, index) {
    newHdrs.set(name, securityHeaders[name]);
  })

  Object.keys(sanitiseHeaders).map(function(name, index) {
    newHdrs.set(name, sanitiseHeaders[name]);
  })

  removeHeaders.forEach(function(name){
    newHdrs.delete(name)
  })

  return new Response(response.body , {
    status: response.status,
    statusText: response.statusText,
    headers: newHdrs
  })
}
