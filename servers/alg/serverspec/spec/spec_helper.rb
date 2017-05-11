require 'serverspec'
require 'net/ssh'
require 'pathname'
require 'bundler/setup'
require 'serverspec_extended_types'
require 'dockerspec/serverspec'


set :env, :LANG => 'C', :LC_MESSAGES => 'C'
set :path, '/sbin:/usr/local/sbin:$PATH'
