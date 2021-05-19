import styled from "styled-components";

const NavbarContainer = styled.nav.attrs({
  className: "flex flex-wrap ph3",
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
  className: "f4 flex items-center list mb0 ph0",
})`
  li {
    color: #777;
    cursor: pointer;
    padding: 0 12px;
  }
`;

const MenuButton = styled.button.attrs({
  className: "bn flex gray outline-0 pointer",
})`
  background: none;
`;

const DropdownMenu = styled.ul.attrs({
  className: "absolute bg-white f5 list mt3 mr3 ph2 pv2 shadow-3",
})`
  min-width: 240px;
  right: 0;
  li {
    color: black;
  }
`;

export { DropdownMenu, MenuButton, NavbarContainer, NavbarHeader, NavbarMenu };
