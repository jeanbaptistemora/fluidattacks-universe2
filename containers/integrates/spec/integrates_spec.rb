require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'
require 'serverspec_extended_types'

describe docker_build('.', tag: 'integrates-test', rm: TRUE) do

  it { should have_expose '80' }
  it { should have_expose '443' }

  describe docker_run('integrates-test', family: :debian) do

    describe package('apache2') do
      it { should be_installed }
    end

    describe service('apache2') do
      it { should be_enabled }
    end

    describe file('/etc/apache2/sites-available/000-default.conf') do
        it { should exist }
    end

    describe file('/etc/apache2/sites-available/integrates-ssl.conf') do
        it { should exist }
    end

    describe server(described_container) do # Infrataster
      describe http('http://localhost') do
        it 'responds content including "Please log in to proceed"' do
          expect(response.body).to include 'Please log in to proceed'
        end
      end
    end

  end
end
