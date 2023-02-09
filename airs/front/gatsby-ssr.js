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
      httpEquiv={"Pragma"}
      content={"no-cache"}
      key={1}
    />,
    <metadata
      httpEquiv={"cache-control"}
      content={"no-cache, no-store, must-revalidate"}
      key={2}
    />,
    <script
      id={"Cookiebot"}
      src={"https://consent.cookiebot.com/uc.js"}
      data-cbid={"9c4480b4-b8ae-44d8-9c6f-6300b86e9094"}
      data-blockingmode={"auto"}
      type={"text/javascript"}
      key={3}
    />,
    // Highlight.js syntax highlighter
    <link
      rel={"stylesheet"}
      href={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/styles/foundation.min.css"}
      key={4}
    />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/highlight.min.js"} key={5} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/x86asm.min.js"} key={6} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/gherkin.min.js"} key={7} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/powershell.min.js"} key={8} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/xml.min.js"} key={9} />,
    <script src={"https://cdnjs.cloudflare.com/ajax/libs/highlight.js/10.1.1/languages/shell.min.js"} key={10} />,
    <script src={"/highlightjs.js" } crossOrigin="anonymous" key={11}/>,
    // End Highlight.js
  ]);
  setHtmlAttributes(HtmlAttributes);
  setPostBodyComponents([
    // Zoho CRM Live Chat
    <script
      id={"zsiqchat"}
      src={"/zohoLiveChat.js"}
      type={"text/javascript"}
      crossOrigin="anonymous"
      key={12}
    />,
  ]);
};
