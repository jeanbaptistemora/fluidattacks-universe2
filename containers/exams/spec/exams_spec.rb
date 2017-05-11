require 'spec_helper'
require 'dockerspec/serverspec'

describe docker_run('fluidsignal/fluidservesexams:latest', family: 'debian') do

  describe file('/var/www/moodledata') do
    it { should be_directory }
  end

  describe file('/var/www/html') do
    it { should be_mode 755 }
  end

  describe cron do
    it { should have_entry '* * * * * /usr/bin/php /var/www/html/admin/cli/cron.php >/dev/null' }
  end

  describe service('apache2') do
    it { should be_enabled }
  end

  describe service('mysql') do
    it { should be_enabled }
  end

end
