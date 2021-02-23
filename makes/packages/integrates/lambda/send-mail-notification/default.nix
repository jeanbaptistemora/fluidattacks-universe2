{ buildPythonLambda
, integratesPkgs
, path
, ...
}:
buildPythonLambda integratesPkgs {
  name = "integrates-lambda-send-mail-notification";
  python = integratesPkgs.python37;
  requirements = {
    direct = [
      "certifi==2020.4.5.2"
      "idna==2.9"
      "mandrill-really-maintained==1.2.4"
    ];
    inherited = [
      "chardet==3.0.4"
      "docopt==0.6.2"
      "requests==2.24.0"
      "urllib3==1.25.10"
    ];
  };
  source = path "/integrates/lambda/send_mail_notification";
}
