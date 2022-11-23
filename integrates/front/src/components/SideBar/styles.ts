import styled from "styled-components";

const SideBarBox = styled.div.attrs({
  className: "SideBar h-100",
})`
  background-color: #2e2e38;
  color: #c7c7d1;
  display: inline-block;
  min-width: 150px;
  padding: 12px 0;
`;

const SideBarSubTabs = styled.div`
  > .SideBarTab:not(:last-child)::after {
    content: none;
  }
`;

export { SideBarBox, SideBarSubTabs };
