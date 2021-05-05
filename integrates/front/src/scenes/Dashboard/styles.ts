import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-row h-100",
})``;

const DashboardContent = styled.div.attrs({
  className: "flex-auto overflow-container",
})`
  @media (min-width: 768px) {
    margin-left: 210px;
  }
`;

export { DashboardContainer, DashboardContent };
