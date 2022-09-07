# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makeRubyGemsEnvironment, ...}:
makeRubyGemsEnvironment {
  name = "integrates-tools-concurrent-ruby";
  ruby = "2.7";
  rubyGems = [
    {
      name = "concurrent-ruby";
      sha256 = "094387x4yasb797mv07cs3g6f08y56virc2rjcpb1k79rzaj3nhl";
      version = "1.1.6";
    }
  ];
}
