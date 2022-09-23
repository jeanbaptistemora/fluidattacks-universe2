# SPDX-FileCopyrightText: 2022 "Fluid Attacks <development@fluidattacks.com>"
#
# SPDX-License-Identifier: MPL-2.0
{python_pkgs}:
python_pkgs.oscrypto.overridePythonAttrs (
  _: {
    postPatch = ''
      substituteInPlace oscrypto/_openssl/_libcrypto_cffi.py \
      --replace "libcrypto_path = _backend_config().get('libcrypto_path')" "libcrypto_path = 'libcrypto.so.1.1'"
    '';
  }
)
