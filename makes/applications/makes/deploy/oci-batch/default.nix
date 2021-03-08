{ dockerBuild
, ...
}:
dockerBuild {
  context = ".";
  name = "makes-deploy-oci-batch";
  tag = "registry.gitlab.com/fluidattacks/product/makes:batch";
}
