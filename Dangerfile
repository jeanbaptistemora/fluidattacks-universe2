repo = 'fluidattacks/public'
branch = 'master'
path = 'dangerfiles/Dangerfile.others'
danger.import_dangerfile(github: repo, branch: branch, path: path)

if git.modified_files.select { |path| path.include? "mobile/" }.length > 0
  if git.modified_files.include? 'mobile/app.json'
    warn "OTA-N: This change requires to build and deploy a new app binary"
  else
    expo_url = "@developmentatfluid/integrates?"\
               "release-channel=#{@mr_info['source_branch']}"
    message "OTA-Y: This change will be deployed via OTA. \n"\
            "You can [review it here](https://expo.io/#{expo_url}) "\
            "or by scanning the following QR code: \n\n"\
            "![qr](https://api.qrserver.com/v1/create-qr-code/"\
            "?size=200x200&data=exp://exp.host/#{expo_url})"
  end
end
