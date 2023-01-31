import styled from "styled-components";

const DashboardContainer = styled.div.attrs({
  className: "flex flex-column h-100",
})`
  background-color: #e9e9ed;
  color: #2e2e38;
  font-family: Roboto, sans-serif;
  font-size: 14px;
`;

const DashboardContent = styled.main.attrs({
  className: "flex flex-auto flex-column",
})`
  overflow-y: auto;
  padding: 4px 24px 72px 24px;

  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: #b0b0bf;
  }

  ::-webkit-scrollbar-thumb {
    background: #65657b;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: #535365;
  }
`;

export { DashboardContainer, DashboardContent };
