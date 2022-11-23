{makeSslCertificate, ...}:
makeSslCertificate {
  name = "integrates-certs-development";
  options = [
    [
      "-subj"
      (builtins.concatStringsSep "" [
        "/C=CO"
        "/CN=fluidattacks.com"
        "/emailAddress=development@fluidattacks.com"
        "/L=Medellin"
        "/O=Fluid Attacks"
        "/ST=Antioquia"
      ])
    ]
  ];
}
