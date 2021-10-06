{ __nixpkgs__
, inputs
, makeRubyGemsEnvironment
, ...
}:
makeRubyGemsEnvironment {
  name = "integrates-mobile-tools-fastlane";
  ruby = "2.6";
  rubyGems = [
    {
      name = "addressable";
      version = "2.8.0";
      sha256 = "f76d29d2d1f54b6c6a49aec58f9583b08d97e088c227a3fcba92f6c6531d5908";
    }
    {
      name = "artifactory";
      version = "3.0.15";
      sha256 = "9aeaa82ad7be8057934abc3363cedc2009b576303e2be30b5f25730933f22e72";
    }
    {
      name = "atomos";
      version = "0.1.3";
      sha256 = "7d43b22f2454a36bace5532d30785b06de3711399cb1c6bf932573eda536789f";
    }
    {
      name = "aws-eventstream";
      version = "1.2.0";
      sha256 = "ffa53482c92880b001ff2fb06919b9bb82fd847cbb0fa244985d2ebb6dd0d1df";
    }
    {
      name = "aws-partitions";
      version = "1.503.0";
      sha256 = "0a2bfe2c6b8d583decdd2e379847c760d9eb8e1738a00c44b635af5b37e7b2fc";
    }
    {
      name = "aws-sdk-core";
      version = "3.121.0";
      sha256 = "886aa2d97080dae711bb18f0cb4ce00f2f1f9f3ab52d3c79526f54253bd0f4eb";
    }
    {
      name = "aws-sdk-kms";
      version = "1.48.0";
      sha256 = "2a3eb6a9bf16d7b31b86154615b715b3648101b3318cf56fd40892a6d6b04729";
    }
    {
      name = "aws-sdk-s3";
      version = "1.103.0";
      sha256 = "5816f08c0994d1cef35c3415925c728454457c9c26ebfab9a89353d7b4354af7";
    }
    {
      name = "aws-sigv4";
      version = "1.4.0";
      sha256 = "0a3be41096724a617fcfde8bb96f711c16335db42b9d2afc7a9f68b0d3f101f2";
    }
    {
      name = "babosa";
      version = "1.0.4";
      sha256 = "18dea450f595462ed7cb80595abd76b2e535db8c91b350f6c4b3d73986c5bc99";
    }
    {
      name = "bundler";
      version = "2.2.27";
      sha256 = "21d85c47937496b08b021df716b4eaa81e2223a04e8eba92ee9e767b9e1b3ed8";
    }
    {
      name = "CFPropertyList";
      version = "3.0.3";
      sha256 = "047f474797a1a71e7bf654e875bd836a9ffed3a47b641f1d83720db9504e4045";
    }
    {
      name = "claide";
      version = "1.0.3";
      sha256 = "1fbc84bad66bbde2058d13875f73a25fd1d252fa1620837563cf11a1abee5a4d";
    }
    {
      name = "colored";
      version = "1.2";
      sha256 = "9d82b47ac589ce7f6cab64b1f194a2009e9fd00c326a5357321f44afab2c1d2c";
    }
    {
      name = "colored2";
      version = "3.1.2";
      sha256 = "b13c2bd7eeae2cf7356a62501d398e72fde78780bd26aec6a979578293c28b4a";
    }
    {
      name = "commander-fastlane";
      version = "4.4.6";
      sha256 = "c5bc7152dce2ea9e00a2533cd13253dd07af1bcbc85d9bcd63a1729c981a0d79";
    }
    {
      name = "declarative";
      version = "0.0.20";
      sha256 = "8021dd6cb17ab2b61233c56903d3f5a259c5cf43c80ff332d447d395b17d9ff9";
    }
    {
      name = "digest-crc";
      version = "0.6.4";
      sha256 = "a283a60ad466f621b130c516a664df744207ee1b0283ec821fc1223eca54eab3";
    }
    {
      name = "domain_name";
      version = "0.5.20190701";
      sha256 = "000a600454cb4a344769b2f10b531765ea7bd3a304fe47ed12e5ca1eab969851";
    }
    {
      name = "dotenv";
      version = "2.7.6";
      sha256 = "2451ed5e8e43776d7a787e51d6f8903b98e446146c7ad143d5678cc2c409d547";
    }
    {
      name = "emoji_regex";
      version = "3.2.2";
      sha256 = "a78ce739dc298b32c8c1277bdfcd7b7b15a38179c8b7045cf63ee596588db897";
    }
    {
      name = "excon";
      version = "0.85.0";
      sha256 = "ea0c472e3231eed9d851c3dd8b4cacab66f8fe096ab4f86036a235230577d3c7";
    }
    {
      name = "faraday";
      version = "1.8.0";
      sha256 = "d1fb776cf25973b7f52a82b625bb0a009fe30ad6021ef838fb9109bf1ea6d029";
    }
    {
      name = "faraday-cookie_jar";
      version = "0.0.7";
      sha256 = "f3cbbe6f2de3d4028f00a67ae4196b99348a6dc3c065fdae6d3c7123fa8b1402";
    }
    {
      name = "faraday-em_http";
      version = "1.0.0";
      sha256 = "7a3d4c7079789121054f57e08cd4ef7e40ad1549b63101f38c7093a9d6c59689";
    }
    {
      name = "faraday-em_synchrony";
      version = "1.0.0";
      sha256 = "460dad1c30cc692d6e77d4c391ccadb4eca4854b315632cd7e560f74275cf9ed";
    }
    {
      name = "faraday-excon";
      version = "1.1.0";
      sha256 = "b055c842376734d7f74350fe8611542ae2000c5387348d9ba9708109d6e40940";
    }
    {
      name = "faraday-httpclient";
      version = "1.0.1";
      sha256 = "4c8ff1f0973ff835be8d043ef16aaf54f47f25b7578f6d916deee8399a04d33b";
    }
    {
      name = "faraday_middleware";
      version = "1.1.0";
      sha256 = "442288d81bdb48dccadf5463e256582850a2cc654ef5cd281f941c7b1cbcec4d";
    }
    {
      name = "faraday-net_http";
      version = "1.0.1";
      sha256 = "3245ce406ebb77b40e17a77bfa66191dda04be2fd4e13a78d8a4305854d328ba";
    }
    {
      name = "faraday-net_http_persistent";
      version = "1.2.0";
      sha256 = "0b0cbc8f03dab943c3e1cc58d8b7beb142d9df068b39c718cd83e39260348335";
    }
    {
      name = "faraday-patron";
      version = "1.0.0";
      sha256 = "dc2cd7b340bb3cc8e36bcb9e6e7eff43d134b6d526d5f3429c7a7680ddd38fa7";
    }
    {
      name = "faraday-rack";
      version = "1.0.0";
      sha256 = "ef60ec969a2bb95b8dbf24400155aee64a00fc8ba6c6a4d3968562bcc92328c0";
    }
    {
      name = "fastimage";
      version = "2.2.5";
      sha256 = "49334a947fc8b576b3e0031fb619a8da1ce40868a6f85479b48050e2f1732116";
    }
    {
      name = "fastlane";
      version = "2.172.0";
      sha256 = "ad64d27bc01126d684b7cf761b2e45414184edd1ee3a77132034f9d7b0203933";
    }
    {
      name = "gh_inspector";
      version = "1.1.3";
      sha256 = "04cca7171b87164e053aa43147971d3b7f500fcb58177698886b48a9fc4a1939";
    }
    {
      name = "google-api-client";
      version = "0.38.0";
      sha256 = "41a7dbc0cc33d7ad2864fc94c305fcec9ad95603a9cf9a7acf3d0310919ecbcb";
    }
    {
      name = "google-apis-core";
      version = "0.4.1";
      sha256 = "1e334ff47ce35680f0bb701abeaa94cbb48af77d7f62b96aa3293fca8c91ffdb";
    }
    {
      name = "google-apis-iamcredentials_v1";
      version = "0.7.0";
      sha256 = "0a12733683caa45271e3bf0f36e4b536dda621943f10eaa58a3203a13b65c931";
    }
    {
      name = "google-apis-storage_v1";
      version = "0.7.0";
      sha256 = "63fffe906ab8bb9a229cdf08b207a5acd0e0060630bc5165ceb5314423ca02dd";
    }
    {
      name = "googleauth";
      version = "0.17.1";
      sha256 = "d4a9cbce0d6b5fbb9e6f8e42c18ab44ea38594757952d94706461dabc4c28922";
    }
    {
      name = "google-cloud-core";
      version = "1.6.0";
      sha256 = "ea1744cd5a3085d3072de3fab9106afc769cd198609ebb5c6eeb5f13da46b72a";
    }
    {
      name = "google-cloud-env";
      version = "1.5.0";
      sha256 = "4fb9bfc49f68801c6218306972d079a6ba6770f8aeacba18f7863ccc091f4c2a";
    }
    {
      name = "google-cloud-errors";
      version = "1.2.0";
      sha256 = "6d47eb4cea8d6630bb2a30a5e4f5d0de338601a17f32e8afcccf4c66b9765359";
    }
    {
      name = "google-cloud-storage";
      version = "1.34.1";
      sha256 = "65dd9818d863276616b9a1b968c89404cbea73ff07a7fc5b01b533623abe6cdf";
    }
    {
      name = "highline";
      version = "1.7.10";
      sha256 = "1e147d5d20f1ad5b0e23357070d1e6d0904ae9f71c3c49e0234cf682ae3c2b06";
    }
    {
      name = "httpclient";
      version = "2.8.3";
      sha256 = "2951e4991214464c3e92107e46438527d23048e634f3aee91c719e0bdfaebda6";
    }
    {
      name = "http-cookie";
      version = "1.0.4";
      sha256 = "89a64e1b9e3ed823b559b2030e0b62ad850d0d11325a0589145ebf93d80267a4";
    }
    {
      name = "jmespath";
      version = "1.4.0";
      sha256 = "ee5930ed833d3472fce31abf2f4a39852718e90b099dc2a6713234d600539cb4";
    }
    {
      name = "json";
      version = "2.5.1";
      sha256 = "918d8c41dacb7cfdbe0c7bbd6014a5372f0cf1c454ca150e9f4010fe80cc3153";
    }
    {
      name = "jwt";
      version = "2.2.3";
      sha256 = "da2d43a5f7ff46037abd426574ce558adf1409ac83f09a88aee58804982bd10c";
    }
    {
      name = "memoist";
      version = "0.16.2";
      sha256 = "a52c53a3f25b5875151670b2f3fd44388633486dc0f09f9a7150ead1e3bf3c45";
    }
    {
      name = "mini_magick";
      version = "4.11.0";
      sha256 = "1a8abef753110e7362d221cad76046a52c701c1a144049979e37b5103a0146aa";
    }
    {
      name = "mini_mime";
      version = "1.1.1";
      sha256 = "d49f705f7d87721dd2aad2fa2787cd65ed5e2cefaa0d8495a13af48d37b96d9c";
    }
    {
      name = "multi_json";
      version = "1.15.0";
      sha256 = "1fd04138b6e4a90017e8d1b804c039031399866ff3fbabb7822aea367c78615d";
    }
    {
      name = "multipart-post";
      version = "2.0.0";
      sha256 = "3dc44e50d3df3d42da2b86272c568fd7b75c928d8af3cc5f9834e2e5d9586026";
    }
    {
      name = "nanaimo";
      version = "0.3.0";
      sha256 = "aaaedc60497070b864a7e220f7c4b4cad3a0daddda2c30055ba8dae306342376";
    }
    {
      name = "naturally";
      version = "2.2.1";
      sha256 = "a9b88c7d2fb06da3d9c51f4b885f35bac93d760178377809a31fcf67fab4a113";
    }
    {
      name = "os";
      version = "1.1.1";
      sha256 = "3db1fbc14ab8ea99b69ed8e353c894613e1b35e665fffb90414996cf8989d489";
    }
    {
      name = "plist";
      version = "3.6.0";
      sha256 = "f468bcf6b72ec6d1585ed6744eb4817c1932a5bf91895ed056e69b7f12ca10f2";
    }
    {
      name = "public_suffix";
      version = "4.0.6";
      sha256 = "a99967c7b2d1d2eb00e1142e60de06a1a6471e82af574b330e9af375e87c0cf7";
    }
    {
      name = "rake";
      version = "13.0.6";
      sha256 = "5ce4bf5037b4196c24ac62834d8db1ce175470391026bd9e557d669beeb19097";
    }
    {
      name = "representable";
      version = "3.1.1";
      sha256 = "dacfd01d46ee2c398cf78aa74a3269dd52adc38fdae32c3d3fe5fa4cd2ffbc27";
    }
    {
      name = "retriable";
      version = "3.1.2";
      sha256 = "0a5a5d0ca4ba61a76fb31a17ab8f7f80281beb040c329d34dfc137a1398688e0";
    }
    {
      name = "rexml";
      version = "3.2.5";
      sha256 = "a33c3bf95fda7983ec7f05054f3a985af41dbc25a0339843bd2479e93cabb123";
    }
    {
      name = "rouge";
      version = "2.0.7";
      sha256 = "2da14eb856839a81ad708883c2495507f50f973f3f46904cc7d87784039ed169";
    }
    {
      name = "ruby2_keywords";
      version = "0.0.5";
      sha256 = "ffd13740c573b7301cf7a2e61fc857b2a8e3d3aff32545d6f8300d8bae10e3ef";
    }
    {
      name = "rubyzip";
      version = "2.3.2";
      sha256 = "3f57e3935dc2255c414484fbf8d673b4909d8a6a57007ed754dde39342d2373f";
    }
    {
      name = "security";
      version = "0.1.3";
      sha256 = "aad3bcd890b065d1dbfafd6611dedd54714a2b701e0126fc5c991b2381eed2e7";
    }
    {
      name = "signet";
      version = "0.16.0";
      sha256 = "939464142cf004d379985a5dde3cc51cbb6c6b528f89ba379decce777353f531";
    }
    {
      name = "simctl";
      version = "1.6.8";
      sha256 = "1d80cfd5b5044e2e0d0ad945b57408d8cabd5cb6fd107d919bb3b0f26ad339ed";
    }
    {
      name = "slack-notifier";
      version = "2.4.0";
      sha256 = "cd9aba3f5f3e6227f73df1f6a33ac6c127c5fac35b513b86b7ba900cd98d2b00";
    }
    {
      name = "terminal-notifier";
      version = "2.0.0";
      sha256 = "7a0d2b2212ab9835c07f4b2e22a94cff64149dba1eed203c04835f7991078cea";
    }
    {
      name = "terminal-table";
      version = "1.8.0";
      sha256 = "13371f069af18e9baa4e44d404a4ada9301899ce0530c237ac1a96c19f652294";
    }
    {
      name = "trailblazer-option";
      version = "0.1.1";
      sha256 = "59c59c76d20e091f898509ad4f9c7c0017b5bea256b91cd73fa6818372caba79";
    }
    {
      name = "tty-cursor";
      version = "0.7.1";
      sha256 = "79534185e6a777888d88628b14b6a1fdf5154a603f285f80b1753e1908e0bf48";
    }
    {
      name = "tty-screen";
      version = "0.8.1";
      sha256 = "6508657c38f32bdca64880abe201ce237d80c94146e1f9b911cba3c7823659a2";
    }
    {
      name = "tty-spinner";
      version = "0.9.3";
      sha256 = "0e036f047b4ffb61f2aa45f5a770ec00b4d04130531558a94bfc5b192b570542";
    }
    {
      name = "uber";
      version = "0.1.0";
      sha256 = "5beeb407ff807b5db994f82fa9ee07cfceaa561dad8af20be880bc67eba935dc";
    }
    {
      name = "unf";
      version = "0.1.4";
      sha256 = "4999517a531f2a955750f8831941891f6158498ec9b6cb1c81ce89388e63022e";
    }
    {
      name = "unf_ext";
      version = "0.0.8";
      sha256 = "cd8f69915afccd3766400bf4f5f18038a57a75a2efde4c21fabfc96b6f8dab4a";
    }
    {
      name = "unicode-display_width";
      version = "1.8.0";
      sha256 = "0292132d364d59fcdd83f144910c48b3c8332b28a14c5c04bb093dd165600488";
    }
    {
      name = "webrick";
      version = "1.7.0";
      sha256 = "87e9b8e39947b7925338a5eb55427b11ce1f2b25a3645770ec9f39d8ebdb8cb4";
    }
    {
      name = "word_wrap";
      version = "1.0.0";
      sha256 = "f556d4224c812e371000f12a6ee8102e0daa724a314c3f246afaad76d82accc7";
    }
    {
      name = "xcodeproj";
      version = "1.21.0";
      sha256 = "e4e6130aa20d35aefc2ff1305dd0316f22c685051ff203f671775add6a58bf76";
    }
    {
      name = "xcpretty";
      version = "0.3.0";
      sha256 = "75c7cc577be3527e7663ca627cbeb47613904c3a44f34cca3a92d202053e04f7";
    }
    {
      name = "xcpretty-travis-formatter";
      version = "1.0.1";
      sha256 = "aacc332f17cb7b2cba222994e2adc74223db88724fe76341483ad3098e232f93";
    }
  ];
  searchPathsBuild = {
    bin = [
      __nixpkgs__.gcc
      inputs.nixpkgs.gnumake
      inputs.nixpkgs.rake
    ];
    rpath = [ __nixpkgs__.gcc.cc.lib ];
  };
}
