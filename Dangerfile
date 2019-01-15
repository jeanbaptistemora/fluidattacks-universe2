# rubocop:disable Lint/MissingCopEnableDirective
# rubocop:disable Metrics/MethodLength
# rubocop:disable Metrics/AbcSize
# rubocop:disable Metrics/CyclomaticComplexity
# rubocop:disable Style/GuardClause

require 'pp'
require 'open3'

def environment
  # Get env vars
  @max_deltas = ENV['DANGER_MAX_DELTAS'].to_i

  # Get mr basic information
  @mr_info = gitlab.mr_json
  @mr_commit_msg = "#{gitlab.mr_title}\n\n#{gitlab.mr_body}"

  # Set local vars
  @mr_title_regex = /^(\w*)\((\w*)\):\s(#\d+)(.\d+)?\s(.*)$/i
  @mr_title_matches = gitlab.mr_title.match(@mr_title_regex).captures
  @relevances = {
    'revert' => 1,
    'feat' => 2,
    'perf' => 3,
    'fix' => 4,
    'refactor' => 5,
    'test' => 6,
    'docs' => 7,
    'style' => 8,
    'sltn' => 9
  }
end

def check_mr_under_max_deltas
  # MR under @max_deltas if commit is not solution
  if git.lines_of_code > @max_deltas
    failure "MR must be under or equal to #{@max_deltas} deltas"
    return false
  end
  true
end

def check_last_pipeline_successful
  # Check if the last pipeline was successful before opening MR
  pipeline =
    gitlab.api.merge_request_pipelines(@mr_info['project_id'], @mr_info['iid'])
  if pipeline[1].nil? || pipeline[1].to_h['status'] != 'success'
    failure 'A MR must only be created after a successful CI run in your branch'
    return false
  end
  true
end

def check_mr_message
  # Run commitlint on MR message
  command = "echo \"#{@mr_commit_msg}\" | npx commitlint"
  stdout, stderr, status = Open3.capture3(command)
  unless status.success?
    failure "Commitlint tests failed. MR Message must be syntax compliant.\n"\
            "**stdout:**\n"\
            "#{stdout}\n"\
            "**stderr:**\n"\
            "#{stderr}"
    return false
  end
  true
end

def check_mr_title_issue_part
  # Check if mr title has #N.N syntax
  unless @mr_title_matches[3].nil?
    failure "Your MR title messsage is not using the right syntax.\n"\
            "Use #{@mr_title_matches[2]} instead of "\
            "#{@mr_title_matches[2]}#{@mr_title_matches[3]}"
    return false
  end
  true
end

def check_branch_equals_to_user
  # Check if branch name differs from user name
  if @mr_info['source_branch'] != gitlab.mr_author
    failure "Your branch name must be equal to your gitlab user.\n\n"\
            "**Branch name**: #{@mr_info['source_branch']}\n"\
            "**Gitlab user**: #{gitlab.mr_author}"
    return false
  end
  true
end

def check_most_relevant_type
  # Check if MR message uses the most relevant type of all its commits
  commits =
    gitlab.api.merge_request_commits(@mr_info['project_id'], @mr_info['iid'])
  mr_title_type = @mr_title_matches[0]
  most_relevant_type = 'sltn'
  commits.each do |commit|
    commit_title_type = commit.to_h['title'].match(@mr_title_regex).captures[0]
    most_relevant_type = commit_title_type if
      @relevances.key?(commit_title_type) &&
      @relevances[commit_title_type] < @relevances[most_relevant_type]
  end
  if mr_title_type != most_relevant_type
    fail_msg = 'The most relevant type of all commits included in your MR is: '\
               "**#{most_relevant_type}**.\n"\
               'The type used in your MR title is: '\
               "**#{mr_title_type}**.\n"\
               "Please make sure to change it.\n\n"\
               "The relevance order is (from highest to lowest):\n\n"
    @relevances.each_key { |type| fail_msg << "    #{type}\n" }
    failure fail_msg
    return false
  end
  true
end

def check_one_commit_per_mr
  # Only one commit per MR
  if git.commits.length > 1
    warn "This MR adds #{git.commits.length} commits."\
         'Only one commit per MR is recommended. Make sure to use git squash'
  end
end

def check_close_issue_directive
  # Checks if a MR has an issue different from #0 without a Closes directive
  if @mr_title_matches[2] != '#0' && !gitlab.mr_body.include?('Closes #')
    warn "This MR is referencing issue #{@mr_title_matches[2]} "\
         "but it does not have a ``Closes #{@mr_title_matches[2]}`` "\
         'in its footer. Was this intentional?'
  end
end

def thank_you_message(pass)
  if pass
    message "Hi #{@mr_info['author']['name']}\n\n"\
            'Thank you for posting this MR to the repo! '\
            ":tada: :tada: :tada:.\n"\
            'Please be patient while our maintainers review it :spy\\_tone2:.'
  else
    message "Hi #{@mr_info['author']['name']}\n\n"\
            "Unfortunately, your MR did not pass my automated tests :robot:.\n"\
            'Please make sure to check my failure messages and repair them '\
            "before posting it again.\n"\
            'If you think there is a bug :beetle:, '\
            'please contact a repo maintainer.'
  end
end

def run_checks
  # Run checks that produce failure
  pass = true
  pass = check_mr_under_max_deltas && pass
  pass = check_last_pipeline_successful && pass
  pass = check_mr_message && pass
  pass = check_mr_title_issue_part && pass
  pass = check_branch_equals_to_user && pass
  pass = check_most_relevant_type && pass

  # Run other checks
  check_one_commit_per_mr
  check_close_issue_directive

  pass
end

environment
thank_you_message(run_checks)
