================================
Developing exploits with secrets
================================

Requirements
============

At least once a day:

1. Rebase your local changes to the **master** branch
2. Update your **subscription repositories**
3. Update your **fluid-cli** and the **utilities** package:

   Example:

   .. code:: bash

       continuous $ python3 -m pip install --user --upgrade fluidattacks[with_everything]
       continuous $ python3 -m pip install --user --upgrade forces/packages/*

Hands-on tutorial
=================

We are going to create this portion of the manual for the **some-subs-name**
subscription. Replace it when necessary for your own subscription.

Key concepts
------------

Secrets are managed in the exploit via an **encrypted YAML** file, these
encrypted YAML files look something like this:

.. code:: yaml

    secrets:
      test_user: gAAAAABdp3GJPNLES8B0FkDtOyCdlWRRfvxPSn9fBZNgW6AbndwXzpgy15wDZ9aT9yNdPyNUfERcpdparN7XjsgOFDFVug3NRg==
      test_password: gAAAAABdp3GJFVUe-xkFqwVFGnVu54dmbdCCbjsuFAeGAUfxe3MHCK4npc3myoXNIjz_CM0Al6tLccMg4wuaTPwn0d526dXcpQ==

This is nothing more than a clear text **key-value** file where the
**values** have been encrypted with the **customer secret**.

The original file is:

.. code:: yaml

    secrets:
      test_user: Einstein
      test_password: E=m*C^2

You are going to upload the **encrypted YAML** file to the continuous
repository, and this file is going to be placed in the Docker Image for
the subscription.

Once in the customer's hands, the customer (via an script that we wrote)
is going to decrypt this file using its **secret**, and the exploits are
going to use the **decrypted values** to perform the security checks.

If your are going to add secrets for the first time
---------------------------------------------------

We need to create two dummy secret files, once created we'll add our
secrets, and encrypt them:

Let's generate them:

.. code:: bash

    kamado@fluid:/continuous$ fluid forces --init-secrets <some-subs-name>


.. code:: bash

    Initializing subscriptions/some-subs-name/forces/static/resources/plaintext.yml
      Done!
    Initializing subscriptions/some-subs-name/forces/dynamic/resources/plaintext.yml
      Done!
    Moving secrets from subscriptions/some-subs-name/forces/static/resources/plaintext.yml to subscriptions/some-subs-name/forces/static/resources/secrets.yml
      Done!
    Moving secrets from subscriptions/some-subs-name/forces/dynamic/resources/plaintext.yml to subscriptions/some-subs-name/forces/dynamic/resources/secrets.yml
      Done!

Two files are created for the static and dynamic exploits:

1. plaintext.yml:

   This is a local file only, we'll write here the plain text key-value
   file

2. secrets.yml:

   This is the file we upload to the continuous repository, we'll
   generate it automatically with the fluid-cli.

At this point, the directory structure look something like this:

.. code:: bash

    kamado@fluid:/continuous$ tree subscriptions/some-subs-name/forces/

.. code:: bash

    subscriptions/some-subs-name/forces/
    ├── dynamic
    │   ├── exploits
    │   │   ├── capec-93-889225719.exp
    │   │   ├── fin-0043-601083224.exp
    │   │   ├── fin-0063-695302231.cannot.exp
    │   │   └── fin-0076-612653721.cannot.exp
    │   └── resources
    │       ├── plaintext.yml
    │       └── secrets.yml
    └── static
        ├── exploits
        │   ├── capec-0210-531993653.exp
        │   ├── fin-0006-529485525.exp
        │   ├── fin-0007-506022632.exp
        │   ├── fin-0011-522244264.exp
        │   ├── fin-0020-504994991.exp
        │   ├── fin-0037-505041691.exp
        │   ├── fin-0039-540214551.exp
        │   ├── fin-0044-506033283.exp
        │   ├── fin-0060-522308864.exp
        │   ├── fin-0061-967254060.exp
        │   └── fin-0063-528871763.exp
        └── resources
            ├── plaintext.yml
            └── secrets.yml

The original file:

.. code:: bash

    kamado@fluid:/continuous$ cat subscriptions/some-subs-name/forces/static/resources/plaintext.yml

.. code:: yaml

    secrets:
      test_user: Einstein
      test_password: E=m*C^2

The encrypted file:


.. code:: bash

    kamado@fluid:/continuous$ cat subscriptions/some-subs-name/forces/static/resources/secrets.yml

.. code:: yaml

    secrets:
      test_user: gAAAAABdp3GJPNLES8B0FkDtOyCdlWRRfvxPSn9fBZNgW6AbndwXzpgy15wDZ9aT9yNdPyNUfERcpdparN7XjsgOFDFVug3NRg==
      test_password: gAAAAABdp3GJFVUe-xkFqwVFGnVu54dmbdCCbjsuFAeGAUfxe3MHCK4npc3myoXNIjz_CM0Al6tLccMg4wuaTPwn0d526dXcpQ==

Adding secrets
--------------

We'll need to add secrets in order to use them in our exploits.

1. Add them to the corresponding **plaintext.yml** file:

   for instance:

   .. code:: yaml

       secrets:
         you_choose_a_pretty_name_1: 'highly-secret-value-123-123'
         you_choose_a_pretty_name_2: 'highly-secret-value-456-456'
         you_choose_a_pretty_name_3: 'highly-secret-value-789-789'

2. Encrypt **plaintext.yml** with the fluid-cli to generate
   **secrets.yml**:

   .. code:: bash

       kamado@fluid:/continuous$ fluid forces --encrypt-secrets <some-subs-name>

       bash Moving secrets from
       subscriptions/some-subs-name/forces/static/resources/plaintext.yml to
       subscriptions/some-subs-name/forces/static/resources/secrets.yml Done!
       Moving secrets from
       subscriptions/some-subs-name/forces/dynamic/resources/plaintext.yml to
       subscriptions/some-subs-name/forces/dynamic/resources/secrets.yml Done!

Using the secrets in the exploits
---------------------------------

See this example:

.. code:: diff

    --- a/subscriptions/some-subs-name/forces/static/exploits/fin-0020-504994991.exp
    +++ b/subscriptions/some-subs-name/forces/static/exploits/fin-0020-504994991.exp
    @@ -2,6 +2,7 @@ import utilities
     from fluidasserts.proto import git
     from fluidasserts.utils import generic

    -
    +secrets = utilities.get_secrets()

     if utilities.is_current_dir_in_repositories(
             'Some-Customer-Repository'):
    @@ -10,18 +11,18 @@ if utilities.is_current_dir_in_repositories(
         git.commit_has_secret(
             '',
             '6bddfc015080ddf04c33aeb94bbc59c3431c6550',
    -        'highly-secret-value-123-123')
    +        secrets['you_choose_a_pretty_name_1'])
         git.commit_has_secret(
             '',
             'fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27',
    -        'highly-secret-value-123-123')
    +        secrets['you_choose_a_pretty_name_1'])
         git.commit_has_secret(
             '',
             'fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27',
    -        'highly-secret-value-456-456')
    +        secrets['you_choose_a_pretty_name_2'])
         git.commit_has_secret(
             '',
             'fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27',
    -        'highly-secret-value-789-789')
    +        secrets['you_choose_a_pretty_name_3'])
     else:
         generic.add_finding('[Skipped] FIN.0020. (it does not apply to this repo)')

Running the exploit
-------------------

Remember to clone the customer repositories and then
use the fluid-cli!

.. code:: bash

    kamado@fluid:/continuous$ fluid forces --run --static all <some-subs-name>


.. code:: bash

    kamado@fluid:/continuous$ fluid forces --run --dynamic all <some-subs-name>

Now inspect the output:


.. code:: bash

    kamado@fluid:/continuous$ cat subscriptions/some-subs-name/forces/static/exploits/fin-0020-504994991.exp.out.yml

.. code:: yaml

    ---
    repository: 'Some-Customer-Repository'

    #    ________      _     __   ___                        __
    #   / ____/ /_  __(_)___/ /  /   |  _____________  _____/ /______
    #  / /_  / / / / / / __  /  / /| | / ___/ ___/ _ \/ ___/ __/ ___/
    # / __/ / / /_/ / / /_/ /  / ___ |(__  |__  )  __/ /  / /_(__  )
    #/_/   /_/\__,_/_/\__,_/  /_/  |_/____/____/\___/_/   \__/____/
    #
    # v. 19.10.22490
    #  ___
    # | >>|> fluid
    # |___|  attacks, we hack your software
    #
    # Loading attack modules ...
    #
    ---
    finding: FIN.0020. Ausencia de cifrado de información confidencial
      check: fluidasserts.proto.git -> commit_has_secret
      check: fluidasserts.proto.git -> commit_has_secret
      check: fluidasserts.proto.git -> commit_has_secret
      check: fluidasserts.proto.git -> commit_has_secret
    ---
    finding: FIN.0020. Ausencia de cifrado de información confidencial
    ---
    check: fluidasserts.proto.git -> commit_has_secret
    description: Check if commit has given secret.
    status: OPEN
    message: Secret found in commit 6bddfc015080ddf04c33aeb94bbc59c3431c6550
    vulnerabilities:
    - where: ''
      specific: Secret found in commit 6bddfc015080ddf04c33aeb94bbc59c3431c6550
    parameters:
      repo: ''
      commit_id: 6bddfc015080ddf04c33aeb94bbc59c3431c6550
      secret: 'highly-secret-value-123-123'
    vulnerable_incidences: 1
    when: 2019-10-16T15:52:19-0500
    elapsed_seconds: 0.0
    test_kind: SAST
    risk: low
    ---
    check: fluidasserts.proto.git -> commit_has_secret
    description: Check if commit has given secret.
    status: OPEN
    message: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    vulnerabilities:
    - where: ''
      specific: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    parameters:
      repo: ''
      commit_id: fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
      secret: 'highly-secret-value-123-123'
    vulnerable_incidences: 1
    when: 2019-10-16T15:52:19-0500
    elapsed_seconds: 0.0
    test_kind: SAST
    risk: low
    ---
    check: fluidasserts.proto.git -> commit_has_secret
    description: Check if commit has given secret.
    status: OPEN
    message: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    vulnerabilities:
    - where: ''
      specific: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    parameters:
      repo: ''
      commit_id: fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
      secret: highly-secret-value-456-456
    vulnerable_incidences: 1
    when: 2019-10-16T15:52:19-0500
    elapsed_seconds: 0.0
    test_kind: SAST
    risk: low
    ---
    check: fluidasserts.proto.git -> commit_has_secret
    description: Check if commit has given secret.
    status: OPEN
    message: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    vulnerabilities:
    - where: ''
      specific: Secret found in commit fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
    parameters:
      repo: ''
      commit_id: fb2fb6d96ea205f03a8f9aa32ffb4a90c0027f27
      secret: highly-secret-value-789-789
    vulnerable_incidences: 1
    when: 2019-10-16T15:52:19-0500
    elapsed_seconds: 0.0
    test_kind: SAST
    risk: low
    ---
    method level stats:
      FIN.0020. Ausencia de cifrado de información confidencial:
        fluidasserts.proto.git -> commit_has_secret: 4 open, 0 closed, 0 unknown
    ---
    summary:
      test time: 0.1614 seconds
      checks:
        total: 4 (100%)
        errors: 0 (0.00%)
        unknown: 0 (0.00%)
        closed: 0 (0.00%)
        opened: 4 (100.00%)
      risk:
        high: 0 (0.00%)
        medium: 0 (0.00%)
        low: 4 (100.00%)
    # elapsed: 0.3631293773651123
