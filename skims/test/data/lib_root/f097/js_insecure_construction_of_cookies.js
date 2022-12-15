// Safe because name in not _blank
function safeFunc() {
  const externalUrl = "https://www.external.com/";
  const safeName = "_parent";
  window.open(externalUrl, safeName);
}

// Safe because url is not internal
function safeFuncTwo() {
  const internalUrl = "/internal";
  const unsafeName = "_blank";
  window.open(internalUrl, unsafeName);
}

// Safe Features has correct config
function safeFuncThree() {
  window.open("http://external.com", "_blank", "noopener,noreferrer");
}

// Unsafe Features has cbad window features
function unsafeFuncFour() {
  window.open("http://external.com", "_blank", "noreferrer");
}

// Unsafe no Features parameter
function unsafeFuncFive() {
  window.open("http://external.com", "_blank");
}

// Unsafe no Features nor name parameters
function unsafeFuncSix() {
  window.open("http://external.com");
}
