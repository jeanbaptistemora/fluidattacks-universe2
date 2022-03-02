import styled from "styled-components";

const ButtonCol = styled.div.attrs({
  className: "flex flex-auto items-center justify-end",
})``;

const TitleContainer = styled.div.attrs({ className: "flex flex-wrap pa3" })`
  background-color: #f4f4f6;
`;

const Title = styled.h1.attrs({ className: "ma0 pa0" })``;

export { ButtonCol, Title, TitleContainer };
