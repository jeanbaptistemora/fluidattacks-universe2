import styled from "styled-components";

const CloseButton = styled.button`
  background-color: transparent;
  border: 1px solid #bf0b1a;
  border-radius: 100%;
  color: #bf0b1a;
  display: flex;
  font-size: 8px;
  margin-left: 8px;
  padding: 2px 3px 2px 3px;
  transition: all 0.3s ease;

  :hover {
    background-color: #bf0b1a;
    color: #fff;
    cursor: pointer;
  }
`;

export { CloseButton };
