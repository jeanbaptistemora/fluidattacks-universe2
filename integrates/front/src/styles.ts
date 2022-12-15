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

  .g-btn {
    color: #333;
    border: 1px solid transparent;
    border-color: #ccc;
  }

  .g-a,
  .g-a:hover,
  .g-a:focus,
  .g-a:visited {
    color: #333;
    text-decoration: none;
  }

  .questionBtn {
    border: 0 !important;
    color: #ff3435;
  }

  .questionBtn:hover {
    background-color: unset !important;
    color: #272727 !important;
  }

  .panel-cb {
    border-color: #ddd;
  }

  .panel-ch {
    color: #333;
    background-color: #f5f5f5;
    border-color: #ddd;
  }

  .g1 {
    border: 1px solid transparent;
    border-color: #ddd;
    height: 402px;
  }

  .g2 {
    border: 1px solid transparent;
    border-color: #ddd;
    height: 242px;
  }

  .g3 {
    border: 1px solid transparent;
    border-color: #ddd;
    height: 162px;
  }

  .upload-file {
    margin-right: 40px;
    margin-left: 40px;
  }

  @media (max-width: 479px) {
    .upload-file {
      margin-top: 20px;
    }
  }
`;

export { GlobalStyle };
