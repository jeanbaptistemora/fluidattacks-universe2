# shellcheck shell=bash

source "${srcIncludeHelpers}"

function helper_deploy_install_plugins_old {
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

function helper_deploy_install_plugins_new {
  local asciidoc='asciidoc_reader'
  local asciidoc_version='ad6d407'

  local others='assets neighbors representative_image sitemap'
  local others_version='666716e'

  local pelican_plugins_path='pelican-plugins'
  local url_pelican_plugins='https://github.com/getpelican/pelican-plugins.git'

      helper_git_sparse_checkout \
        "${asciidoc}" \
        "${asciidoc_version}" \
        "${pelican_plugins_path}" \
        "${url_pelican_plugins}" \
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

function helper_deploy_pages {
      rsync -av --progress content/pages/ new/content/pages/ --exclude contact-us \
        --exclude products --exclude services --exclude careers/* \
        --exclude defends --exclude findings --exclude location --exclude rules \
        --exclude subscription --exclude values --exclude reviews --exclude events \
        --exclude people --exclude partners \
  &&  rsync -av --progress content/pages/careers/ new/content/pages/careers/ \
  &&  sed -i "s|:template: faq||g" new/content/pages/careers/faq/index.adoc \
  &&  rsync -av --progress content/pages/services/certifications content/pages/services/differentiators \
        content/pages/values content/pages/reviews content/pages/events \
        content/pages/people content/pages/partners new/content/pages/about-us/ \
  &&  sed -i "s|:slug: services/|:slug: about-us/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: values/|:slug: about-us/values/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: reviews/|:slug: about-us/reviews/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: certifications/|:slug: about-us/certifications/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: events/|:slug: about-us/events/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: events/|:slug: about-us/events/|g" new/content/pages/about-us/events/*/index.adoc \
  &&  sed -i "s|:slug: people/|:slug: about-us/people/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: people/|:slug: about-us/people/|g" new/content/pages/about-us/people/*/index.adoc \
  &&  sed -i "s|:slug: partners/|:slug: about-us/partners/|g" new/content/pages/about-us/*/index.adoc \
  &&  sed -i "s|:slug: partners/terms|:slug: about-us/partners/terms|g" \
        new/content/pages/about-us/partners/terms/index.adoc \
  &&  sed -i "s|:category: services|:category: about us|g" new/content/pages/about-us/*/index.adoc \
  &&  rsync -av --progress content/blog/ new/content/blog/ \
  &&  rsync -av --progress content/images new/content/ \
  &&  sed -i "s|image:../images|image:../../images|g" new/content/pages/about-us/partners/index.adoc
}

function helper_deploy_compile_old {
  local target="${1}"

      env_prepare_python_packages \
  &&  npm install --prefix theme/2014/ \
  &&  PATH="${PATH}:$(pwd)/theme/2014/node_modules/.bin/" \
  &&  sed -i "s#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#" "theme/2014/node_modules/intl-tel-input/src/css/intlTelInput.scss" \
  &&  helper_deploy_install_plugins_old \
  &&  PATH="${PATH}:$(pwd)/theme/2014/node_modules/uglify-js/bin/" \
  &&  sed -i "s|https://fluidattacks.com|${target}|g" pelicanconf.py \
  &&  npm run --prefix theme/2014/ build \
  &&  cp -a "${STARTDIR}/cache" . || true \
  &&  echo '[INFO] Compiling site' \
  &&  pelican --fatal errors --fatal warnings content/ \
  &&  echo '[INFO] Finished compiling site' \
  &&  cp -a cache/ "${STARTDIR}" || true \
  &&  rm -rf output/web/de \
  &&  mv output/web/pages/* output/web/ \
  &&  rm -rf output/web/pages \
  &&  cp sitemap.xml output/sitemap.xml \
  &&  tail -n +6 output/web/sitemap.xml >> output/sitemap.xml \
  &&  rm output/web/sitemap.xml \
  &&  cp robots.txt output/robots.txt
}

function helper_deploy_compile_new {
  local target="${1}"
      helper_deploy_pages \
  &&  pushd new/ || return 1 \
  &&  env_prepare_python_packages \
  &&  helper_deploy_install_plugins_new \
  &&  sed -i "s|https://fluidattacks.com|${target}|g" pelicanconf.py \
  &&  npm install --prefix theme/2020/ \
  &&  npm run --prefix theme/2020/ build \
  &&  sed -i "s#\$flagsImagePath:.*#\$flagsImagePath:\ \"../../images/\";#" "theme/2020/node_modules/intl-tel-input/src/css/intlTelInput.scss" \
  &&  cp -a "${STARTDIR}/new/cache" . || true \
  &&  echo '[INFO] Compiling New site' \
  &&  pelican --fatal errors --fatal warnings content/ \
  &&  echo '[INFO] Finished compiling New site' \
  &&  cp -a cache/ "${STARTDIR}/new" || true \
  &&  rm -rf output/web \
  &&  mv output/newweb/pages/* output/newweb/ \
  &&  rm -rf output/newweb/pages \
  &&  popd || return 1
}

function helper_deploy_compile_all {
  local target="${1}"

      helper_deploy_compile_old "${target}" \
  &&  helper_deploy_compile_new "${target}" \
  &&  cp -a new/output/newweb output/
}
