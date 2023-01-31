import { createGlobalStyle } from "styled-components";

const GlobalStyle = createGlobalStyle`
  html,
  body,
  #root {
    height: 100%;
    overflow: hidden;
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

  .no-data {
    color: lightgray;
    font-size: 40px;
    text-align: center;
  }

  .b-sb,
  .b-sb:active,
  .b-sb:focus,
  .b-sb:hover {
    border: none !important;
  }

  .b-switch {
    border-color: #d9534f;
  }

  .b-switch:hover {
    border-color: #ac2925;
  }

  .bg-lbl-green {
    background-color: #c2ffd4;
    color: #009245;
  }

  .bg-lbl-yellow {
    background-color: #ffbf00;
  }

  .bg-sb,
  .bg-sb:active,
  .bg-sb:focus,
  .bg-sb:hover {
    background: transparent !important;
  }

  .bg-switch {
    background-color: #d9534f;
  }

  .bg-switch:hover {
    background-color: #c9302c;
  }

  .checkbox-mh {
    min-height: calc(1.5em + 0.75rem + 2px);
  }

  .fs-checkbox {
    font-size: 12px;
  }

  .green-checkbox {
    background-color: #5cb85c;
    border-color: #5cb85c;
  }

  .green-checkbox:hover {
    background-color: #3faf3f;
    border-color: #3faf3f;
  }

  .red-checkbox {
    background-color: #d9534f;
    border-color: #d9534f;
  }

  .red-checkbox:hover {
    background-color: #c9302c;
    border-color: #c9302c;
  }

  .grid {
    display: grid;
  }

  .menu-grid {
    grid-template-columns: repeat(auto-fit, minmax(7rem, 1fr));
  }

  .orgred {
    color: #ff3435;
  }

  .ph1-5 {
    padding-left: 1.5rem;
    padding-right: 1.5rem;
  }

  .svg-box20 svg {
    width: 20px !important;
    height: 20px !important;
  }

  .switch-mh {
    min-height: calc(1.5em + 0.75rem + 2px);
  }

  .w-fit-content {
    width: fit-content;
  }

  .ws-pre-wrap {
    white-space: pre-wrap;
  }
`;

export { GlobalStyle };
