import styled from "styled-components";

const ButtonContainer = styled.div.attrs({
  className: `
    flex
    relative
    pointer
    poppins
  `,
})<{ isRight: boolean }>`
  width: 50px;
  height: 50px;
  z-index: 1;
  left: ${({ isRight }): string => (isRight ? "-25px" : "25px")};
  float: ${({ isRight }): string => (isRight ? "left" : "right")};
  top: 50%;

  :hover > div + div {
    opacity: 0.4;
  }

  :hover > div + div + div {
    opacity: 0.2;
  }
`;

const FirstCircle = styled.div.attrs({
  className: `
    absolute
  `,
})`
  border-radius: 100%;
  background-color: #ff7070;
  width: 30px;
  height: 30px;
  top: 20%;
  left: 20%;
`;

const SecondCircle = styled.div.attrs({
  className: `
    absolute
  `,
})`
  border-radius: 100%;
  background-color: #ff7070;
  width: 40px;
  height: 40px;
  opacity: 0.2;
  top: 10%;
  left: 10%;
`;

const ThirdCircle = styled.div.attrs({
  className: `
    dib
    relative
  `,
})`
  border-radius: 100%;
  background-color: #ff7070;
  width: 50px;
  height: 50px;
  opacity: 0.1;
`;

export { ButtonContainer, FirstCircle, SecondCircle, ThirdCircle };
