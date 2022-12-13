const crypto = require("crypto");

let keyString = "*4wQZgn+U2RW_mb=";
const key = Buffer.from(keyString.substring(0, 8), "utf8");

const cipher = crypto.createCipheriv("des-ecb", key, "");

let encrypted = "";
cipher.on("readable", () => {
  let chunk;
  while (null !== (chunk = cipher.read())) {
    encrypted += chunk.toString("hex");
  }
});
cipher.on("end", () => {
  console.log(encrypted);
});

cipher.write("some clear text data");
cipher.end();
