const externalUrl = "https://www.external.com/";
const internalUrl = "/internal";
const safeName = "_parent";
const unsafeName = "_blank";
const safeWindowFeatures = "noopener, noreferrer";
const unsafeWindowFeatures = "noreferrer";

// Safe cases Skims must not mark any of following
window.open(internalUrl);
window.open(internalUrl, unsafeName, unsafeWindowFeatures);
window.open(externalUrl, safeName, unsafeWindowFeatures);
window.open(externalUrl, safeName);
window.open(externalUrl, unsafeName, safeWindowFeatures);

// Unsafe cases Skims must mark all following cases
window.open(externalUrl, unsafeName, unsafeWindowFeatures);
window.open(externalUrl, unsafeName);
window.open(externalUrl);
