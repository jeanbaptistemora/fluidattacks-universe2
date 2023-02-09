# Task inventory

## Schedulers
1. [clone_groups_roots](../back/src/schedulers/clone_groups_roots.py):
   lists all the roots of all the groups, for each git root
   makes a request to the git server to check if we have the latest version
   of the repository in S3. If the version we have in S3 is different from
   the version on the git server, a clone is queued for that root. Jobs for
   root cloning are grouped by each group. The cloning is the main job,
   it queues the other necessary jobs so that all the elements
   of the chain are synchronized. The order of execution of the jobs is
   the following: `clone_roots` -> `refresh_toe_lines` -> `rebase`. These jobs
   are queued as batch jobs dependent on each other,
   which makes the job execution chain brittle and leaves unexecuted jobs.
   Machine does not appear in the execution chain because it is critical jobs,
   machine is queued as a separate job after completion of `clone_roots`
   execution, with this we make sure that if there is a new version of a
   repository, machine will always be run on it.
2. [clone_groups_roots_vpn](../back/src/schedulers/clone_groups_roots_vpn.py):
   Queues the cloning of all the roots that require
   the aws VPN to be cloned. A separate schedule is used because
   `clone_groups_roots` cannot check if there is a new version of the
   repository. A clone is queued regardless of whether there is a new
   version of the repository.
3. [machine_queue_all](back/src/schedulers/machine_queue_all.py): Queue an
   execution of machine for all git roots of all groups that have machine.
4. [machine_queue_re_attacks](back/src/schedulers/machine_queue_re_attacks.py):
   Finds all vulnerabilities that have been reattacked and queues a grouped
   machine execution all roots with reattacks requested from each group
5. [refresh_toe_lines](../back/src/schedulers/refresh_toe_lines.py): Queues a
   cascade execution of the following jobs for each root of all active groups `refresh_toe_lines` -> `rebase`

## batch_dispatch

1. [clone_roots](../back/src/batch_dispatch/clone_roots.py):
   Clone the specified git roots of a group. To queue a job of this
   type it is necessary to call a function called `queue_sync_git_roots`,
   this function is referenced from:
   - [add_git_root](../back/src/api/mutations/add_git_root.py) mutation
   - [sync_git_root](../back/src/api/mutations/sync_git_root.py) mutation
   - [update_git_root](../back/src/api/mutations/update_git_root.py) mutation
   - [queue_job_new](../back/src/machine/jobs.py) function, this function is
     called to do a clone before the execution of a machine job
   - [clone_groups_roots](../back/src/schedulers/clone_groups_roots.py) scheduler
2. [move_roots](../back/src/batch_dispatch/remove_roots.py)
3. [rebase](../back/src/batch_dispatch/rebase.py): To enqueue this job,
   a batch action is called directly, there is no centralized function to
   enqueue the job. As it is not centralized, different calls can be made,
   which means that the jobs are not always the same. This job is queued from:
   - [queue_sync_git_roots](../back/src/roots/domain.py), this call is part of
     a chain of dependent jobs that could fail
     [refresh_toe_lines](../back/src/schedulers/refresh_toe_lines.py): the
     rebase is a dependent job of refresh toe lines
4. [refresh_toe_inputs](../back/src/batch_dispatch/refresh_toe_inputs.py)
5. [refresh_toe_lines](../back/src/batch_dispatch/refresh_toe_lines.py)
   - [activate_root](../back/src/api/mutations/activate_root.py) mutation
   - [add_git_root](../back/src/api/mutations/add_git_root.py) mutation
   - [deactivate_root](../back/src/api/mutations/deactivate_root.py) mutation:
   this mutation first removes all root-related resources and then makes
   the job remove all lines.
   - [move_root](../back/src/api/mutations/move_root.py) mutation
   - [refresh_toe_lines](../back/src/api/mutations/refresh_toe_lines.py) mutation
   - [move_root](../back/src/batch_dispatch/move_root.py) function
   - [queue_sync_git_roots](../back/src/roots/domain.py) function
   - [refresh_toe_lines](../back/src/schedulers/refresh_toe_lines.py) scheduler
