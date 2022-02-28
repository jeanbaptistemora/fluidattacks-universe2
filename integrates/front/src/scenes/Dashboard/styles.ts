import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-row h-100",
})`
  font-family: "Roboto", sans-serif;
  font-size: 16px;
`;

const DashboardContent = styled.div.attrs({
  className: "flex flex-auto flex-column overflow-container",
})`
  padding-left: 24px;
  padding-right: 24px;

  // Hide scrollbar for Chrome, Safari and Opera
  ::-webkit-scrollbar {
    display: none;
  }
  // Hide scrollbar for IE, Edge and Firefox
  -ms-overflow-style: none;
  scrollbar-width: none;
`;

const DashboardHeader = styled.header.attrs({
  className: "top-0 z-5",
})``;

export { DashboardContainer, DashboardContent, DashboardHeader };
