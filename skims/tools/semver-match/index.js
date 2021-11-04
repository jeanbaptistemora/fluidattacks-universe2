const semverIntersects = require('semver/ranges/intersects');

const argv = process.argv;
const left = argv[2];
const right = argv[3];

try {
  console.log(JSON.stringify({
    success: true,
    match: semverIntersects(left, right),
  }, null, true));
}
catch (error) {
  console.log(JSON.stringify({
    success: false,
    error: error.toString(),
  }, null, true));
}

process.exit(0);
