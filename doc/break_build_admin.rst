=================
Break Build Admin
=================

Ask an administrator for Continuous-Admin role in OKta.

Managing the service
====================

When a ${SUBS} is added
-----------------------

1. create:

   -  continuous/subscriptions/${SUBS}/break-build/dynamic/exploits/.gitkeep
   -  continuous/subscriptions/${SUBS}/break-build/static/exploits/.gitkeep

2. run:

   -  ``continuous $ toolbox --init-secrets``

3. commit your changes to the master branch
4. give the customer the credentials (see below) and CI commands to pull
   and run the container

When a ${SUBS} is finished/suspended
------------------------------------

1. Move the subscription folder in the continuous repository to the
   suspended/finished folder

Credentials
-----------

Credentials are created automatically for projects in the master branch.

Please save:

-  break_build_aws_access_key_id
-  break_build_aws_secret_access_key

In:

-  subscriptions/${SUBS}/config/secrets.yaml

Also give the customer the id and secret.

Get the credentials with the following commands:

.. code:: bash

   function get_break_build_credentials {
     local subs

     for args in "${@}"; do
       subs="${1}"
       shift 1 || break
       aws --profile continuous-admin s3 cp 's3://fluidattacks-terraform-states-prod/break-build.tfstate' - \
         | jq -r '.resources[] | select(.type == "aws_iam_access_key") ' \
         | jq -r '.instances[] | select(.index_key == "'${subs}'")' \
         | jq -r '.attributes | {
             subscription: "'${subs}'",
             break_build_aws_access_key_id: .id,
             break_build_aws_secret_access_key: .secret
           }'
     done
   }

   function get_break_build_id {
     local subs="${1}"

     get_break_build_credentials "${subs}" \
       | jq -r '.break_build_aws_access_key_id'
   }

   function get_break_build_secret {
     local subs="${1}"

     get_break_build_credentials "${subs}" \
       | jq -r '.break_build_aws_secret_access_key'
   }

Breaking the build
------------------

How a customer should run the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Documentation`_

How we should run the container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Exactly as the customer does.

However, it's useful to have the following functions:

.. code:: bash

   function run_break_build {
     # run the production static or dynamic container for a subscription
     #   run_break_build 'subscription-name' 'static'
     #   run_break_build 'subscription-name' 'dynamic'
     local subs="${1}"
     local type="${2}"
     local extra="${3}"

     docker pull fluidattacks/break-build
     bash <(docker run fluidattacks/break-build \
             ${extra} \
             --${type} \
             --no-image-rm \
             --id $(get_break_build_id "${subs}") \
             --secret $(get_break_build_secret "${subs}") \
             --cpus 0)
   }

   function run_break_build_test {
     # useful while developing the break-build container
     local subs="${1}"
     local type="${2}"
     local extra="${3}"

     docker build --tag test ./break-build/containers/break-build
     bash <(docker run test \
             ${extra} \
             --${type} \
             --no-image-rm \
             --id $(get_break_build_id "${subs}") \
             --secret $(get_break_build_secret "${subs}") \
             --cpus 0)
   }

.. _Documentation: https://fluidattacks.com/asserts/install/#inside-your-ci-continuous-integration-pipeline
