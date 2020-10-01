'use strict';
exports.handler = (event, context, callback) => {

  // Extract the request from the CloudFront event that is sent to Lambda@Edge
  var request = event.Records[0].cf.request;

  // Extract the URI from the request
  var olduri = request.uri;

  // Match any 
  var newuri;
  if ( !olduri.endsWith("index.html") ) {
    if ( !olduri.endsWith("/") ) {
      if ( olduri.includes("#") ) {
        newuri = olduri.replace("#", "/index.html#");
      } else {
        newuri = olduri.concat("/index.html");
      }
    } else {
      newuri = olduri.replace(/\/$/, '\/index.html');
    }
  }


  // Log the URI as received by CloudFront and the new URI to be used to fetch from origin
  console.log("Old URI: " + olduri);
  console.log("New URI: " + newuri);

  // Replace the received URI with the URI that includes the index page
  request.uri = newuri;

  // Return to CloudFront
  return callback(null, request);

};
