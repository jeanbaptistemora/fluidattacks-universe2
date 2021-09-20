{ makes
, ...
}:
makes.makeRubyGemsEnvironment {
  name = "integrates-tools-asciidoctor-pdf";
  ruby = "2.6";
  rubyGems = [
    {
      name = "addressable";
      version = "2.8.0";
      sha256 = "f76d29d2d1f54b6c6a49aec58f9583b08d97e088c227a3fcba92f6c6531d5908";
    }
    {
      name = "afm";
      version = "0.2.2";
      sha256 = "c83e698e759ab0063331ff84ca39c4673b03318f4ddcbe8e90177dd01e4c721a";
    }
    {
      name = "Ascii85";
      version = "1.1.0";
      sha256 = "9ce694467bd69ab2349768afd27c52ad721cdc6f642aeaa895717bfd7ada44b7";
    }
    {
      name = "asciidoctor";
      version = "2.0.16";
      sha256 = "02439a5b89b25550297a21c631035c2a6608d6fc9d9b63d7f137b3356bbd0482";
    }
    {
      name = "asciidoctor-pdf";
      version = "1.5.0.rc.3";
      sha256 = "a23affdbb49f94acd9f29a5c33cc9b79095eea9c0f0ecd14cfbe928d1c45ef56";
    }
    {
      name = "concurrent-ruby";
      version = "1.1.9";
      sha256 = "0ec0846d991c38f355b4228ad8ea77aa69c3fdaa320cd574dafedc10c4688a5b";
    }
    {
      name = "css_parser";
      version = "1.10.0";
      sha256 = "a5aef148ca782f999339f10ea0da152be7efe7c89afdc2b1feab0a36f9900fe1";
    }
    {
      name = "hashery";
      version = "2.1.2";
      sha256 = "d239cc2310401903f6b79d458c2bbef5bf74c46f3f974ae9c1061fb74a404862";
    }
    {
      name = "pdf-core";
      version = "0.7.0";
      sha256 = "c1afdbb79edaf7c9fea69fd4b8d3b2c68eeb7203ce4db0e80be5392e20e394a6";
    }
    {
      name = "pdf-reader";
      version = "2.5.0";
      sha256 = "7e1c36c086031e7219670646a44b02637ea053d75bd48bc918d6daa4f2909d91";
    }
    {
      name = "polyglot";
      version = "0.3.5";
      sha256 = "59d66ef5e3c166431c39cb8b7c1d02af419051352f27912f6a43981b3def16af";
    }
    {
      name = "prawn";
      version = "2.2.2";
      sha256 = "95284b761f0ea99334ef840ab85f577cfe2cc9448f769cc723843a6d7670b2e1";
    }
    {
      name = "prawn-icon";
      version = "2.5.0";
      sha256 = "dc88129676707c983e914ca2d2f066fb244e946075ed933c8422b996916b73c7";
    }
    {
      name = "prawn-svg";
      version = "0.30.0";
      sha256 = "e7d85c2b7c05427cfe9860c29db99ce9c935bd88158eb340e4b70fcf12a1c335";
    }
    {
      name = "prawn-table";
      version = "0.2.2";
      sha256 = "336d46e39e003f77bf973337a958af6a68300b941c85cb22288872dc2b36addb";
    }
    {
      name = "prawn-templates";
      version = "0.1.2";
      sha256 = "117aa03db570147cb86fcd7de4fd896994f702eada1d699848a9529a87cd31f1";
    }
    {
      name = "public_suffix";
      version = "4.0.6";
      sha256 = "a99967c7b2d1d2eb00e1142e60de06a1a6471e82af574b330e9af375e87c0cf7";
    }
    {
      name = "ruby-rc4";
      version = "0.1.5";
      sha256 = "00cc40a39d20b53f5459e7ea006a92cf584e9bc275e2a6f7aa1515510e896c03";
    }
    {
      name = "safe_yaml";
      version = "1.0.5";
      sha256 = "a6ac2d64b7eb027bdeeca1851fe7e7af0d668e133e8a88066a0c6f7087d9f848";
    }
    {
      name = "thread_safe";
      version = "0.3.6";
      sha256 = "9ed7072821b51c57e8d6b7011a8e282e25aeea3a4065eab326e43f66f063b05a";
    }
    {
      name = "treetop";
      version = "1.6.11";
      sha256 = "102e13adf065fc916eae60b9539a76101902a56e4283c847468eaea9c2c72719";
    }
    {
      name = "ttfunk";
      version = "1.5.1";
      sha256 = "8da1c20cc9e010a4b083376e6ae6996c4aa517558420bb23d9a1d8a228b6f9d5";
    }
  ];
}
