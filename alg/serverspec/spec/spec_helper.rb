require 'serverspec'
require 'net/ssh'
require 'pathname'
require 'bundler/setup'

RSpec.configure do |config|
  set :host,  ENV['TARGET_HOST']
    set :ssh_options, :user => 'root', :port => 22000, :paranoid => false, :verbose => :error, :host_key => 'ssh-rsa', :keys => '~/.ssh/config.facont.alg'
  set :backend, :ssh
  set :request_pty, true
end
set :env, :LANG => 'C', :LC_MESSAGES => 'C'
set :path, '/sbin:/usr/local/sbin:$PATH'

