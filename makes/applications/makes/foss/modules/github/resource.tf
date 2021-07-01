resource "github_actions_environment_secret" "dev" {
  for_each        = var.secrets_dev
  repository      = github_repository.repo.name
  environment     = github_repository_environment.dev.environment
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_actions_environment_secret" "prod" {
  for_each        = var.secrets_prod
  repository      = github_repository.repo.name
  environment     = github_repository_environment.prod.environment
  secret_name     = each.key
  plaintext_value = each.value
}

resource "github_branch_default" "default" {
  repository = github_repository.repo.name
  branch     = "main"
}

resource "github_branch_protection" "main" {
  allows_force_pushes    = false
  allows_deletions       = false
  enforce_admins         = false
  pattern                = "main"
  repository_id          = github_repository.repo.node_id
  require_signed_commits = false
  required_status_checks {
    strict   = false
    contexts = []
  }
}

resource "github_repository" "repo" {
  allow_merge_commit     = false
  allow_squash_merge     = false
  allow_rebase_merge     = true
  auto_init              = true
  delete_branch_on_merge = false
  description            = var.description
  has_downloads          = false
  has_issues             = true
  has_projects           = false
  has_wiki               = false
  homepage_url           = var.homepage
  is_template            = false
  license_template       = "mpl-2.0"
  name                   = var.name
  topics                 = var.topics
  vulnerability_alerts   = false
  visibility             = "public"
}

resource "github_repository_environment" "dev" {
  environment = "dev"
  repository  = github_repository.repo.name

  deployment_branch_policy {
    custom_branch_policies = false
    protected_branches     = true
  }

  reviewers {
    teams = [github_team.approvers.id]
  }
}

resource "github_repository_environment" "prod" {
  environment = "prod"
  repository  = github_repository.repo.name

  deployment_branch_policy {
    custom_branch_policies = false
    protected_branches     = true
  }
  reviewers {
    teams = [github_team.approvers.id]
  }
}

resource "github_team" "approvers" {
  name        = "approvers"
  description = "Approvers team"
  privacy     = "closed"
}
