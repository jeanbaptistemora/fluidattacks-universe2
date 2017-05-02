require 'spec_helper'

describe network_acl('FLUIDServes VPC') do
  its(:inbound) { should be_allowed(80).protocol('tcp').source('0.0.0.0/0') }
  its(:inbound) { should be_allowed(443).protocol('tcp').source('0.0.0.0/0') }

  its(:outbound) { should be_allowed(80).protocol('tcp').source('0.0.0.0/0') }
  its(:outbound) { should be_allowed(443).protocol('tcp').source('0.0.0.0/0') }

end
