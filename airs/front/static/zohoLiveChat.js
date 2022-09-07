// SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
//
// SPDX-License-Identifier: MPL-2.0

let $zoho = $zoho || {};
$zoho.salesiq = $zoho.salesiq || {
  widgetcode:
    "50094df2b302da078befa3cee2e8de00943ab0089a71d1aa34f6df9b6cb54ae5feb79731b60e202192c2895c9acefb61",
  values: {},
  ready: function () {
    // Intentionally left blank
  },
};
let d = document;
let s = d.createElement("script");
s.type = "text/javascript";
s.id = "zsiqscript";
s.defer = true;
s.src = "https://salesiq.zoho.com/widget";
let t = d.getElementsByTagName("script")[0];
t.parentNode.insertBefore(s, t);
