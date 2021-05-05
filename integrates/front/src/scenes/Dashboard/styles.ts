import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-row h-100",
})``;

const DashboardContent = styled.div.attrs({
  className: "flex-auto overflow-container",
})`
  @media (max-width: 768px) {
    margin-left: 50px;
  }
`;

export { DashboardContainer, DashboardContent };
