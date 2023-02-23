import { createHmac as hmacAlias } from "crypto";

const secret = "GfG";

// Lines 6 and 10 should be marked
let hash = hmacAlias("sha256", secret)
  .update("This is a test in a chain")
  .digest("hex");

hash = hmacAlias("sha1", secret).update("This is a test in a chain");

// Next following lines are safe:
let hash1 = createHmac("sha256", secret)
  .update("This is a test in a chain")
  .digest("hex");

hash1 = crypto.createHmac("sha1", secret);
