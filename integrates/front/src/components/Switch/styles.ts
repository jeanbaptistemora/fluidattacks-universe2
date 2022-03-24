import styled from "styled-components";

const Slider = styled.span.attrs({
  className: "absolute absolute--fill pointer",
})`
  background-color: #d2d2da;
  border-radius: 34px;
  transition: 0.4s;

  span {
    bottom: 5px;
    color: #5c5c70;
    height: 16px;
    left: 21px;
    position: absolute;
    transition: 0.4s;
  }

  :before {
    background-color: #f4f4f6;
    border-radius: 50%;
    bottom: 4px;
    content: "";
    height: 16px;
    left: 4px;
    position: absolute;
    transition: 0.4s;
    width: 16px;
    z-index: 1;
  }
`;

const Container = styled.label.attrs({ className: "dib mh2 relative v-mid" })`
  height: 24px;
  width: 48px;

  input {
    height: 0;
    opacity: 0;
    width: 0;
  }

  input:checked + ${Slider} {
    background-color: #5c5c70;
  }

  input:checked + ${Slider} span {
    color: #d2d2da;
    transform: translateX(-19px);
  }

  input:checked + ${Slider}:before {
    transform: translateX(24px);
  }

  input:disabled + ${Slider} {
    cursor: not-allowed;
    opacity: 0.5;
  }
}
`;

export { Container, Slider };
