==========
Developing
==========

A new support module must be placed
in the appropriate package:

* :doc:`lang<fluidasserts.lang>` for code checks,
  v.g. in :doc:`Java<fluidasserts.lang.java>`
* :doc:`proto<fluidasserts.proto>` for protocols
  such as :doc:`LDAP<fluidasserts.proto.ldap>`
* :doc:`format<fluidasserts.format>` for formats
  such as :doc:`Cookies<fluidasserts.format.cookie>`
* :doc:`syst<fluidasserts.syst>` for global OS checks
  v.g. in :doc:`Linux<fluidasserts.syst.linux>`

New functions must be predicates i.e.
they must return
true if the vulnerability is open
or false if it is closed,
and show the appropriate message
from the main package:

.. code-block:: python

   from fluidasserts import show_close, show_open

   def has_insecure_deserialization(java_dest: str) -> bool:
       if ...:
           show_open('Code uses insecure deserialization', details=...)
           return True
       else:
           show_close('Code uses secure deserialization', details=...)
           return False

This will sometimes lead to
apparently awkward function names,
like ``is_not_https_required``
but it makes sense considering
we are not testing
if ``https`` is _required_, but rather
whether the `vulnerability` "not requiring ``https``" `is open`.

Function names must be written in english
and conform to :pep:`8`
(in particular they must be written in ``snake_case``)
so that they can be used like this
from a project exploit:

.. code-block:: python

   from fluidasserts.lang import javascript
   javascript.uses_eval('my-script.js')

Other good function name ideas:

.. code-block:: python

   is_code_not_obfuscated
   is_disk_not_encrypted
   is_linter_bypassed
   has_blind_xee
   contains_commented_code

Notice that if the answer to any of these questions is true,
then we have an open vulnerability.

Bad function names:

.. code-block:: python

   is_secure         # Too general
   has_antimalware   # Logic inverted
   ssh_version       # Not a verb

Comments, variables, parameter names, etc
should also be written in English
and conform to :pep:`8` conventions.

All modules are checked with the linters
`Pylint <https://www.pylint.org/>`_, \
`Pyflakes <https://www.pylint.org/>`_, \
`Flake8 <http://flake8.pycqa.org/en/latest/>`_, \
`Pycodestyle <https://pypi.org/project/pycodestyle/>`_, \
and the tools \
`dodgy <https://github.com/landscapeio/dodgy>`_, \
`mccabe <https://pypi.org/project/mccabe/>`_, and \
`pep8 <https://pypi.org/project/pep8/>`_ (via \
`Prospector <https://pypi.org/project/prospector/>`_, \
in highest strictness).
It is recommended to install and
use `overcommit <https://github.com/sds/overcommit>`_
locally before committing.

--------------
Required tools
--------------

Besides the runtime dependencies
(see ...),
you will need some dependencies
which you can install with this command
on a ``Debian``-based OS: ::

   $ sudo apt install python3-dev python3-pip python3.6-venv git cloc scons rubygems

And then some python packages via ``pip``: ::

   $ pip3 install invoke configobj tox sphinx mypy

Finally install the pre-commit hooks ::

  $ gem install overcommit
  $ overcommit --sign pre-commit

This last step should be done after cloning the repository
since it needs the ``overcommit.yml`` configuration file in it.

You also need to install ``Docker-CE``.
Follow the steps in `this guide <https://docs.docker.com/install/linux/docker-ce/debian/>`_.

------------------------
Version control workflow
------------------------

After receiving developer access and cloning the repository,
setup your credentials if you haven't done so already.
In GitLab (from the website) and
your local git installation (with ``git config``),
your username must be ``loginatfluid`` v.g. ``dknuthatfluid``
and your email must be your corporate email, v.g. ``dknuth@fluidattacks.com``.
The name should be your real name, v.g. ``Donald Knuth``.

The branching workflow is with
``topic branches``
but with one caveat:
the name of the branch you work on
must be your ``login``.
Following the example above,
Don should name his branch ``dknuth``.

The merge strategy is by
fast-forwards only.
When ready to make a merge request,
ensure that your branch is ahead of master.
This means that
you must integrate the latest changes
in the ``master`` branch before your own commits, i.e.
you should `rebase` the ``master`` branch onto your own branch.
Don can keep up to date easily using these commands
after finishing his commits
without ever leaving his branch: ::

   $ git fetch
   $ git rebase origin/master

If Don followed these steps,
checking their effect with ``git log``,
he would see this:

.. code-block:: console

   [dknuth@tex asserts]$ git commit -m "My last commit"
   [dknuth bc53277] My last commit
   1 file changed, 44 insertions(+)
   [dknuth@tex asserts]$ git log --pretty=oneline --abbrev-commit
   a201834 (HEAD -> dknuth) My last commit
   f3dec2a (origin/master) Feature: Add cool new feature
   ...
   [dknuth@tex asserts]$ git fetch
   remote: Counting objects: 4, done.
   remote: Compressing objects: 100% (4/4), done.
   remote: Total 4 (delta 0), reused 0 (delta 0)
   Unpacking objects: 100% (4/4), done.
   From gitlab.com:fluidsignal/asserts
   20b4133..347d774  master     -> origin/master
   + f56e548...e11188e ltorvalds    -> origin/ltorvalds  (forced update)
   + f56e548...347d774 rstallman    -> origin/rstallman  (forced update)
   [dknuth@tex asserts]$ git rebase origin/master
   First, rewinding head to replay your work on top of it...
   Applying: My last commit
   [dknuth@tex asserts]$ git log --pretty=oneline --abbrev-commit
   a201834 (HEAD -> dknuth) My last commit
   347d774 (origin/rstallman, origin/master, origin/HEAD) Add emacs support
   e11188e (origin/ltorvalds) Update to kernel 4.14
   f3dec2a Add cool new feature
   ...
   [dknuth@tex asserts]

Now Don is ready to make his merge request,
that is, if his pipeline passes...

----------------------
Continuous Integration
----------------------

``Asserts`` uses GitLab CI to
make sure that a change in a commit
does not break anything in the master branch.
Among other things, the CI pipeline:

#. Builds environments for development and runtime
#. Lints the entire codebase
#. Runs the whole test suite
#. Deploys the project for release
#. Updates this documentation site

You can run this pipeline locally before pushing using the
`Nix <https://nixos.wiki/wiki/Nix_Installation_Guide>`_ shell
and the
`local-integration.nix <https://gitlab.com/fluidattacks/asserts/blob/master/local-integration.nix>`_
script in the repo.

As a developer,
you should be specially concerned about:

* Not pushing simple mistakes like trailing
  whitespace or typos. ::

     $ overcommit --run

  Can help avoid these.

* Not pushing functional but ugly code
  by linter standards. Run ::

     $ scons lint

  You can use each linter individually as well.

* Your code passing every test. Run ::

     $ scons test

Finally, keep your commits small and
logically atomic, that is, there should
be a one-to-one mapping between
functional changes to the codebase and commits.
If you're adding a function in the HTTP module,
don't commit every line you add independently,
but also don't include your changes to another module
in that same commit.

-------------
Documentation
-------------

Docstrings should conform to :pep:`257`
and will be checked by ``pydocstyle`` in CI time.
Parameters and return specifications should be written in
plain `Sphinx <http://www.sphinx-doc.org/en/master/>`_
`ReStructured Text
<https://pythonhosted.org/an_example_pypi_project/sphinx.html#function-definitions>`_ style, while
parameter and return types must be specified using
Type Hints according to :pep:`484`:

.. code-block:: python

   def is_long_line(line: str) -> bool
       """
       Determine if a ``line`` is *too* long.

       :param line: A line of code to test.
       :return: ``True`` if too long, ``False`` if **OK**.
       """

This is further enhanced by `MyPy <http://mypy-lang.org/>`_
and the :mod:`typing` module
which provides means to specify, in particular,
optional and multiple return types.
Type consistency will be checked by MyPy in CI time,
but not strictly.

Whenever possible,
docstrings should link to the appropriate entry
in FLUIDRules and FLUIDDefends.

----------
References
----------

The following pages contain some ideas
to keep in mind when developing ``Fluid Asserts``:

* https://haacked.com/archive/2007/09/21/unit-testing-security-example.aspx/
* https://wiki.owasp.org/index.php/OWASP_Secure_TDD_Project
* https://dadario.com.br/security-unit-tests-are-important/
* https://owasp.blogspot.com/2012/08/owasp-xelenium-security-unit-tests.html
* https://www.owasp.org/images/9/99/AutomatedSecurityTestingofWebApplications-StephendeVries.pdf
* https://www.owasp.org/images/6/62/OWASPAppSecEU2006_SecurityTestingthruAutomatedSWTests.ppt
* https://spring.io/blog/2014/05/07/preview-spring-security-test-method-security
* https://www.adapttransformation.com/devops-toolchain/test/testing/security-testing/
* https://blogs.adobe.com/security/2014/07/overview-of-behavior-driven-development.html
* https://www.hugeinc.com/work
* https://wiki.mozilla.org/Security/Projects/Minion
* https://devops.com/automated-security-testing-continuous-delivery-pipeline/
* https://iriusrisk.com/open-source/
* https://blog.joda.org/2004/11/testing-security-permission_5894.html
* https://www.ibm.com/developerworks/java/library/j-fuzztest/index.html
* https://howtodoinjava.com/junit/how-to-unit-test-spring-security-authentication-with-junit/
* https://blog.box.com/a-baseline-approach-to-security-testing
* https://morelia.readthedocs.io/en/latest/gherkin.html#gherkin
* https://dzone.com/articles/making-web-secure-one-unit
* https://www.linkedin.com/in/stephen-de-vries-4185a8
* https://www.slideshare.net/StephendeVries2/automating-security-tests-for-continuous-integration
* https://www.slideshare.net/StephendeVries2/continuous-security-testing-with-devops
* http://lettuce.it/tutorial/simple.html
* https://aws.amazon.com/blogs/developer/devops-meets-security-security-testing-your-aws-application-part-i-unit-testing/
* https://github.com/OWASP/OWASP-Testing-Guide/blob/master/2-Introduction/2.5%20Security%20Tests%20Integrated%20in%20Development%20and%20Testing%20Workflows.md
* https://support.smartbear.com/cucumberstudio/docs/bdd/write-gherkin-scenarios.html
* https://www.arachni-scanner.com/screenshots/web-user-interface/
