# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{inputs, ...}: let
  amazon_kinesis_client_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/amazon-kinesis-client/1.13.3/amazon-kinesis-client-1.13.3.jar";
    sha256 = "0h49rr8d1sfwq60gwfpiwwj00gi8lvhyydd2ww438r1a1h6wzbsb";
  };
  aws_java_sdk_dynamodb_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-dynamodb/1.12.311/aws-java-sdk-dynamodb-1.12.311.jar";
    sha256 = "0y3q54mgs5prwmc0pnkp3l3zz53x72v4za6jhbf8ix5yh5ad43wg";
  };
  aws_java_sdk_s3_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-s3/1.12.311/aws-java-sdk-s3-1.12.311.jar";
    sha256 = "129lbhb5qzgsfmyh06bc3ccz2ycsxw3g04qrfwnwz6lff5bhv6yz";
  };
  aws_java_sdk_kms_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-kms/1.12.311/aws-java-sdk-kms-1.12.311.jar";
    sha256 = "03k6czwlalm867z25avlx78bf0ccx31m8my2r7ykcvnz1rc70kb0";
  };
  aws_java_sdk_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-core/1.12.311/aws-java-sdk-core-1.12.311.jar";
    sha256 = "1psqckhqpa97agq6a3s67nyzc9xm12d1dicjbxp7z19n508xlhlx";
  };
  ion_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/ion/ion-java/1.0.2/ion-java-1.0.2.jar";
    sha256 = "19bishkkp0y5p9cw1x2wq5kbqlc6fi0s0mrp5ay0mkhzb8h7n4hd";
  };
  jmespath_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/jmespath-java/1.12.311/jmespath-java-1.12.311.jar";
    sha256 = "189kfv98bb8bnxv2bmfd2h441dxxpvxcqdbmzmdq5a22xm8fiz09";
  };
  jackson_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-annotations/2.6.0/jackson-annotations-2.6.0.jar";
    sha256 = "1bgmxwasmiajvncnmp4q0vmxga5xh36ndi2g8k67c4wqgl28qd03";
  };
  jackson_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-core/2.6.7/jackson-core-2.6.7.jar";
    sha256 = "0krh3yavqvcwpvpqsv7jr5q5h1lz9pcvb4i1mpg52g84z6wh934i";
  };
  jackson_databind_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-databind/2.6.7.1/jackson-databind-2.6.7.1.jar";
    sha256 = "0jhabr8hqbgshjhg0rmr4bm82w2i16nryfxfyhv7asc0d0y09dn6";
  };
  jackson_dataformat_cbor_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/dataformat/jackson-dataformat-cbor/2.6.7/jackson-dataformat-cbor-2.6.7.jar";
    sha256 = "1gwry7a4jp8faiziq9kyciwl402mxshrv428cn56nyba32whyslm";
  };
  aws_java_sdk_kinesis_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-kinesis/1.12.311/aws-java-sdk-kinesis-1.12.311.jar";
    sha256 = "1yshcnr9riyjyy51xs4id0g030is3spdps3wdcgg8nf1rya2lw61";
  };
  aws_java_sdk_cloudwatch_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-cloudwatch/1.12.311/aws-java-sdk-cloudwatch-1.12.311.jar";
    sha256 = "0ic4d79hj3bh9kaqc8savz9i32dxfadhi5bijz6d8fcp13j7l57r";
  };
  guava_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/guava/guava/26.0-jre/guava-26.0-jre.jar";
    sha256 = "0b7a7c1hgx5rmnx0ma5f2dp7agy0by7107xhsay21g35ssxcmsd0";
  };
  jsr305_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar";
    sha256 = "1iyh53li6y4b8gp8bl52fagqp8iqrkp4rmwa5jb8f9izg2hd4skn";
  };
  error_prone_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/errorprone/error_prone_annotations/2.1.3/error_prone_annotations-2.1.3.jar";
    sha256 = "1y3zzjqxckrn39z5d4724lwhkb9fx94i0kb3gkhsjgf18yak5l03";
  };
  j2objc_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/j2objc/j2objc-annotations/1.1/j2objc-annotations-1.1.jar";
    sha256 = "1xpcvmnw2y3fa56hhk8dmknrq8afr6r3kdmzsg9hnwgjg3msg519";
  };
  protobuf_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/protobuf/protobuf-java/2.6.1/protobuf-java-2.6.1.jar";
    sha256 = "1rn4vazkb50h3kypld9jq4bslf4dd37i4qb1ylfl6gwq8d45bajm";
  };
  commons_lang3_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/commons/commons-lang3/3.7/commons-lang3-3.7.jar";
    sha256 = "0ix8nr1pxy5k8awbarl98rpzw2rf1kglwlwn7jaxj2350hgc73bf";
  };
  httpclient_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpclient/4.5.13/httpclient-4.5.13.jar";
    sha256 = "0hzp3vrxbnyc6w86v671wp0zchb634rgrwwcc00m0skcarm05sbg";
  };
  httpcore_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpcore/4.4.9/httpcore-4.4.9.jar";
    sha256 = "1i8zypyncjd9swyzb3zpv7innjpxpvicdlq806kys8j2kc5iqjhv";
  };
  checker_qual_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/checkerframework/checker-qual/2.5.2/checker-qual-2.5.2.jar";
    sha256 = "02h4iibbzqwy5i9bfqp6h5p2rsp7vi1fgqlf1xqfgm5rr28jdc34";
  };
  animal_sniffer_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/codehaus/mojo/animal-sniffer-annotations/1.14/animal-sniffer-annotations-1.14.jar";
    sha256 = "0pchd4360mim0f0a6vwr33szigihgvv4ic1scz1l9mxssq5k4s10";
  };
  commons_codec_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-codec/commons-codec/1.10/commons-codec-1.10.jar";
    sha256 = "0scm6321zz76dc3bs8sy2qyami755lz4lq5455gl67bi9slxyha2";
  };
  commons_logging_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-logging/commons-logging/1.1.3/commons-logging-1.1.3.jar";
    sha256 = "110p76ws0ql4zs8jjr0jldq0h3yrc4zl884zvb40i69fr1pkz43h";
  };
  joda_time_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=joda-time/joda-time/2.8.1/joda-time-2.8.1.jar";
    sha256 = "18hz0ri229ix133cahzng0jvwh30jvd3lpsc51scjmsryyahnrxl";
  };
  dynamodb_streams_kinesis_adapter_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/dynamodb-streams-kinesis-adapter/1.5.3/dynamodb-streams-kinesis-adapter-1.5.3.jar";
    sha256 = "09dc17f9plyg5455609ic4jf1blxn7karz7cfww5bk2qzfq0s7fh";
  };

  jars = [
    aws_java_sdk_dynamodb_jar
    aws_java_sdk_s3_jar
    aws_java_sdk_kms_jar
    ion_java_jar
    amazon_kinesis_client_jar
    aws_java_sdk_core_jar
    jmespath_java_jar
    jackson_annotations_jar
    jackson_core_jar
    jackson_databind_jar
    jackson_dataformat_cbor_jar
    aws_java_sdk_kinesis_jar
    aws_java_sdk_cloudwatch_jar
    guava_jar
    jsr305_jar
    error_prone_annotations_jar
    j2objc_annotations_jar
    protobuf_java_jar
    commons_lang3_jar
    httpclient_jar
    httpcore_jar
    checker_qual_jar
    animal_sniffer_annotations_jar
    commons_codec_jar
    commons_logging_jar
    joda_time_jar
    dynamodb_streams_kinesis_adapter_jar
  ];
in
  inputs.nixpkgs.python39Packages.amazon_kclpy.overridePythonAttrs (_: rec {
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
        --replace "'1.9.3'" "'1.13.3'" \
        --replace "'1.11.438'" "'1.12.311'" \
        --replace "'4.5.5'" "'4.5.13'"
    '';
    src = inputs.nixpkgs.fetchFromGitHub {
      owner = "awslabs";
      repo = "amazon-kinesis-client-python";
      rev = "v${version}";
      sha256 = "A9v6FVzziYdnPv+SSflT+fnbIzNZYspP5qJDgGGCWEo=";
    };
    version = "1.5.1";
  })
