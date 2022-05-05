import styled from "styled-components";

const Container = styled.div.attrs({
  className: `
    h-500
    bg-darker-blue
    center
    flex
    flex-wrap
  `,
})``;

const ClientsContainer = styled.div.attrs({
  className: `
    w-100
    mw-1920
    relative
    center
    overflow-hidden
    home-clients-container
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

const ArrowButton = styled.button.attrs({
  className: `
    bg-fluid-gray
    bn
    pa3
    dib
    pointer
    outline-transparent
  `,
})``;

const SlideShow = styled.div.attrs({
  className: `
    home-slide-track
    flex
  `,
})``;

const ArrowContainer = styled.div.attrs({
  className: `
    bt
    b--light-gray
    tr
  `,
})``;

export {
  ArrowButton,
  ArrowContainer,
  ClientsContainer,
  Container,
  SlideShow,
  TitleContainer,
};
