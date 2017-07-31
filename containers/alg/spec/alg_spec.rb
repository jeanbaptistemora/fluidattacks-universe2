require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'alg-test', rm: TRUE) do

  it { should have_expose '80' }
  it { should have_expose '443' }

  describe docker_run('alg-test', family: :debian) do

    describe command('ls /etc/apache2/sites-enabled') do
      its(:stdout) { should eq "000-default.conf\ndefault-ssl\nfluid.la\nwww.fluid.la\nfluidsignal.com\nfluidsignal.com.co\nfluidsignal.co\nfluid.com.co"}
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

    describe server(described_container) do # Infrataster
      describe http('http://localhost/') do
        it 'responds content including "<a href="https://fluid.la/">here"' do
          expect(response.body).to include '<a href="https://fluid.la/">here'
        end
      end
    end

  end
end
