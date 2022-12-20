const extUrl: string = "https://www.external.com/";
const intUrl: string = "/internal";
const safe: string = "_parent";
const unsafe: string = "_blank";
const safeWF: string = "noopener, noreferrer";
const unsafeWF: string = "noreferrer";

//String literals

// Safe cases Skims must not mark any of following
window.open("/internal");
window.open("https://External.com", "_parent");
window.open("https://External.com", "_blank", "noreferrer,noopener");

// Unsafe cases Skims must mark all following cases
window.open("https://External.com");
window.open("https://External.com", "_blank");
window.open("https://External.com", "_blank", "Any");

// Data in variables

// Safe cases Skims must not mark any of following
window.open();
window.open(intUrl);
window.open(intUrl, unsafe, unsafeWF);
window.open(extUrl, safe, unsafeWF);
window.open(extUrl, safe);
window.open(extUrl, unsafe, safeWF);

// Unsafe cases Skims must mark all following cases
window.open(extUrl, unsafe, unsafeWF);
window.open(extUrl, unsafe);
window.open(extUrl);
