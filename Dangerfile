# Version 1.0

# Get mr basic information
mr_info = gitlab.mr_json

# MR under 300 deltas
if git.lines_of_code > 300
  warn('MR should be under or equal to 300 deltas')
end

# Only one commit per MR
if git.commits.length > 1
  warn("This MR adds #{git.commits.length} commits.
    Only 1 commit per MR is recommended. Please use git squash")
end

# Check if the last pipeline was successful before opening MR
pipe = gitlab.api.merge_request_pipelines(mr_info['project_id'], mr_info['iid'])
if pipe[1].nil? || pipe[1].to_h['status'] != 'success'
  warn('A MR should only be created after a successful CI run in your branch')
end
