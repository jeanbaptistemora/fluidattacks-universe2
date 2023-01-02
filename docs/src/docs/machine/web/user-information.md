---
id: user
title: User
sidebar_label: User
slug: /machine/web/user
---

On the ARM, it is quite easy to
find the options to enable early
access to changes to the platform,
register your mobile phone number,
access the platform’s API,
configure what notifications you
want to receive in your email,
configure from which CVSS score
you want to receive email,
delete your account,
and log out.
These are shown on a drop-down
menu that appears when you click
the user icon on the upper-right
part of your screen.
Your username,
email address and role
are shown as well.

![User Drop Down Menu](https://res.cloudinary.com/fluid-attacks/image/upload/v1665497903/docs/web/drop_menu.png)

The first information on
this menu is your username,
followed by the email address
with which you signed in and
your mobile phone number which
one you subscribe to the ARM.
Remember your privileges are
attached to this email address.

Differences in access
privileges are managed depending
on your role on the ARM,
which is also shown on this menu.
You can find out
more about roles
[here](/machine/web/groups/roles)
(be sure to check out the
[role table](/machine/web/groups/roles/#roles-table)).
Below the user role information is
the **Feature preview** option,
which you can toggle on to enable
early access to changes to the
platform features,
i.e.,
before they are officially released.

Further down,
there’s an option that says **API token**.
Clicking on it will allow you to
generate an access token to
consume the ARM’s API.
You will be asked to set its
expiration date before generating it.
You can find out more about
this under
[this link](/machine/api/#using-the-asm-api-token).

Next is the
**Notifications** option,
which allows you to select
which notifications you
want to receive.
When you click on it,
you will see the
**Notifications matrix**
that shows you all the
reports and alerts that
our ARM generates.
Learn more about how you
can manage notifications
[here](/machine/web/notifications).

![Notification Matrix](https://res.cloudinary.com/fluid-attacks/image/upload/v1665497944/docs/web/matrix_notification.png)

You also find in this same view
**Minimum Severity**,
which helps you to configure the
CVSS (Common Vulnerability Scoring System)
severity range that you want to
receive in the
[Vulnerability Alert notification](/machine/web/notifications#vulnerability-alert).
According to the number you leave
in this section,
vulnerabilities with a severity higher
than the limit you set will be reported.

![Minimum Severity](https://res.cloudinary.com/fluid-attacks/image/upload/v1665777823/docs/web/minimum_severity.png)

Next is **Mobile**,
which allows you to
register your mobile
phone number to the ARM.
This registration is
required to access
the ARM reports.

![Mobile Option](https://res.cloudinary.com/fluid-attacks/image/upload/v1665497976/docs/web/mobile.png)

When you click on
the Mobile option,
a pop-up window will appear.
If you had not registered
your mobile phone before,
you will be asked to
add your number and then
enter the verification code
sent to you via SMS to
complete the registration.
However,
if you had already registered it,
you will be presented with
the option to change it.
To do this,
you will need to click on
Edit and follow a verification
procedure.

![Enter Mobile](https://res.cloudinary.com/fluid-attacks/image/upload/v1665498003/docs/web/edit_mobile.png)

Next on the menu is the
**Delete account** option.
This will allow you to delete
your account if you are no
longer using the ARM.
Your access privileges will
be deleted along with the account.
Before proceeding, a warning
message will appear, reminding
you that you will not be able
to restore your account afterward.

![Delete Account](https://res.cloudinary.com/fluid-attacks/image/upload/v1665498032/docs/web/delete_account.png)

> **Note:** Regardless of their role,
> all stakeholders are automatically
> removed after 90 days of inactivity.

Lastly, the **Log out**
option will allow you to end
your session on the ARM.
