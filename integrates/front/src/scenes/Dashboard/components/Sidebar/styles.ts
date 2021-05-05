import styled from "styled-components";

import logo from "resources/integrates_sidebar.svg";

const SidebarContainer = styled.aside.attrs({
  className: "flex flex-column",
})`
  background-color: #272727;
  transition: width 0.3s, left 0.3s;
  width: 210px;
`;

const SidebarMenu = styled.ul.attrs({
  className: "pl0 list flex-auto content-start",
})``;

const Logo = styled.img.attrs({
  alt: "integrates-logo",
  className: "ml2 pointer",
  src: logo,
})`
  width: 190px;
  min-width: 116px;
`;

const MenuButton = styled.button.attrs({
  className: "white ph3 pv2 w-100 bn pointer outline-0 tl nowrap",
})`
  background: none;
  & svg {
    margin-right: 10px;
  }
`;

const ExtraInfo = styled.div.attrs({
  className: "tr flex-auto content-end white mr1",
})``;

const LogoutButton = styled.button.attrs({
  className: "bg-red f3 w-100 white bn pointer outline-0 flex-auto content-end",
})`
  height: 60px;
`;

export {
  ExtraInfo,
  Logo,
  LogoutButton,
  MenuButton,
  SidebarContainer,
  SidebarMenu,
};
