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
  its(:stdout) { should ="ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)" } 
end
