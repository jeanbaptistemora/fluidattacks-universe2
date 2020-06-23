repo = 'fluidattacks/public'
branch = 'master'
path = 'dangerfiles/Dangerfile.others'
danger.import_dangerfile(github: repo, branch: branch, path: path)

if git.modified_files.select { |path| path.include? "mobile/" }.length > 0
  if git.modified_files.include? 'mobile/app.json'
    warn "OTA-N: This change requires to build and deploy a new app binary"
  else
    message "OTA-Y: This change will be deployed via OTA"
  end
end
