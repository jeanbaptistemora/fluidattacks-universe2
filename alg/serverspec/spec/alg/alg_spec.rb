require 'spec_helper'

packages = [
  'apache2',
  'ssh']

  describe "CentOS Operating System Checks for #{ENV['TARGET_HOST']}" do

    packages.each do|p|
      describe package(p) do
        it { should be_installed }
      end
    end