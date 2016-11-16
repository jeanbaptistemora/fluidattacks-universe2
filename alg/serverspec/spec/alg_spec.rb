require 'spec_helper'

describe port(443) do
  it { should be_listening }
end

describe port(80) do
  it { should be_listening }
end

describe command('ls /etc/apache2/sites-enabled') do
  its(:stdout) { should eq "000-default.conf  default-ssl  fluid.la  www.fluid.la\n"}
end

describe command("lsb_release -d") do
  its(:stdout) { should contain /jessie/ }
end

describe package('apache2') do
  it { should be_installed }
end

describe service('apache2') do
  it { should be_enabled }
end

describe user('root') do 
  it {should exist }
end

describe file ('/etc/apache2/sites-enabled/default-ssl') do
  it {should contain 'ProxyPass /blog'}
  it {should contain 'ProxyPass /sitemap.xml'}
  it {should contain 'ProxyPass /courses'}
  it {should contain 'ProxyPass /forms'}
  it {should contain 'ProxyPass /kb'}
  it {should contain 'ProxyPassReverse /es'}
  it {should contain 'ProxyPassReverse /en'}
  it {should contain 'SSLProxyEngine on'}
end


