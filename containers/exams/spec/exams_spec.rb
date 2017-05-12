require 'dockerspec'
require 'dockerspec/serverspec'
require 'dockerspec/infrataster'

describe docker_build('.', tag: 'exams-test', rm: TRUE) do

  it { should have_expose '80' }

  describe docker_run('exams-test', family: :debian) do

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

      describe server(described_container) do # Infrataster
        describe http('http://localhost') do
          it 'responds content including "This page should automatically redirect."' do
            expect(response.body).to include 'This page should automatically redirect.'
          end
        end
      end

  end
end
