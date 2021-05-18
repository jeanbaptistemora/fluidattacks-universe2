import styled from "styled-components";

const NavbarContainer = styled.nav.attrs({
  className: "flex flex-wrap ph4",
})`
  background-color: #f5f5f5;
  border-bottom: 2px #e4e4e4 solid;
  font-size: 18px;
  height 100%;
  min-height: 50px;
`;

const NavbarHeader = styled.div.attrs({
  className: "flex flex-auto items-center",
})``;

const NavbarMenu = styled.ul.attrs({
  className: "flex items-center list mb0 ph0",
})`
  li {
    color: #777;
    padding: 2px 12px;
  }
`;

export { NavbarContainer, NavbarHeader, NavbarMenu };
