import styled from "styled-components";

import preloader from "resources/loading.gif";

const SidebarContainer = styled.aside.attrs({
  className: "flex flex-column overflow-x-hidden",
})`
  background-color: #2e2e38;
  border-right: 1px solid #5c5c70;
  height: 100%;
  min-width: 72px;
  width: 72px;
`;

const SidebarMenu = styled.ul.attrs({
  className: "flex-auto list mt2 pl0",
})``;

const Preloader = styled.img.attrs({
  alt: "Loading animation",
  className: "ml-auto",
  src: preloader,
})`
  width: 100px;
`;

export { Preloader, SidebarContainer, SidebarMenu };
