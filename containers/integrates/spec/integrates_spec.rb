require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'integrates-test', rm: TRUE) do

  it { should have_expose '443' }

  describe docker_run('integrates-test', family: :debian) do

    describe package('apache2') do
      it { should be_installed }
    end

    describe service('apache2') do
      it { should be_enabled }
    end

    end
end
