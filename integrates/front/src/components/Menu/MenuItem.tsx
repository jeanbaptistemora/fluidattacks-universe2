import styled from "styled-components";

const MenuItem = styled.li.attrs({
  className: "hover-bg-light-gray pointer tl w-100",
})`
  > a,
  button {
    color: #777;
    display: inline-block;
    padding: 0.5rem 1rem;
    width: 100%;
  }
  > button {
    background-color: transparent;
    border: none;
    cursor: pointer;
    text-align: left;
  }
  & svg {
    height: 18px;
    width: 18px;
    margin-right: 5px;
  }
`;

export { MenuItem };
