import styled from "styled-components";

const BreadcrumbContainer = styled.div.attrs({
  className: "breadcrumb list",
})``;

const NavSplitButtonContainer = styled.div.attrs({
  className: "split-button",
})`
  padding-right: 24px;
`;

const SplitItems = styled.div.attrs({
  className: "splitItems mr3 flex-wrap fixed",
})`
  background-color: #fff;
  border: solid 1px;
  border-color: #ddd;
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
  color: #333;
  display: none;
  margin-top: 5px;
  max-width: 1172px;
  max-height: 827px;
  overflow: auto;
  writing-mode: vertical-lr;
  z-index: 1;

  @media (max-width: 1254px) {
    max-width: 1055px;
  }

  @media (max-width: 1137px) {
    max-width: 938px;
  }

  @media (max-width: 1020px) {
    max-width: 821px;
  }

  @media (max-width: 903px) {
    max-width: 704px;
  }

  @media (max-width: 786px) {
    max-width: 587px;
  }

  @media (max-width: 669px) {
    max-width: 470px;
  }

  @media (max-width: 552px) {
    max-width: 353px;
  }

  @media (max-width: 435px) {
    max-width: 236px;
  }

  @media (max-width: 318px) {
    max-width: 119px;
  }
`;

export { BreadcrumbContainer, NavSplitButtonContainer, SplitItems };
