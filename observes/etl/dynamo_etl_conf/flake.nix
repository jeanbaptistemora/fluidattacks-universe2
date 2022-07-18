{
  description = "Dynamo ETLs configuration";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    purity.url = "gitlab:dmurciaatfluid/purity/tags/v1.22.1";
    purity.inputs.nixpkgs.follows = "nixpkgs";
    redshift_client.url = "gitlab:dmurciaatfluid/redshift_client/tags/v0.10.0";
    redshift_client.inputs.nixpkgs.follows = "nixpkgs";
    redshift_client.inputs.purity.follows = "purity";
  };
  outputs = {
    self,
    nixpkgs,
    purity,
    redshift_client,
  }: let
    system = "x86_64-linux";
    out = python_version:
      import self {
        inherit python_version;
        nixpkgs =
          nixpkgs.legacyPackages."${system}"
          // {
            fa_purity = purity.packages."${system}";
            redshift_client = redshift_client.packages."${system}";
          };
        src = self;
      };
  in {
    packages."${system}" = out "python310";
    defaultPackage."${system}" = self.packages."${system}".pkg;
  };
}
