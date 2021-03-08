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
      data-cf-beacon={'{"token": "f4f99c985c414a5591e8077bf301b39b"}'}
    />,
    // Tachyons stylesheet, this preload is necessary
    <link
      rel="preload"
      as="style"
      onload="this.rel = 'stylesheet'"
      href="https://unpkg.com/tachyons@4.10.0/css/tachyons.min.css"
    />,
    // this is an alternative to old browsers
    <link
      rel="stylesheet"
      href="https://unpkg.com/tachyons@4.10.0/css/tachyons.min.css"
    />,
  ]);
  setPostBodyComponents([
    // Zoho CRM Live Chat
    <script
      type="text/javascript"
      dangerouslySetInnerHTML={{
        __html: `
        var $zoho=$zoho || {};$zoho.salesiq = $zoho.salesiq ||
        {widgetcode:"50094df2b302da078befa3cee2e8de00943ab0089a71d1aa34f6df9b6cb54ae5feb79731b60e202192c2895c9acefb61", values:{},ready:function(){}};
        var d=document;s=d.createElement("script");s.type="text/javascript";s.id="zsiqscript";s.defer=true;
        s.src="https://salesiq.zoho.com/widget";t=d.getElementsByTagName("script")[0];t.parentNode.insertBefore(s,t);d.write("<div id='zsiqwidget'></div>");
      `,
      }}
    />,
  ]);
};
