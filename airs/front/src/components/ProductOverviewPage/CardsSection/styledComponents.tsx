import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-gray-36
    center
    flex
    flex-wrap
    ph-body
  `,
})``;

const CardContainer = styled.div.attrs({
  className: `
    bg-fluid-black
    center
    mv5
    pv4
    ph3
    tc
    br3
    w-100
  `,
})`
  max-width: 424px;
`;

const CardTitle = styled.p.attrs({
  className: `
    white
    roboto
    f3
    mb1
    fw7
    mv4
  `,
})``;

const CardText = styled.p.attrs({
  className: `
    c-fluid-gray
    b
    mt0
    f5
    roboto
  `,
})``;

export { CardContainer, CardText, CardTitle, Container };
