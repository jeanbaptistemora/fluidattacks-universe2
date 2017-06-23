require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'base-test', rm: TRUE) do

  describe docker_run('alg-test', family: :debian) do

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

  end
end
