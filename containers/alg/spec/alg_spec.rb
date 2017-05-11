require 'spec_helper'
require 'dockerspec/serverspec'

set :docker_compose_container, :alg
describe docker_build('.', tag: 'alg') do
  describe docker_run('alg') do
    set :docker_compose_container, :alg
    case os[:family]
    when 'debian'

      describe command('ls /etc/apache2/sites-enabled') do
        its(:stdout) { should eq "000-default.conf  default-ssl  fluid.la  www.fluid.la  www.fluidsignal.com\n"}
      end

      describe command("lsb_release -d") do
        its(:stdout) { should   contain /jessie/ }
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
        it {should contain 'ProxyPassReverse /blog'}
        it {should contain 'ProxyPassReverse /sitemap.xml'}
        it {should contain 'ProxyPassReverse /courses'}
        it {should contain 'ProxyPassReverse /forms'}
        it {should contain 'ProxyPassReverse /kb'}
        it {should contain 'SSLProxyEngine on'}
      end

      describe file('/var/www/html/index.html') do
        it { should_not exist }
      end

      describe file ('/etc/apache2/apache2.conf') do
        it {should contain 'ServerTokens ProductOnly'}
        it {should contain 'ServerSignature Off'}
      end

    end
  end
end
