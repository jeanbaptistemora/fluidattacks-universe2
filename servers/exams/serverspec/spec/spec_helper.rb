require 'serverspec'
require 'net/ssh'
require 'pathname'
require 'bundler/setup'

RSpec.configure do |config|
  set :host,  '127.0.0.1'
  set :ssh_options, :user => 'root', :port => 22001, :host_key => 'ssh-rsa', :keys => '~/.ssh/exams_facont_id_rsa'
  set :backend, :ssh
  set :request_pty, true
end

set :env, :LANG => 'C', :LC_MESSAGES => 'C'
set :path, '/sbin:/usr/local/sbin:$PATH'

