'use strict';
const path = require("path");
exports.handler = (event, context, callback) => {

  // Extract the request from the CloudFront event that is sent to Lambda@Edge
  const { request } = event.Records[0].cf;

  let plainUri = request.uri;

  // Replace the received URI with the URI that includes the index page
  request.uri = checkUri(plainUri);

  // Return to CloudFront
  return callback(null, request);

};

const checkUri = (plainUri) => {
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

    } else {
      newUri = path.join(oldPath.dir, oldPath.base, "index.html");
    }
  } else {
    newUri = plainUri;
  }

  console.log(newUri);

  return newUri;
};


const testCheckUri = () => {

  // Test data: URI with an extension
  let testRequestExt = {
    "request": {
      "uri": "https://web.eph.fluidattacks.com/jperezatfluid/theme/theme.min.css"
    }
  }

  // Test data: URI with an anchor
  let testRequestAnchor = {
    "request": {
      "uri": "https://web.eph.fluidattacks.com/jperezatfluid/products#test_anchor"
    }
  }

  // Test data: URI with a closing slash
  let testRequestClose = {
    "request": {
      "uri": "https://web.eph.fluidattacks.com/jperezatfluid/products/"
    }
  }

  // Test data: URI without a closing slash
  let testRequestNoClosed = {
    "request": {
      "uri": "https://web.eph.fluidattacks.com/jperezatfluid/products"
    }
  }

  const plainUri = testRequestExt.uri; // Change the testRequest variable to check different cases
  console.log("Plain URI: " + plainUri);

  const newUri = checkUri(plainUri);

  console.log("Resulting URI: " + newUri);

}
