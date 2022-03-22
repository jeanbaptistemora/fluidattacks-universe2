import styled from "styled-components";

const Slider = styled.span.attrs({
  className: "absolute absolute--fill pointer",
})`
  background-color: #d2d2da;
  border-radius: 34px;
  transition: 0.4s;

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
  }
`;

const Container = styled.label.attrs({ className: "dib mh2 relative" })`
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

  input:checked + ${Slider}:before {
    transform: translateX(24px);
  }
}
`;

export { Container, Slider };
