# shellcheck shell=bash

function helper_airs_deploy_install_plugins {
  local asciidoc='asciidoc_reader'
  local asciidoc_version='ad6d407'

  local tipuesearch='assets/tipuesearch/tipuesearch.min.js assets/tipuesearch/tipuesearch_set.js'
  local tipuesearch_version='d4b5df7'

  local others='assets neighbors share_post representative_image sitemap tag_cloud tipue_search'
  local others_version='666716e'

  local pelican_plugins_path='pelican-plugins'
  local url_pelican_plugins='https://github.com/getpelican/pelican-plugins.git'

  local js_plugins_path='theme/2020/static/js'
  local url_tipuesearch_plugin='https://github.com/jekylltools/jekyll-tipue-search.git'

      helper_airs_git_sparse_checkout \
        "${asciidoc}" \
        "${asciidoc_version}" \
        "${pelican_plugins_path}" \
        "${url_pelican_plugins}" \
  &&  helper_airs_git_sparse_checkout \
        "${tipuesearch}" \
        "${tipuesearch_version}" \
        "${js_plugins_path}" \
        "${url_tipuesearch_plugin}" \
  &&  helper_airs_git_sparse_checkout \
        "${others}" \
        "${others_version}" \
        "${pelican_plugins_path}" \
        "${url_pelican_plugins}"
}

function helper_airs_compile {
  local target="${1}"

      env_prepare_python_packages \
  &&  helper_airs_deploy_install_plugins \
  &&  sed -i "s|https://fluidattacks.com|${target}|g" pelicanconf.py \
  &&  npm install --prefix theme/2020/ \
  &&  PATH="${PATH}:$(pwd)/theme/2020/node_modules/.bin/" \
  &&  PATH="${PATH}:$(pwd)/theme/2020/node_modules/uglify-js/bin/" \
  &&  npm run --prefix theme/2020/ build \
  &&  sed --in-place \
        "s/airs_version/${CI_COMMIT_SHORT_SHA}/g" \
        "theme/2020/static/js/tmp/bugsnagErrorBoundary.min.js" \
  &&  sed -i "s#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#" "theme/2020/node_modules/intl-tel-input/src/css/intlTelInput.scss" \
  &&  cp -a "${STARTDIR}/airs/cache" . || true \
  &&  echo '[INFO] Compiling website' \
  &&  pelican --fatal errors --fatal warnings content/ \
  &&  echo '[INFO] Finished compiling website' \
  &&  cp -a cache/ "${STARTDIR}/airs" || true \
  &&  rm -rf output/de \
  &&  mv output/pages/* output/ \
  &&  rm -rf output/pages \
  &&  cp robots.txt output/ \
  &&  rsync content/files/* output/ \
  &&  cp -r content/files/.well-known output/
}
