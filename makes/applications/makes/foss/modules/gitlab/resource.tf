resource "gitlab_project" "project" {
  archived                                         = false
  approvals_before_merge                           = 1
  container_registry_enabled                       = false
  default_branch                                   = "main"
  description                                      = var.description
  initialize_with_readme                           = false
  issues_enabled                                   = true
  lfs_enabled                                      = false
  merge_method                                     = "ff"
  merge_requests_enabled                           = true
  mirror                                           = false
  mirror_overwrites_diverged_branches              = true
  mirror_trigger_builds                            = false
  name                                             = var.name
  namespace_id                                     = data.gitlab_group.group.id
  only_allow_merge_if_pipeline_succeeds            = true
  only_allow_merge_if_all_discussions_are_resolved = true
  only_mirror_protected_branches                   = true
  packages_enabled                                 = false
  pages_access_level                               = "disabled"
  path                                             = var.name
  pipelines_enabled                                = true
  request_access_enabled                           = true
  shared_runners_enabled                           = false
  snippets_enabled                                 = false
  visibility_level                                 = "public"
  wiki_enabled                                     = false

  push_rules {
    deny_delete_tag = true
    prevent_secrets = true
  }
}
