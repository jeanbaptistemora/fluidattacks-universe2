let securityHeaders = {
  "Content-Security-Policy" : "script-src \
                              'self' \
                              'unsafe-inline' \
                              *.cloudflare.com \
                              *.cloudflareinsights.com \
                              *.cookiebot.com \
                              *.google-analytics.com \
                              *.googleadservices.com \
                              *.googletagmanager.com \
                              *.hotjar.com \
                              *.typekit.net \
                              *.zoho.com \
                              *.zohocdn.com \
                              *.zohopublic.com \
                              *.zohostatic.com \
                              googleads.g.doubleclick.net \
                              snap.licdn.com; \
                              frame-ancestors \
                              'self'; \
                              object-src \
                              'none'; \
                              upgrade-insecure-requests;",
  "Strict-Transport-Security" : "max-age=31536000",
  "X-Xss-Protection" : "1; mode=block",
  "X-Frame-Options" : "DENY",
  "X-Content-Type-Options" : "nosniff",
  "X-Permitted-Cross-Domain-Policies": "none",
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
