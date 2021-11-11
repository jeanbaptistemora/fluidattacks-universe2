{ makeSslCertificate
, ...
}:
makeSslCertificate {
  name = "integrates-back-certs-development";
  options = [
    [ "-subj" "/C=CO" ]
    [ "-subj" "/CN=fluidattacks.com" ]
    [ "-subj" "/emailAddress=development@fluidattacks.com" ]
    [ "-subj" "/L=Medellin" ]
    [ "-subj" "/O=Fluid" ]
    [ "-subj" "/ST=Antioquia" ]
  ];
}
