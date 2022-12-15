import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
  html,
  body,
  #root {
    height: 100%;
  }

  ::selection {
    color: #fff;
    background: #2e2e38;
  }

  hr {
    border: 0;
    border-top: 1px solid #eee;
  }

  a {
    color: #bf0b1a;
    text-decoration: none;
  }

  a:hover,
  a:focus {
    text-decoration: none;
    outline: none;
  }

  .breadcrumb > li + li > a:active,
  .breadcrumb > li + li > a:focus,
  .breadcrumb > li + li > a:hover {
    color: #272727 !important;
  }

  .breadcrumb {
    background-color: transparent;
    margin-bottom: 0;
    display: flex;
    align-items: flex-end;
    flex-wrap: wrap;
  }

  .breadcrumb > li:not(:last-child)::after {
    content: "/";
    padding: 0 4px;
  }
`;

export { GlobalStyle };
