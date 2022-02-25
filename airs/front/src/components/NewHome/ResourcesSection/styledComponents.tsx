import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    white
    center
    ph-body
  `,
})``;

const TitleContainer = styled.div.attrs({
  className: `
    w-100
    tc
    mt5
    ph-body
  `,
})``;

const BlackParagraph = styled.p.attrs({
  className: `
    neue
    f3
    c-fluid-bk
    lh-copy
    fw6
    ma0
    mr3-l
  `,
})``;

export { BlackParagraph, Container, TitleContainer };
