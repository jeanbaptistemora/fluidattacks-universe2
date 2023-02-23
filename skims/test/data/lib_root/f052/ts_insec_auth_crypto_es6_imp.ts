import { createHmac } from "crypto";

const secret = "GfG";

// Lines 6 and 10 should be marked
let hash = createHmac("sha256", secret)
  .update("This is a test in a chain")
  .digest("hex");

hash = createHmac("sha1", secret).update("This is a test in a chain").digest("hex");

// Next following lines are safe:
let hash1 = createHmac("sha512", secret)
  .update("This is a test in a chain")
  .digest("hex");

hash1 = crypto.createHmac("sha1", secret);
