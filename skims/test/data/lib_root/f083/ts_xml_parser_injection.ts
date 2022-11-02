declare function require(name:string);

const libxmljs = require("libxmljs");
const fs = require("fs");

function xml_parser_vuln() {
  const xml = fs.readFileSync("xxe.xml", "utf8");

  const config = {
    noblanks: true,
    noent: true,
    nocdata: true,
  };
  const xmlDoc = libxmljs.parseXmlString(xml, config); // Noncompliant: noent set to true

  const xmlGoodDoc = libxmljs.parseXmlString(xml); // Compliant: noent set to false by default
}

function xml_parser_fail() {
  const xml = fs.readFileSync("xxe.xml", "utf8");

  const xmlDoc = libxmljs.parseXmlString(xml, {
    noblanks: true,
    noent: true,
    nocdata: true,
  });
}

function xml_parser_good() {
  const xml = fs.readFileSync("xxe.xml", "utf8");

  const xmlGoodDoc = libxmljs.parseXmlString(xml); // Compliant: noent set to false by default
}
