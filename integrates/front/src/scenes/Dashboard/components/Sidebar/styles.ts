import styled from "styled-components";

const MenuButton = styled.button.attrs({
  className: "white ph3 pv2 w-100 bn pointer outline-0 tl nowrap",
})`
  background: none;
  & svg {
    margin-right: 10px;
  }
`;

const LogoutButton = styled.button.attrs({
  className: "bg-red f3 w-100 white bn pointer outline-0",
})`
  height: 60px;
`;

export { LogoutButton, MenuButton };
