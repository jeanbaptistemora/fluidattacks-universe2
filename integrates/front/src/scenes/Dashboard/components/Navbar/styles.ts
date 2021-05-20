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
  & li {
    position: relative;
  }
`;

const NavbarButton = styled.button.attrs({
  className: "bn flex gray outline-0 ph3 pv2 pointer",
})`
  background: none;
`;

const DropdownMenu = styled.ul.attrs({
  className: "absolute bg-white f5 list mt3 ph0 pv2 shadow-1",
})`
  min-width: 240px;
  right: 0;
  & li {
    padding: 0;
  }
`;

const DropdownButton = styled.button.attrs({
  className: "bn gray hover-bg-light-gray outline-0 ph3 pv2 pointer tl w-100",
})`
  background: none;
  & svg {
    margin-right: 5px;
  }
`;

const DropdownDivider = styled.hr.attrs({
  className: "mv2",
})``;

export {
  DropdownButton,
  DropdownDivider,
  DropdownMenu,
  NavbarButton,
  NavbarContainer,
  NavbarHeader,
  NavbarMenu,
};
