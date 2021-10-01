import React from "react";

export const onRenderBody = (
  { setHeadComponents, setPostBodyComponents },
  pluginOptions
) => {
  setHeadComponents([
    <script
      id={"Cookiebot"}
      src={"https://consent.cookiebot.com/uc.js"}
      data-cbid={"9c4480b4-b8ae-44d8-9c6f-6300b86e9094"}
      data-blockingmode={"auto"}
      type={"text/javascript"}
    />,
    // Cloudflare Web Analytics
    <script
      defer
      src={"https://static.cloudflareinsights.com/beacon.min.js"}
      integrity={
        "sha384-OkvTy+NUkZMJbbmFEAPbDMq3Q9yJVfdMxHLBqwXd7W5c256/DtRrbfLEg5NgPlD+"
      }
      crossOrigin={"anonymous"}
      data-cf-beacon={'{"token": "f4f99c985c414a5591e8077bf301b39b"}'}
    />,
    // Highlight.js syntax highlighter
    <link
      rel={"stylesheet"}
      href={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/foundation.min.css"}
    />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js"} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/x86asm.min.js"} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/gherkin.min.js"} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/powershell.min.js"} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/xml.min.js"} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/shell.min.js"} />,
    <script src={"highlightjs.js"}/>,
    // End Highlight.js
  ]);
  setPostBodyComponents([
    // Zoho CRM Live Chat
    <script
      id={"zsiqchat"}
      src={"zohoLiveChat.js"}
      type={"text/javascript"}
    />,
  ]);
};
