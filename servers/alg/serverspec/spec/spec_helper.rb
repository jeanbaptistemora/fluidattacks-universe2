require 'serverspec'
require 'net/ssh'
require 'pathname'
require 'bundler/setup'
require 'serverspec_extended_types'
require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

set :env, :LANG => 'C', :LC_MESSAGES => 'C'
set :path, '/sbin:/usr/local/sbin:$PATH'
