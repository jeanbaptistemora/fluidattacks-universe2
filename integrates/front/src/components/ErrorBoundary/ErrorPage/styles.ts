import styled from "styled-components";

const PageContainer = styled.div.attrs({
  className: "flex flex-column h-100 justify-center tc",
})`
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 4px 24px 72px 24px;
  background-color: #e9e9ed;
  color: #2e2e38;
  font-family: Roboto, sans-serif;
  font-size: 16px;
`;

export { PageContainer };
