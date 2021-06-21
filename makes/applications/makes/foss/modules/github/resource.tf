resource "github_repository" "repo" {
  allow_merge_commit     = false
  allow_squash_merge     = false
  allow_rebase_merge     = true
  auto_init              = false
  delete_branch_on_merge = false
  description            = var.description
  has_downloads          = false
  has_issues             = true
  has_projects           = false
  has_wiki               = false
  homepage_url           = var.homepage
  is_template            = false
  name                   = var.name
  topics                 = var.topics
  vulnerability_alerts   = false
  visibility             = "public"
}
