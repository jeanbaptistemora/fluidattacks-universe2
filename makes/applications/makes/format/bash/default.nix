{ bashFormat
, ...
}:
bashFormat {
  targets = [ "." ];
  name = "makes-format-bash";
}
