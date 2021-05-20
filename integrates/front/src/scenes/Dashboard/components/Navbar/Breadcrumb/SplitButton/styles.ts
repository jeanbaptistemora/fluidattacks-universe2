import styled from "styled-components";

const LastOrg = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `br0 outline-0 ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

const IconButton = styled.button.attrs(
  ({
    className,
    type,
  }): Partial<React.ButtonHTMLAttributes<HTMLButtonElement>> => ({
    className: `br0 outline-0 ph0 ${className ?? ""}`,
    type: type ?? "button",
  })
)``;

export { IconButton, LastOrg };
