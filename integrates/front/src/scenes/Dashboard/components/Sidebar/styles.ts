import styled from "styled-components";

const SidebarContainer = styled.aside.attrs({
  className: "flex flex-column justify-between",
})`
  background-color: #272727;
  transition: width 0.3s, left 0.3s;
  width: 210px;
`;

const SidebarMenu = styled.ul.attrs({
  className: "pl0 list",
})``;

const MenuButton = styled.button.attrs({
  className: "white ph3 pv2 w-100 bn pointer outline-0 tl nowrap",
})`
  background: none;
  & svg {
    margin-right: 10px;
  }
`;

const LogoutButton = styled.button.attrs({
  className: "bg-red f3 w-100 white bn pointer outline-0",
})`
  height: 60px;
`;

export { LogoutButton, MenuButton, SidebarContainer, SidebarMenu };
