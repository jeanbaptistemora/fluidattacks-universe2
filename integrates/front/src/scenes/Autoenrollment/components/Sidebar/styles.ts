import styled from "styled-components";

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

export { SidebarContainer, SidebarMenu };
