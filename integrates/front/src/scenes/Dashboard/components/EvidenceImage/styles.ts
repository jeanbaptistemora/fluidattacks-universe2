import styled from "styled-components";

const DescriptionContainer = styled.div`
  border-top: 1px solid #ddd;
  padding: 20px 20px 15px;
  word-break: break-word;
`;

const ImageContainer = styled.div`
  border-width: 0;
  box-shadow: none;
  margin-bottom: 30px;
  padding: 15px 20px 20px;

  div:empty,
  img,
  svg,
  video {
    background-color: #f0f0f0;
    border-radius: 0;
    border: 1px solid #ddd;
    cursor: pointer;
    display: inline-block;
    font-size: 150px;
    height: 600px;
    line-height: 1.4286;
    max-height: 250px;
    max-width: 100%;
    padding: 4px;
    text-align: center;
    vertical-align: middle;
    width: 600px;
    transition: all 0.2s ease-in-out;

    @media (min-width: 768px) and (max-width: 1199px) {
      height: 200px !important;
    }

    @media (min-width: 1200px) {
      height: 250px !important;
    }
  }
`;

export { DescriptionContainer, ImageContainer };
