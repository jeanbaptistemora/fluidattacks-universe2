{ fetchGithub
, ...
}:
{
  inputs = {
    skimsBenchmarkOwaspRepo = fetchGithub {
      owner = "owasp";
      repo = "benchmark";
      rev = "1cfe52ea6dc49bebae12e6ceb20356196f0e9ac8";
      sha256 = "pcNMJJJ2cRxh4Kgq0ElOIyBJemJu4qggxY3Debjbcms=";
    };
  };
}
