# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{inputs, ...}: let
  kinesis_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/kinesis/2.17.52/kinesis-2.17.52.jar";
    sha256 = "0iswmvqmdg4galsxnjkgc7sxh6pbjmn8www04q50z2hi58cpsmzv";
  };
  annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/annotations/2.17.52/annotations-2.17.52.jar";
    sha256 = "1kccljkrvi9z32z3jdmkxpvyi402zzxzfwqx1jwj86683br4x38j";
  };
  apache_client_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/apache-client/2.17.52/apache-client-2.17.52.jar";
    sha256 = "0716igzc5fyj2m2krypwyjh73nlvj0fxcy029y7k3hjzxyj7ncif";
  };
  auth_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/auth/2.17.52/auth-2.17.52.jar";
    sha256 = "13pwam31ijn0kx4j2gvwh5q8kdr22kna6gb95zl8v3jpg5alpj8k";
  };
  aws_cbor_protocol_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/aws-cbor-protocol/2.17.52/aws-cbor-protocol-2.17.52.jar";
    sha256 = "14p34qdd7ivhz651ikwf4c146dg9h5wlmcr388v107bigkd71wz9";
  };
  aws_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/aws-core/2.17.52/aws-core-2.17.52.jar";
    sha256 = "1j2zz96anl3k871av4wc6xdix8g9fkcmawn5kczdlvsadqckxv5p";
  };
  aws_json_protocol_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/aws-json-protocol/2.17.52/aws-json-protocol-2.17.52.jar";
    sha256 = "1zkm5csvi30i8makgsxy0y0dmp7lxyxd4d9x0gxajv8ks0q1zpsc";
  };
  aws_query_protocol_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/aws-query-protocol/2.17.52/aws-query-protocol-2.17.52.jar";
    sha256 = "0h7l50vqsmbvsm0wnyv9i1484hj3isvpvsv9nb2syxk10va9nb97";
  };
  cloudwatch_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/cloudwatch/2.17.52/cloudwatch-2.17.52.jar";
    sha256 = "05di1rcnxa59ld0d2g8brkqsblfm1k5v7al8izx3jr7ldqn7sxyv";
  };
  dynamodb_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/dynamodb/2.17.52/dynamodb-2.17.52.jar";
    sha256 = "16y13nilzrr69nxnhiz3fkmdd8l0zpb0hqlb10j1j1rqbbzf08br";
  };
  http_client_spi_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/http-client-spi/2.17.52/http-client-spi-2.17.52.jar";
    sha256 = "066lcs5lzpaq3c4hg42mklb4jmdy1n6wb7k0c0kr198sqqm7fjdk";
  };
  json_utils_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/json-utils/2.17.52/json-utils-2.17.52.jar";
    sha256 = "0529s6w45vm0ysg37ly7sgvlr71xf4jyim9qr4iqhd0s25saw9vs";
  };
  metrics_spi_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/metrics-spi/2.17.52/metrics-spi-2.17.52.jar";
    sha256 = "05x9l8zbh3p8x92qz7v3ivcz9xrd8hksamq8bx523gq8713dvrbr";
  };
  netty_nio_client_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/netty-nio-client/2.17.52/netty-nio-client-2.17.52.jar";
    sha256 = "0pmxrfbrjrbz9bzgqgxvyiqdhaxald3yjja73kp7zazvf9avk54b";
  };
  protocol_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/protocol-core/2.17.52/protocol-core-2.17.52.jar";
    sha256 = "15582dnzvfdv4vmd082idd463xyprpr569brjnqqkfdkbqghw7lr";
  };
  profiles_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/profiles/2.17.52/profiles-2.17.52.jar";
    sha256 = "1g12fqwyprqjd2h7gnmcjd4zj72jpwwrjmnid8lzjn22jk2c0yag";
  };
  regions_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/regions/2.17.52/regions-2.17.52.jar";
    sha256 = "0wwnwrkm8ajbx29nv93swa0yna2qz9iq1ix62x9c55jv6ihnyv77";
  };
  sdk_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/sdk-core/2.17.52/sdk-core-2.17.52.jar";
    sha256 = "00vixjng5mkky8rmdj6v0a0zy0h0fr2ga8mrp0nn3mipgpxzyhq9";
  };
  sts_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/sts/2.17.52/sts-2.17.52.jar";
    sha256 = "0g6dgyblx97y258q8brwr5v4n5l7xd2w82bbn03nnhaajjs0jicg";
  };
  #aaa
  third_party_jackson_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/third-party-jackson-core/2.17.52/third-party-jackson-core-2.17.52.jar";
    sha256 = "0lzgh0nncld2ljwrzmglrpj6blx1c63srvckmi3pd9gxak91ic6v";
  };
  third_party_jackson_dataformat_cbor_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/third-party-jackson-dataformat-cbor/2.17.52/third-party-jackson-dataformat-cbor-2.17.52.jar";
    sha256 = "02pbz8ayjyirqjghnqwxsq4fxmvgjgymigjbqis76pigyjfzcbpm";
  };
  utils_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/awssdk/utils/2.17.52/utils-2.17.52.jar";
    sha256 = "0vcz9gc77518bd9ddasi6idbwy7z1h0kxg5nsz2h360nfxra1pq1";
  };
  eventstream_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/eventstream/eventstream/1.0.1/eventstream-1.0.1.jar";
    sha256 = "08p8dk0p7v39lb1k9kig87x21syhn08826qr0b1h4zqijvkdhdqc";
  };
  ion_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/ion/ion-java/1.5.1/ion-java-1.5.1.jar";
    sha256 = "1rzvk6x015ix1qmr1iqyvl1s6bq1kmcvnhdi9i9r07cf837nyz2f";
  };
  schema_registry_serde_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/glue/schema-registry-serde/1.1.5/schema-registry-serde-1.1.5.jar";
    sha256 = "01a0ckp46a56l0src5imb2dgdr44f2dfwa769gjb52idzlbl6wbf";
  };
  amazon_kinesis_client_multilang_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/kinesis/amazon-kinesis-client-multilang/2.3.9/amazon-kinesis-client-multilang-2.3.9.jar";
    sha256 = "0sdw39p2fzypzimyczfa52cpjxn6h4mygblzg18qp4bn9idng8y3";
  };
  amazon_kinesis_client_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=software/amazon/kinesis/amazon-kinesis-client/2.3.9/amazon-kinesis-client-2.3.9.jar";
    sha256 = "1wddb85b9q8xl64angc5pyfx11qply4vsndrz835q8rh5rgh6iv1";
  };
  aws_java_sdk_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-core/1.12.3/aws-java-sdk-core-1.12.3.jar";
    sha256 = "0q6qc4zd114c2v78982q3565na5jx45a4l88gvp13n26mib6184s";
  };
  aws_java_sdk_sts_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/aws-java-sdk-sts/1.12.3/aws-java-sdk-sts-1.12.3.jar";
    sha256 = "0p6payabi6aphvwjj1r79vw6pvlph6i1j917x56ca2fp1qs63i88";
  };
  jmespath_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/amazonaws/jmespath-java/1.12.3/jmespath-java-1.12.3.jar";
    sha256 = "000mmnz8rv85nbbva9gzrsal8rz6zk9v94fxyn24q8n447y7yg4v";
  };
  jackson_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-annotations/2.12.4/jackson-annotations-2.12.4.jar";
    sha256 = "13pcs5p1jfw9fbq7n4flzb69bdzxbpv38cxcrmk9ns3mm033gapn";
  };
  jackson_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-core/2.12.4/jackson-core-2.12.4.jar";
    sha256 = "18v85pfxljhlgp01b533c2072krprgvhb5fph0nsw116xi3ww1im";
  };
  jackson_databind_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/core/jackson-databind/2.12.4/jackson-databind-2.12.4.jar";
    sha256 = "00bsiiaxqkp3ygd7jjf3qn6bc60k5hgypndwma4wcjq7i55pp6p9";
  };
  jackson_dataformat_cbor_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/fasterxml/jackson/dataformat/jackson-dataformat-cbor/2.12.4/jackson-dataformat-cbor-2.12.4.jar";
    sha256 = "09y8zs1rgdx15d7hgf26hci5q9bvmq1ww54hwwhxbq9507cp54f6";
  };
  netty_codec_http_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-codec-http/4.1.68.Final/netty-codec-http-4.1.68.Final.jar";
    sha256 = "19vfb0mlr43w0n9r7mbf3jlm7q88czzsfdiiapp9d6kzy1cgpi6p";
  };
  netty_codec_http2_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-codec-http2/4.1.68.Final/netty-codec-http2-4.1.68.Final.jar";
    sha256 = "0jslg5kj5mfln525jmnnh48s3wv11m4g3irf44dp798gqqpzz7l6";
  };
  netty_codec_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-codec/4.1.68.Final/netty-codec-4.1.68.Final.jar";
    sha256 = "109pkp7dm1knhddg9qp8rjpx6n2072i1miqyghbp79n2mdi0lga5";
  };
  netty_transport_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-transport/4.1.68.Final/netty-transport-4.1.68.Final.jar";
    sha256 = "1gdy7mjrc7ddnp8r2s92glh413yrkinqv9caghzrp9m6h4ah36ix";
  };
  netty_resolver_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-resolver/4.1.68.Final/netty-resolver-4.1.68.Final.jar";
    sha256 = "12z6ph64zwqrx4s9ywmg75q1hhjikg8al036mvbc4aqldl7fga3w";
  };
  netty_common_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-common/4.1.68.Final/netty-common-4.1.68.Final.jar";
    sha256 = "14px83f7a4gw3cfn9gpplnh1yrbnpc544ywy25x2q2ihdmzbr4nm";
  };
  netty_buffer_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-buffer/4.1.68.Final/netty-buffer-4.1.68.Final.jar";
    sha256 = "176fi9ln7m2h8wvs53qzwvf5wj06ss69n7wnmvsfp8cpsam1pg7w";
  };
  netty_handler_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-handler/4.1.68.Final/netty-handler-4.1.68.Final.jar";
    sha256 = "0byrwbgrnfn88nhdkbgqjbd9bp1si5ds8dp5gfl4833k89gs4hgg";
  };
  netty_transport_native_epoll_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-transport-native-epoll/4.1.68.Final/netty-transport-native-epoll-4.1.68.Final.jar";
    sha256 = "16sy8vqjsd3wgp0wfrx7v419dkn8kfp5s701xcm6l1rphi9gkmda";
  };
  netty_transport_native_unix_common_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/netty/netty-transport-native-unix-common/4.1.68.Final/netty-transport-native-unix-common-4.1.68.Final.jar";
    sha256 = "120nkm49zp7zm01jd8p8g4807577zah48x1wbls4g6hni9kcxrjn";
  };
  rxjava_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=io/reactivex/rxjava2/rxjava/2.2.21/rxjava-2.2.21.jar";
    sha256 = "072h516kigjzc5l55svgq7s86hqz9i7sx6l99h7qy0a0m10nbpsr";
  };
  jcommander_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/beust/jcommander/1.81/jcommander-1.81.jar";
    sha256 = "018swhr33fdc32y5iks8rck25x95zfhrpzh2j6lxmwwrkjbl52wx";
  };
  guava_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/guava/guava/31.0.1-jre/guava-31.0.1-jre.jar";
    sha256 = "1fc7y1dan9jqfg7j27f9iywa6mdagd8x2fhrnfgj3gc7bvb99gnm";
  };
  jsr305_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar";
    sha256 = "1iyh53li6y4b8gp8bl52fagqp8iqrkp4rmwa5jb8f9izg2hd4skn";
  };
  error_prone_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/errorprone/error_prone_annotations/2.7.1/error_prone_annotations-2.7.1.jar";
    sha256 = "1wygw4flzzzwlfj1r27nj7pr5q9bhb5p3bhpi1ighv14ib05flnd";
  };
  j2objc_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/j2objc/j2objc-annotations/1.3/j2objc-annotations-1.3.jar";
    sha256 = "0ysaws2dawf41raccmprx8vilr5nrh6d5d70q0i63gb74b4k1br1";
  };
  protobuf_java_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/google/protobuf/protobuf-java/3.17.1/protobuf-java-3.17.1.jar";
    sha256 = "1p4p4v0ncygw1dvys1kyss1mikaxd1y7axbk806nc9l3ng0cbkwx";
  };
  netty_reactive_streams_http_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/typesafe/netty/netty-reactive-streams-http/2.0.5/netty-reactive-streams-http-2.0.5.jar";
    sha256 = "00zkpiwmg6g3g3bqlz4y0zlybbc00cir9ng9fs0padnr39sj94mk";
  };
  netty_reactive_streams_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=com/typesafe/netty/netty-reactive-streams/2.0.5/netty-reactive-streams-2.0.5.jar";
    sha256 = "1mhkmi6x3jbx58xvhh193aipymq45vgkafmsd3jgsxgfr2gq8jgr";
  };
  commons_lang3_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar";
    sha256 = "0kp9qwqmqp45axxddf9h8ai9yap2j86dl4il366py0vc902dj6fr";
  };
  commons_collections4_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/commons/commons-collections4/4.4/commons-collections4-4.4.jar";
    sha256 = "1la610p7d0q8vadvxb8a82r72lzg6cz40pl1sx1x33jw1d1vky0x";
  };
  httpclient_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpclient/4.5.13/httpclient-4.5.13.jar";
    sha256 = "0hzp3vrxbnyc6w86v671wp0zchb634rgrwwcc00m0skcarm05sbg";
  };
  httpcore_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/apache/httpcomponents/httpcore/4.4.14/httpcore-4.4.14.jar";
    sha256 = "0a1vlr5r9w0bnxifv60jkbdxi79ywlivvpvn2z2x1c8c8ng20mpr";
  };
  checker_qual_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/checkerframework/checker-qual/2.5.2/checker-qual-2.5.2.jar";
    sha256 = "02h4iibbzqwy5i9bfqp6h5p2rsp7vi1fgqlf1xqfgm5rr28jdc34";
  };
  animal_sniffer_annotations_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/codehaus/mojo/animal-sniffer-annotations/1.20/animal-sniffer-annotations-1.20.jar";
    sha256 = "1b12fpkw0gz0d04jd0bpqr70jx6fw3qddlccq3svihidrbgl9pdy";
  };
  reactive_streams_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/reactivestreams/reactive-streams/1.0.3/reactive-streams-1.0.3.jar";
    sha256 = "0rfqf7slrj7gvfha0a8m07f8aq1g9phmbq93nqlwj69d0y0h9vhx";
  };
  slf4j_api_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=org/slf4j/slf4j-api/1.7.30/slf4j-api-1.7.30.jar";
    sha256 = "0msw2089azqdmhl3ki8r3pmxk3rgihg6np28c43hmd0v9nb0gfnd";
  };
  commons_beanutils_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-beanutils/commons-beanutils/1.9.4/commons-beanutils-1.9.4.jar";
    sha256 = "12in6a2q7m8rnmibvm90fr981hjzwx5yjrf011f08a4hg20qr4vx";
  };
  commons_codec_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-codec/commons-codec/1.15/commons-codec-1.15.jar";
    sha256 = "0qzd8v96j4x7jjcfpvvdh9ar1xhwxpxi2rh51nzhj0br7bbgdsdk";
  };
  commons_collections_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar";
    sha256 = "1f43ly6grlyfgchzz4smv1gmqp5acvzhsk0xfj5aci3ij4bykspf";
  };
  commons_io_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-io/commons-io/2.9.0/commons-io-2.9.0.jar";
    sha256 = "0caxa3i8aca8x7sbgg2sqil5r2nvyakgb1gj1ydwak1rkzajjy9w";
  };
  commons_logging_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=commons-logging/commons-logging/1.2/commons-logging-1.2.jar";
    sha256 = "0dm61zgmgjkg67kf9dyrzgpayd18r656n05kiabmc3xyl0gfmpfs";
  };
  logback_classic_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=ch/qos/logback/logback-classic/1.2.7/logback-classic-1.2.7.jar";
    sha256 = "0sir9w37cq5ycplfnm7px9178k9kyaq17n9rzaqr17lx0zbhbmpy";
  };
  logback_core_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=ch/qos/logback/logback-core/1.2.7/logback-core-1.2.7.jar";
    sha256 = "0f191jqxx5s5ffj63sarp8g0kac5q1h0cslxg7krymdyz4jssgkn";
  };
  joda_time_jar = inputs.nixpkgs.fetchurl {
    url = "https://search.maven.org/remotecontent?filepath=joda-time/joda-time/2.10.10/joda-time-2.10.10.jar";
    sha256 = "1qqpjrmk9q0vb93q160ym7zwh0v2kch32gwkgcdqsrss3297r3nx";
  };

  jars = [
    kinesis_jar
    annotations_jar
    apache_client_jar
    auth_jar
    aws_cbor_protocol_jar
    aws_core_jar
    aws_json_protocol_jar
    aws_query_protocol_jar
    cloudwatch_jar
    dynamodb_jar
    http_client_spi_jar
    json_utils_jar
    metrics_spi_jar
    netty_nio_client_jar
    protocol_core_jar
    profiles_jar
    regions_jar
    sdk_core_jar
    sts_jar
    third_party_jackson_core_jar
    third_party_jackson_dataformat_cbor_jar
    utils_jar
    eventstream_jar
    ion_java_jar
    schema_registry_serde_jar
    amazon_kinesis_client_multilang_jar
    amazon_kinesis_client_jar
    aws_java_sdk_core_jar
    aws_java_sdk_sts_jar
    jmespath_java_jar
    jackson_annotations_jar
    jackson_core_jar
    jackson_databind_jar
    jackson_dataformat_cbor_jar
    netty_codec_http_jar
    netty_codec_http2_jar
    netty_codec_jar
    netty_transport_jar
    netty_resolver_jar
    netty_common_jar
    netty_buffer_jar
    netty_handler_jar
    netty_transport_native_epoll_jar
    netty_transport_native_unix_common_jar
    rxjava_jar
    jcommander_jar
    guava_jar
    jsr305_jar
    error_prone_annotations_jar
    j2objc_annotations_jar
    protobuf_java_jar
    netty_reactive_streams_http_jar
    netty_reactive_streams_jar
    commons_lang3_jar
    commons_collections4_jar
    httpclient_jar
    httpcore_jar
    checker_qual_jar
    animal_sniffer_annotations_jar
    reactive_streams_jar
    slf4j_api_jar
    commons_beanutils_jar
    commons_codec_jar
    commons_collections_jar
    commons_io_jar
    commons_logging_jar
    logback_classic_jar
    logback_core_jar
    joda_time_jar
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
        --replace 'install_requires=PYTHON_REQUIREMENTS,' 'install_requires=[],' \
        --replace 'setup_requires=["pytest-runner"],' 'setup_requires=[],'
    '';
  })
