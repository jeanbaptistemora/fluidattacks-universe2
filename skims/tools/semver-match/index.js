const semverIntersects = require("semver/ranges/intersects");
const semverRange = require("semver/classes/range");

const coerce = (constraint) => {
  // Coerce versions like a.b.c.d-pre+build to a.b.c-pre-build
  // i.e. remove version components after the third one so it complies semver
  const constraintTokens = constraint.split(/([-+])/);
  const version = constraintTokens[0];
  const tags = constraintTokens.slice(1).join("");

  let versionCoerced = version.split(".");

  if (versionCoerced.length < 3) {
    versionCoerced.push("*");
  };

  return versionCoerced.slice(0, 3).join(".") + tags;
};

const coerceRange = (range) => range
  .replace(/\s+/g, " ")
  .replace(/\s*\|\|\s*/g, "||")
  .split("||")
  .map((token) => token
    .split(" ")
    .map(coerce)
    .join(" "))
  .join("||");

const argv = process.argv;
const left = argv[2];
const right = argv[3];
const leftCoerced = coerceRange(left);
const rightCoerced = coerceRange(right);

console.error("Given left constraint:", left);
console.error("Given right constraint:", right);
console.error();
console.error("Coerced left constraint:", leftCoerced);
console.error("Coerced right constraint:", rightCoerced);
console.error();
console.error("Using left constraint:", new semverRange(leftCoerced).range);
console.error("Using right constraint:", new semverRange(rightCoerced).range);

try {
  console.log(JSON.stringify({
    success: true,
    match: semverIntersects(leftCoerced, rightCoerced),
  }, null, true));
}
catch (error) {
  console.log(JSON.stringify({
    success: false,
    error: error.toString(),
  }, null, true));
}

process.exit(0);
