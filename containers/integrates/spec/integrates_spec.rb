require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'integrates-test', rm: TRUE) do

  it { should have_expose '80' }

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

    describe server(described_container) do # Infrataster
      describe http('http://localhost') do
        it 'responds content including "Please enter your user information."' do
          expect(response.body).to include 'Please enter your user information.'
        end
      end
    end

  end
end
