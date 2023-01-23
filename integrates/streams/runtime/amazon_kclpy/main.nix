{inputs, ...}: let
  # https://github.com/awslabs/dynamodb-streams-kinesis-adapter/blob/1.6.0/pom.xml
  streams_adapter_version = "1.6.0";
  kinesis_client_version = "1.14.9";
  aws_sdk_version = "1.12.130";
  jackson_databind_version = "2.12.7.1";

  # https://github.com/aws/aws-sdk-java/blob/1.12.130/pom.xml
  httpclient_version = "4.5.13";
  httpcore_version = "4.4.13";
  codec_version = "1.15";
  jackson_version = "2.12.3";

  # https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.KCLAdapter.html
  dynamodb_streams_kinesis_adapter_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/dynamodb-streams-kinesis-adapter/${streams_adapter_version}/dynamodb-streams-kinesis-adapter-${streams_adapter_version}.jar";
    sha256 = "1pl5lgn737zf7g4kzsx92y6srd582jbcj974adjky6i76b2aryyp";
  };

  # https://github.com/awslabs/amazon-kinesis-client/issues/761
  aws_java_sdk_sts_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-sts/${aws_sdk_version}/aws-java-sdk-sts-${aws_sdk_version}.jar";
    sha256 = "00y03jmz3xszrh74v8qp6qj39ji0rp1km25cyn02cqlvql7sk9b2";
  };

  # https://github.com/awslabs/amazon-kinesis-client-python/blob/v1.5.1/setup.py
  amazon_kinesis_client_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/amazon-kinesis-client/${kinesis_client_version}/amazon-kinesis-client-${kinesis_client_version}.jar";
    sha256 = "02vn567bgd8pvbqid0idmabrxh4kfswp168d118c74bhk9ij0cjb";
  };
  aws_java_sdk_dynamodb_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-dynamodb/${aws_sdk_version}/aws-java-sdk-dynamodb-${aws_sdk_version}.jar";
    sha256 = "1bk921zjby3w9wja2b5398i7awjfcjw76nlzkm21zpj43nglbaq1";
  };
  aws_java_sdk_s3_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-s3/${aws_sdk_version}/aws-java-sdk-s3-${aws_sdk_version}.jar";
    sha256 = "0c93p5hrjcpfy8amsimf57kms72sdj4xbr68zl432c2i94j4g33k";
  };
  aws_java_sdk_kms_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-kms/${aws_sdk_version}/aws-java-sdk-kms-${aws_sdk_version}.jar";
    sha256 = "0vpyrkh3kr8gy2j92pkhcanrknjsjy8fmq66dzr61h358xxyx3va";
  };
  aws_java_sdk_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-core/${aws_sdk_version}/aws-java-sdk-core-${aws_sdk_version}.jar";
    sha256 = "1vnla0s9m8xf9rlff349jgx5j9w2n3r474yq5xfgnd3ymnkzrcsp";
  };
  httpclient_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpclient/${httpclient_version}/httpclient-${httpclient_version}.jar";
    sha256 = "0hzp3vrxbnyc6w86v671wp0zchb634rgrwwcc00m0skcarm05sbg";
  };
  httpcore_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpcore/${httpcore_version}/httpcore-${httpcore_version}.jar";
    sha256 = "091lnk100aqdg2bwbyg8rnp64dyfpz6kgicylg7my92317a8jvp0";
  };
  commons_codec_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-codec/commons-codec/${codec_version}/commons-codec-${codec_version}.jar";
    sha256 = "0qzd8v96j4x7jjcfpvvdh9ar1xhwxpxi2rh51nzhj0br7bbgdsdk";
  };
  ion_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/ion/ion-java/1.0.2/ion-java-1.0.2.jar";
    sha256 = "19bishkkp0y5p9cw1x2wq5kbqlc6fi0s0mrp5ay0mkhzb8h7n4hd";
  };
  jackson_databind_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-databind/${jackson_databind_version}/jackson-databind-${jackson_databind_version}.jar";
    sha256 = "0bg0108a11ng0ihyr9y7bbrj4lsd910rbxjzcvandq2w82n4ql1z";
  };
  jackson_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-annotations/${jackson_version}/jackson-annotations-${jackson_version}.jar";
    sha256 = "1sg74vrqhympfrvs1aanar5ij79h18g1m6i91a41g8j4pcjhmnh5";
  };
  jackson_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-core/${jackson_version}/jackson-core-${jackson_version}.jar";
    sha256 = "1q3i7wn2p6pxmfkf0c7slv93xd6qgs8zrx1zmzrm8784rvxk9vxs";
  };
  jackson_dataformat_cbor_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/dataformat/jackson-dataformat-cbor/${jackson_version}/jackson-dataformat-cbor-${jackson_version}.jar";
    sha256 = "1kaxq0pm43lwgwl7d34i2rvnl6j570xvcby3pllb0j1zxnnd8j1i";
  };
  joda_time_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=joda-time/joda-time/2.8.1/joda-time-2.8.1.jar";
    sha256 = "18hz0ri229ix133cahzng0jvwh30jvd3lpsc51scjmsryyahnrxl";
  };
  jmespath_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/jmespath-java/${aws_sdk_version}/jmespath-java-${aws_sdk_version}.jar";
    sha256 = "0pps3anyl155yjhcrr0x2rdgm5apsg7ld5cn4bdvkk1iimzh9r53";
  };
  aws_java_sdk_kinesis_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-kinesis/${aws_sdk_version}/aws-java-sdk-kinesis-${aws_sdk_version}.jar";
    sha256 = "01d5bsnr64lv2rvjpbwjirryf8fx88shs2svkxn52laicjn6gbvy";
  };
  aws_java_sdk_cloudwatch_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-cloudwatch/${aws_sdk_version}/aws-java-sdk-cloudwatch-${aws_sdk_version}.jar";
    sha256 = "0qskrif9837crh7ay9cy0fic11w4d18w9h6r8aiblnpjyhh8piz4";
  };
  guava_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/guava/guava/26.0-jre/guava-26.0-jre.jar";
    sha256 = "0b7a7c1hgx5rmnx0ma5f2dp7agy0by7107xhsay21g35ssxcmsd0";
  };
  jsr305_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar";
    sha256 = "1iyh53li6y4b8gp8bl52fagqp8iqrkp4rmwa5jb8f9izg2hd4skn";
  };
  checker_qual_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/checkerframework/checker-qual/2.5.2/checker-qual-2.5.2.jar";
    sha256 = "02h4iibbzqwy5i9bfqp6h5p2rsp7vi1fgqlf1xqfgm5rr28jdc34";
  };
  error_prone_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/errorprone/error_prone_annotations/2.1.3/error_prone_annotations-2.1.3.jar";
    sha256 = "1y3zzjqxckrn39z5d4724lwhkb9fx94i0kb3gkhsjgf18yak5l03";
  };
  j2objc_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/j2objc/j2objc-annotations/1.1/j2objc-annotations-1.1.jar";
    sha256 = "1xpcvmnw2y3fa56hhk8dmknrq8afr6r3kdmzsg9hnwgjg3msg519";
  };
  animal_sniffer_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/codehaus/mojo/animal-sniffer-annotations/1.14/animal-sniffer-annotations-1.14.jar";
    sha256 = "0pchd4360mim0f0a6vwr33szigihgvv4ic1scz1l9mxssq5k4s10";
  };
  protobuf_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/protobuf/protobuf-java/2.6.1/protobuf-java-2.6.1.jar";
    sha256 = "1rn4vazkb50h3kypld9jq4bslf4dd37i4qb1ylfl6gwq8d45bajm";
  };
  commons_lang3_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/commons/commons-lang3/3.7/commons-lang3-3.7.jar";
    sha256 = "0ix8nr1pxy5k8awbarl98rpzw2rf1kglwlwn7jaxj2350hgc73bf";
  };
  commons_logging_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar";
    sha256 = "110p76ws0ql4zs8jjr0jldq0h3yrc4zl884zvb40i69fr1pkz43h";
  };

  jars = [
    dynamodb_streams_kinesis_adapter_jar
    aws_java_sdk_sts_jar
    amazon_kinesis_client_jar
    aws_java_sdk_dynamodb_jar
    aws_java_sdk_s3_jar
    aws_java_sdk_kms_jar
    aws_java_sdk_core_jar
    httpclient_jar
    httpcore_jar
    commons_codec_jar
    ion_java_jar
    jackson_databind_jar
    jackson_annotations_jar
    jackson_core_jar
    jackson_dataformat_cbor_jar
    joda_time_jar
    jmespath_java_jar
    aws_java_sdk_kinesis_jar
    aws_java_sdk_cloudwatch_jar
    guava_jar
    jsr305_jar
    checker_qual_jar
    error_prone_annotations_jar
    j2objc_annotations_jar
    animal_sniffer_annotations_jar
    protobuf_java_jar
    commons_lang3_jar
    commons_logging_jar
  ];
in
  inputs.nixpkgs.python311Packages.amazon_kclpy.overridePythonAttrs (_: rec {
    doCheck = false;
    prePatch = ''
      # Add the jars so it doesn't attempt to download them
      mkdir -p "amazon_kclpy/jars"
      for jar in ${builtins.concatStringsSep " " jars}; do
        cp $jar "amazon_kclpy/jars/$(stripHash $jar)"
      done

      # Remove deps only needed to run the samples
      substituteInPlace setup.py \
        --replace "install_requires=PYTHON_REQUIREMENTS," "install_requires=[],"

      # Override some versions to ensure compatibility with the adapter
      substituteInPlace setup.py \
        --replace "'1.9.3'" "'${kinesis_client_version}'" \
        --replace "'1.11.438'" "'${aws_sdk_version}'" \
        --replace "'4.5.5'" "'${httpclient_version}'" \
        --replace "'4.4.9'" "'${httpcore_version}'"  \
        --replace "'1.10'" "'${codec_version}'" \
        --replace "'2.6.7.1'" "'${jackson_databind_version}'" \
        --replace "'2.6.0'" "'${jackson_version}'" \
        --replace "'2.6.7'" "'${jackson_version}'"
    '';
    propagatedBuildInputs = [];
    src = inputs.nixpkgs.fetchFromGitHub {
      owner = "awslabs";
      repo = "amazon-kinesis-client-python";
      rev = "v${version}";
      sha256 = "A9v6FVzziYdnPv+SSflT+fnbIzNZYspP5qJDgGGCWEo=";
    };
    version = "1.5.1";
  })
