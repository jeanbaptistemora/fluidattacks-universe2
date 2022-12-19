const AdmZip = require('adm-zip');
const fs = require('fs');

const zip = new AdmZip("zip-slip.zip");
const zipEntries = zip.getEntries();
zipEntries.forEach(function (zipEntry) {
  fs.createWriteStream(zipEntry.entryName); // Noncompliant
});

const pathmodule = require('path');
zipEntries.forEach(function (zipEntry) {
  let resolvedPath = pathmodule.join(__dirname + '/archive_tmp', zipEntry.entryName); // join will resolve "../"

  if (resolvedPath.startsWith(__dirname + '/archive_tmp')) {
    // the file cannot be extracted outside of the "archive_tmp" folder
    fs.createWriteStream(resolvedPath); // Compliant
  }
});
