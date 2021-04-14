---
id: deleting-vulns
title: Deleting vulnerabilities
sidebar_label: Deleting vulnerabilities
slug: /machine/web/vulnerabilities/deleting-vulns
---

Sometimes, it is necessary that a vulnerability be removed from the ASM
for different reasons. Nevertheless, deleting the information is not a good idea in
the security world, and it is always important to keep track of these events.
This is why in Fluid Attacks we don’t delete the vulnerabilities.
Instead, analysts can set any of them to a “Deleted” state.

### Deleting specific vulnerabilities

When you want to delete just one or several specific vulnerabilities inside a certain
type of vulnerability, you need to enter the vulnerability and click on the
button **Bulk edit** to enable de edition of vulnerabilities.

![Vulnerabilities Deletion Enabled](/img/web/vulnerabilities/deleting-vulns/vulns_delete_enabled.png)

After this you need to locate the vulnerabilities that you want to delete
and then click on the trash icon to the right of the window for a pop-up to show up.

![Delete Vulnerabilities Modal](/img/web/vulnerabilities/deleting-vulns/delete_vuln_modal.png)

Here you can select between three options to assign as a justification which can be one
of the following:

- **It is a duplicate:** The finding or vulnerability had been reported previously.
- **It is a false positive:** After a review process, it was determined that the finding
or vulnerability was not.
- **Error when reporting:** Given that a vulnerability cannot be edited, this option must
be selected if you are going to report another vulnerability that corrects it.

After this you may click on the **Proceed** button to complete the deletion process or
you can click on the **Cancel** button to dismiss it.

### Deleting a type of vulnerability

Sometimes it is also necessary to delete a type of vulnerability and all the individual
vulnerabilities that it contains, in this case you can click on the **Delete** button that
is located in the upper-right corner of your window.

![Delete Finding Button](/img/web/vulnerabilities/deleting-vulns/delete_finding_button.png)

When you click on it, the same pop-up for the deletion of individual vulnerabilities will
appear, however this one will have one different option to select as a justification, the
ones that appear are the following:

- **It is a duplicate**
- **It is a false positive**
- **Finding not required:** The report was made for a system that no longer exists or
for a finished project.

After choosing the justification, once again, you may click on the **Proceed** button to
complete the deletion process or you can click on the **Cancel** button to dismiss it.
