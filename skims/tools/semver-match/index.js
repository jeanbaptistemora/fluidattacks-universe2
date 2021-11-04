const semverIntersects = require('semver/ranges/intersects');
const semverRange = require('semver/classes/range');

const argv = process.argv;
let left = argv[2];
const right = argv[3];

// Sanitize a little bit the left constraint
left = left.split('-', 1).slice(0, 1)[0]; // Ignore prerelease tag
left = left.split('+', 1).slice(0, 1)[0]; // Ignore build tag
left = left.split('.').slice(0, 3).join('.'); // Ignore fourth+ components
console.error('Using left constraint:', new semverRange(left).range);
console.error('Using right constraint:', new semverRange(right).range);

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
