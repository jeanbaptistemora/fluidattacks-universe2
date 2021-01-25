# shellcheck shell=bash

function load_base {
      echo '[INFO] Setting up base development environment' \
  &&  source '__envBaseSearchPaths__' \
  &&  echo '[INFO] ---' \
  &&  echo '[INFO] You can now execute `load_<product>`' \
  &&  echo '[INFO]   in order to make available all deps required to develop such product' \
  &&  echo '[INFO]' \
  &&  echo '[INFO] Aliases:'  \
  &&  echo '[INFO]   a: add git changes, hunk by hunk' \
  &&  alias a='git add -p' \
  &&  echo '[INFO]   c: create a new commit' \
  &&  alias c='git commit --allow-empty' \
  &&  echo '[INFO]   f: fetch changes from remote (useful for peer review)' \
  &&  alias f='git fetch --all' \
  &&  echo '[INFO]   l: git log' \
  &&  alias l='git log' \
  &&  echo '[INFO]   m: add your added changes to the last commit' \
  &&  alias m='git commit --amend --no-edit --allow-empty' \
  &&  echo '[INFO]   p: push changes to your branch' \
  &&  alias p='git push -f' \
  &&  echo '[INFO]   r: rebase' \
  &&  alias r='git pull --autostash --progress --rebase --stat origin master' \
  &&  echo '[INFO]   rp: r and then p' \
  &&  alias rp='r && p' \
  &&  echo '[INFO]   s: git status' \
  &&  alias s='git status' \

}

function load_skims {
      echo '[INFO] Setting up Skims development environment' \
  &&  source '__envSkimsSetupDevelopment__' \
  &&  source '__envSkimsSetupRuntime__'
}

load_base
