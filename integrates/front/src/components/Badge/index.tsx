import styled from "styled-components";

interface IBadgeProps {
  variant: "gray" | "green" | "orange" | "red";
}

const getBackground = (variant: IBadgeProps["variant"]): string => {
  if (variant === "green") {
    return "#c2ffd4";
  } else if (variant === "orange") {
    return "#ffebd6";
  } else if (variant === "red") {
    return "#ffd6d6";
  }

  return "#e9e9ed";
};

const getColor = (variant: IBadgeProps["variant"]): string => {
  if (variant === "green") {
    return "#009245";
  } else if (variant === "orange") {
    return "#ff961e";
  } else if (variant === "red") {
    return "#ff3435";
  }

  return "#2e2e38";
};

const Badge = styled.span<IBadgeProps>`
  background-color: ${(props): string => getBackground(props.variant)};
  border-radius: 50px;
  color: ${(props): string => getColor(props.variant)};
  font-weight: 400;
  padding: 4px 12px;
`;

export { Badge, IBadgeProps };
