import styled from "styled-components";

const CloseButton = styled.button`
  background-color: transparent;
  border: 1px solid #2e2e38;
  border-radius: 100%;
  color: #2e2e38;
  display: flex;
  font-size: 8px;
  margin-left: 8px;
  padding: 2px 3px 2px 3px;
  transition: all 0.3s ease;

  :hover {
    background-color: #2e2e38;
    color: #fff;
    cursor: pointer;
  }
`;

export { CloseButton };
