import styled from "styled-components";

const QuestionContainer = styled.div.attrs({
  className: `
    w-100
    pb3
    mb3
  `,
})``;

const QuestionTitle = styled.div.attrs({
  className: `
    pointer
    flex
    f3
    b
    c-fluid-bk
    roboto
    w-100
  `,
})`
  border-bottom: solid 1px #ceced7;
`;

const AnswerContainer = styled.div.attrs({
  className: `
    pv2
    w-100
  `,
})`
  display: none;
`;

const AnswerLabel = styled.p.attrs({
  className: `
    f5
    roboto
  `,
})`
  color: #5c5c70;

  a {
    color: #5c5c70;
  }
`;

const AnswerItem = styled.li.attrs({
  className: `
    f5
    roboto
  `,
})`
  color: #5c5c70;
`;

export {
  AnswerContainer,
  AnswerItem,
  AnswerLabel,
  QuestionContainer,
  QuestionTitle,
};
