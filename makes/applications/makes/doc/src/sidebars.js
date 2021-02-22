function getDocs(path) {
  var fs = require('fs');
  var files = fs.readdirSync(`docs/${path}`)

  files.forEach(
    function prepareFile(item, index, arr) {
      arr[index] = `${path}/${item.replace('.md', '')}`
    }
  )

  return files
}

module.exports = {
  Asserts: {
    Asserts: getDocs('asserts'),
  },
  Integrates: {
    Integrates: getDocs('integrates'),
  },
  Skims: {
    Skims: getDocs('skims'),
  },
};
