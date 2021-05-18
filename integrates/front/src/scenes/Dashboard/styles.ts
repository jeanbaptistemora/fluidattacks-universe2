import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-row h-100",
})``;

const DashboardContent = styled.div.attrs({
  className: "flex flex-auto flex-column overflow-container",
})`
  @media (max-width: 768px) {
    margin-left: 50px;
  }
`;

const DashboardHeader = styled.header.attrs({
  className: "top-0 z-5",
})`
  @media (min-width: 768px) {
    position: sticky;
  }
`;

export { DashboardContainer, DashboardContent, DashboardHeader };
