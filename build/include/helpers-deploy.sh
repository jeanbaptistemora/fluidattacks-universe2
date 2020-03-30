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

  local js_plugins_path='js'
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
