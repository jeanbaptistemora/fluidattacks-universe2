import styled from "styled-components";

const NavbarContainer = styled.nav.attrs({
  className: "flex flex-wrap",
})`
  background-color: #f4f4f6;
  border-bottom: 1px solid #bfbfb0;
  padding: 12px 24px;
`;

const NavbarHeader = styled.div.attrs({
  className: "flex flex-auto items-center",
})``;

const NavbarMenu = styled.ul.attrs({
  className: "f4 flex items-center list ma0 ph0",
})`
  & li {
    position: relative;
  }
`;

export { NavbarContainer, NavbarHeader, NavbarMenu };
