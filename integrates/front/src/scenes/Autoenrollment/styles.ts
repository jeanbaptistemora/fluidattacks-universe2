import styled from "styled-components";

const Container = styled.div.attrs({
  className: "flex flex-row h-100",
})`
  background-color: #e9e9ed;
  color: #2e2e38;
  font-family: "Roboto", sans-serif;
  font-size: 16px;
`;

const DashboardContent = styled.div.attrs({
  className: "flex flex-auto flex-column overflow-container",
})`
  margin-top: auto;
  margin-bottom: auto;
  padding-left: 24px;
  padding-right: 24px;
`;

const FormContent = styled.div.attrs({
  className: "col-1",
})`
  margin: 16px 0 0;
  padding: 24px 24px 24.2px;
  border-radius: 6px;
  background-color: #f4f4f6;
`;

export { Container, DashboardContent, FormContent };
