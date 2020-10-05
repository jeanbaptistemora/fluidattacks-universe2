'use strict';
const path = require("path");
exports.handler = (event, context, callback) => {

  // Extract the request from the CloudFront event that is sent to Lambda@Edge
  const { request } = event.Records[0].cf;

  let plainUri = request.uri;

  console.log("Request URI: ", plainUri);
  // Extract the URI from the request,
  // verify if the URI has an etension or an anchor and set the index.html
  const oldPath = path.parse(plainUri);
  let newUri;

  console.log('Parsed Path: ', oldPath);

  // Check if the path dict has an extension
  if (oldPath.ext === "") {
    // Check if the URI has an anchor
    if (oldPath.base.includes("#")) {
      newUri = path.join(oldPath.dir, oldPath.base.replace("#", "/index.html#"));
        // Replace the received URI with the URI that includes the index page
      request.uri = newUri;
      const response = {
        status: '301',
        statusDescription: 'Found',
        headers: {
          location: [{
            key: 'Location', value: newUri,
          }],
        }
      };
      console.log("Response: ", JSON.stringify(response));
      callback(null, request, response);
    } else {
      newUri = path.join(oldPath.dir, oldPath.base, "index.html");
      request.uri = newUri;
      const response = {
        status: '301',
        statusDescription: 'Found',
        headers: {
          location: [{
            key: 'Location', value: newUri,
          }],
        }
      };
      console.log("Response: ", JSON.stringify(response));
      callback(null, request, response);
    }
  } else {
    newUri = plainUri;
    request.uri = newUri;
    callback(null, request);
  }

  console.log("New Request: ", JSON.stringify(request));
};

