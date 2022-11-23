import styled from "styled-components";

const ImgBox = styled.div`
  align-items: center;
  background-color: #e9e9ed;
  border-radius: 4px 4px 0 0;
  display: flex;
  height: 7.5em;
  justify-content: center;
  overflow: hidden;
  position: relative;

  > * {
    border-radius: 4px 4px 0 0;
    display: block;
    max-height: 122%;
    min-height: 100%;
    width: 100%;
  }
`;

export { ImgBox };
