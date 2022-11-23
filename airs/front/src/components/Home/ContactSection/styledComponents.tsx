import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    bg-black-18
    center
    flex
    flex-wrap
    ph-body
    justify-center
  `,
})``;

const WhiteTitle = styled.p.attrs({
  className: `
    poppins
    f3
    white
    lh-copy
    fw6
    ma0
    mr3-l
  `,
})``;

const InnerSection = styled.div.attrs({
  className: `
  w5-l
  mv4
  mh3
  tc
`,
})``;

const SocialContainer = styled.div.attrs({
  className: `
  flex
  mt3
`,
})``;

const SocialButton = styled.button.attrs({
  className: `
  ba
  pa2
  br3
  mr1
  pointer
  bc-gray-64
  social-button
  bg-transparent
`,
})``;

export { Container, InnerSection, SocialContainer, SocialButton, WhiteTitle };
