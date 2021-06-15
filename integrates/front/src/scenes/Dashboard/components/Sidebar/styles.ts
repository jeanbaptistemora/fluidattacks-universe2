import styled from "styled-components";

import logo from "resources/asm_sidebar.svg";
import preloader from "resources/loading.gif";

const SidebarContainer = styled.aside.attrs({
  className: "flex flex-column overflow-x-hidden",
})`
  transition: all 0.3s ease;
  background-color: #272727;
  width: ${(props: { collapsed: boolean }): string =>
    props.collapsed ? "50px" : "210px"};
  min-width: ${(props: { collapsed: boolean }): string =>
    props.collapsed ? "50px" : "210px"};
  @media (max-width: 768px) {
    height: 100%;
    position: fixed;
    z-index: 999;
  }
`;

const SidebarMenu = styled.ul.attrs({
  className: "flex-auto list mt2 pl0",
})``;

const Logo = styled.img.attrs({
  alt: "App logo",
  className: "ml2 pointer",
  src: logo,
})`
  width: 190px;
  min-width: 116px;
`;

const SidebarButton = styled.button.attrs({
  className: "white ph3 pv2 f4 w-100 bn pointer outline-0 tl nowrap",
})`
  background: none;
  & svg {
    margin-right: 10px;
  }
`;

const Preloader = styled.img.attrs({
  alt: "Loading animation",
  className: "ml-auto",
  src: preloader,
})`
  width: 100px;
`;

export { Logo, Preloader, SidebarButton, SidebarContainer, SidebarMenu };
