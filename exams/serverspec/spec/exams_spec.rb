require 'spec_helper'

describe port(80) do
  it { should be_listening }
end

describe port(3306) do
  it { should be_listening }
end

describe file('/var/lib/mysql') do
  it { should be_directory }
end

describe file('/var/lib/mysql/moodle') do
  it { should be_directory }
end

describe command('mysql -e "select version();"') do
  its(:stdout) { should contain "Access denied" }
end

describe user('exams') do
  it {should exist }
end

describe cron do
  it { should have_entry '"/usr/bin/php /var/www/html/admin/cli/cron.php >/dev/null"' }
end

describe service('apache2') do
  it { should be_enabled }
end

describe service('mysql-server') do
  it { should be_enabled }
end

