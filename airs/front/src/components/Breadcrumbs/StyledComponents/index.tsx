import { Link } from "gatsby";
import styled from "styled-components";

const Breadcrumb = styled.nav`
  background-color: #40404f;
  font-family: "Poppins", sans-serif;
  padding-bottom: 0;
  padding-top: 0;
`;

const BreadcrumbList = styled.ol.attrs({
  className: `
    flex
    flex-wrap
    list
    f6
    mv0
    mr-auto
    ml-auto
  `,
})`
  max-width: 1570px;
  padding: 15px 1.75rem !important;
  text-align: left;

  @media screen and (min-width: 60em) {
    font-size: 0.875rem;
    padding: 15px 1.75rem !important;
  }
`;

const BreadcrumbListItem = styled.li.attrs({
  className: `ma0`,
})``;

const BreadcrumbLink = styled(Link).attrs({
  className: `
    c-fluid-gray
    hv-white-244
  `,
})`
  text-decoration: none;
`;

const BreadcrumbSeparator = styled.span.attrs({
  className: `
    c-fluid-gray
    mh1
  `,
})``;

export {
  Breadcrumb,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbListItem,
  BreadcrumbSeparator,
};
