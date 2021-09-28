import React from "react";

const HtmlAttributes = {
  translate: "no"
}

export const onRenderBody = (
  { setHeadComponents, setHtmlAttributes, setPostBodyComponents },
  pluginOptions
) => {
  setHeadComponents([
    // Disabling cache
    <metadata
      http-equiv={"Pragma"}
      content={"no-cache"}
    />,
    <metadata
      http-equiv={"cache-control"}
      content={"no-cache, no-store, must-revalidate"}
    />,
    <script
      id={"Cookiebot"}
      src={"https://consent.cookiebot.com/uc.js"}
      data-cbid={"9c4480b4-b8ae-44d8-9c6f-6300b86e9094"}
      data-blockingmode={"auto"}
      type={"text/javascript"}
    />,
    <metadata 
      name="facebook-domain-verification" 
      content="8hgdyewoknahd41nv3q5miuxx6sazj" 
    />,
    // Cloudflare Web Analytics
    <script
      defer
      src={"https://static.cloudflareinsights.com/beacon.min.js"}
      integrity={"sha384-GJ9nByhjxyQW/UQqhRHgMYt1FWJvn89k/MDc4o3LwMCHwhhWrxAdIvoyuSqjfoIa"}
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
    <script src={"/highlightjs.js"}/>,
    // End Highlight.js
  ]);
  setHtmlAttributes(HtmlAttributes);
  setPostBodyComponents([
    // Zoho CRM Live Chat
    <script
      id={"zsiqchat"}
      src={"/zohoLiveChat.js"}
      type={"text/javascript"}
    />,
  ]);
};
