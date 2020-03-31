# shellcheck shell=bash

source "${srcIncludeHelpers}"

function helper_deploy_install_plugins {
  local asciidoc='asciidoc_reader'
  local asciidoc_version='ad6d407'

  local tipuesearch='assets/tipuesearch/tipuesearch.min.js assets/tipuesearch/tipuesearch_set.js'
  local tipuesearch_version='d4b5df7'

  local others='assets neighbors share_post related_posts representative_image tipue_search sitemap i18n_subsites tag_cloud'
  local others_version='666716e'

  local pelican_plugins_path='pelican-plugins'
  local url_pelican_plugins='https://github.com/getpelican/pelican-plugins.git'

  local js_plugins_path='theme/2014/static/js'
  local url_tipuesearch_plugin='https://github.com/jekylltools/jekyll-tipue-search.git'

      helper_git_sparse_checkout \
        "${asciidoc}" \
        "${asciidoc_version}" \
        "${pelican_plugins_path}" \
        "${url_pelican_plugins}" \
  &&  helper_git_sparse_checkout \
        "${tipuesearch}" \
        "${tipuesearch_version}" \
        "${js_plugins_path}" \
        "${url_tipuesearch_plugin}" \
  &&  helper_git_sparse_checkout \
        "${others}" \
        "${others_version}" \
        "${pelican_plugins_path}" \
        "${url_pelican_plugins}"
}

function helper_deploy_sync_s3 {
  local source_code="${1}"
  local bucket_path="${2}"
  local extensions=('html' 'css' 'js' 'png' 'svg')
  local files_to_compress
  local compress
  local content_type

      files_to_compress="$(find "${source_code}" -type f -name '*.html' -o -name '*.css' -o -name '*.js')" \
  &&  for file in ${files_to_compress}
      do
            gzip -9 "${file}" \
        &&  mv "${file}.gz" "${file}" \
        || return 1
      done \
  &&  for extension in "${extensions[@]}"
      do
            case ${extension} in
              'html')
                    content_type='text/html' \
                &&  compress='gzip'
                    ;;
              'css')
                    content_type='text/css' \
                &&  compress='gzip'
                    ;;
              'js')
                    content_type='application/javascript' \
                &&  compress='gzip'
                    ;;
              'png')
                    content_type='image/png' \
                &&  compress='identity'
                    ;;
              'svg')
                    content_type='image/svg+xml' \
                &&  compress='identity'
                    ;;
              *)
                    content_type='application/octet-stream' \
                &&  compress='identity'
                    ;;
            esac \
        &&  aws s3 sync                        \
              "${source_code}/"                \
              "s3://${bucket_path}/"           \
              --acl public-read                \
              --exclude "*"                    \
              --include "*.${extension}"       \
              --metadata-directive REPLACE     \
              --content-type "${content_type}" \
              --content-encoding "${compress}" \
              --delete \
        ||  return 1
      done \
  &&  aws s3 sync \
        "${source_code}/"      \
        "s3://${bucket_path}/" \
        --exclude "*.html"     \
        --exclude "*.css"      \
        --exclude "*.js"       \
        --exclude "*.png"      \
        --exclude "*.svg"      \
        --delete
}

function helper_deploy_compile_site {
  local target="${1}"
  local base_folder='deploy/builder'

      helper_use_pristine_workdir \
  &&  env_prepare_python_packages \
  &&  npm install --prefix "${base_folder}" \
  &&  PATH="${PATH}:$(pwd)/${base_folder}/node_modules/.bin/" \
  &&  sed -i "s#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#" "${base_folder}/node_modules/intl-tel-input/src/css/intlTelInput.scss" \
  &&  helper_deploy_install_plugins \
  &&  PATH="${PATH}:$(pwd)/${base_folder}/node_modules/uglify-js/bin/" \
  &&  cp -a "${base_folder}/node_modules" theme/2014/ \
  &&  sed -i "s|https://fluidattacks.com|${target}|g" pelicanconf.py \
  &&  sed -i "s|/app/pelican-plugins|pelican-plugins|g" pelicanconf.py \
  &&  sed -i "s|/app/js/|js/|g" theme/2014/templates/base.html \
  &&  sed -i "s|/app/deploy/builder/node_modules/|../node_modules/|g" theme/2014/templates/base.html \
  &&  sed -i "s|/app/deploy/builder/node_modules/|../node_modules/|g" theme/2014/templates/contact.html \
  &&  npm run --prefix "${base_folder}" build \
  &&  cp -a "${STARTDIR}/cache" . || true \
  &&  ./build-site.sh \
  &&  cp -a cache/ "${STARTDIR}" || true \
  &&  cp -a "${base_folder}/node_modules" new/theme/2014/ \
  &&  cp -a "${base_folder}/node_modules" new/ \
  &&  sed -i "s|https://fluidattacks.com|${target}|g" new/pelicanconf.py \
  &&  sed -i "s|/app/pelican-plugins|../pelican-plugins|g" new/pelicanconf.py \
  &&  pushd new/ || return 1 \
  &&  npm run --prefix "../${base_folder}" build-new \
  &&  cp -a "${STARTDIR}/new/cache" . || true \
  &&  ./build-site.sh \
  &&  cp -a cache/ "${STARTDIR}/new" || true \
  &&  popd || return 1 \
  &&  cp -a new/output/newweb output/
}
