{ terraformApply
, ...
}:
terraformApply {
  name = "makes-foss-apply";
  product = "makes";
  target = "makes/applications/makes/foss/src";
  vars = [
    "GITHUB_API_TOKEN"
    "GITHUB_API_USER"
    "PRODUCT_API_TOKEN"
    "PRODUCT_API_USER"
  ];
}
