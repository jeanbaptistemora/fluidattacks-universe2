import styled from "styled-components";

const ScrollContainer = styled.div`
  height: 100%;
  overflow-x: hidden;
  overflow-y: auto;

  ::-webkit-scrollbar {
    width: 8px;
  }
  ::-webkit-scrollbar-track {
    background: #b0b0bf;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb {
    background: #65657b;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #535365;
  }
`;

export { ScrollContainer };
