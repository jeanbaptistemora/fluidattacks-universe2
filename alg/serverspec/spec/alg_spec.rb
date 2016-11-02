require 'spec_helper'

describe port(443) do
  it { should be_listening }
end

describe port(80) do
  it { should be_listening }
end

describe command('ls /etc/apache2/sites-enabled') do
  its(:stdout) { should eq "000-default.conf  default-ssl  fluid.la\n"}
end

#describe command("lsb_release -d") do
#  it { should return_stdout /jessie/ }
#end

#describe package(apache) do
#  it { should be_installed }
#end

#describe service(apache) do
#  it { should be_enabled }
#end
