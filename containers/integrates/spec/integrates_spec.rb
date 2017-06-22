require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'integrates-test', rm: TRUE) do

  describe docker_run('integrates-test', family: :debian) do

    describe package('apache2') do
      it { should be_installed }
    end

    end
end
