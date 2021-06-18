{ terraformApply
, ...
}:
terraformApply {
  name = "makes-foss-apply";
  product = "makes";
  target = "makes/applications/makes/foss/src";
}
