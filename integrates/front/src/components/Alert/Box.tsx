import type { IconDefinition } from "@fortawesome/fontawesome-common-types";
import {
  faCheckCircle,
  faCircleExclamation,
  faCircleInfo,
  faTriangleExclamation,
} from "@fortawesome/free-solid-svg-icons";
import styled from "styled-components";

type TAlertVariant = "error" | "info" | "success" | "warning";

interface IAlertBoxProps {
  show?: boolean;
  variant?: TAlertVariant;
}

interface IVariant {
  bgColor: string;
  border: string;
  color: string;
  icon: IconDefinition;
}

const variants: Record<TAlertVariant, IVariant> = {
  error: {
    bgColor: "#f2dede",
    border: "#bf101a",
    color: "#a94442",
    icon: faCircleExclamation,
  },
  info: {
    bgColor: "#e5f6fd",
    border: "#2d5cc8",
    color: "#014361",
    icon: faCircleInfo,
  },
  success: {
    bgColor: "#c2ffd4",
    border: "#279244",
    color: "#009245",
    icon: faCheckCircle,
  },
  warning: {
    bgColor: "#fff4e5",
    border: "#fccd01",
    color: "#663c00",
    icon: faTriangleExclamation,
  },
};

const AlertBox = styled.div.attrs({
  className: "comp-alert",
})<IAlertBoxProps>`
  align-items: start;
  border-radius: 4px;
  display: flex;
  font-size: 16px;
  justify-content: space-between;
  overflow: hidden;
  transition: all 0.3s ease;

  ${({ show = true, variant = "error" }): string => `
    background-color: ${variants[variant].bgColor};
    border-left: 3px ${variants[variant].border} solid;
    color: ${variants[variant].color};
    height: ${show ? "auto" : 0};
    padding: ${show ? "10px 12px" : 0};
  `}

  > .comp-button {
    background-color: transparent !important;
    border: none !important;
    padding: 1px 5px;
  }
`;

const ContentBox = styled.div`
  flex-grow: 1;
  margin-left: 12px;
  margin-right: 12px;
`;

export type { IAlertBoxProps, TAlertVariant };
export { AlertBox, ContentBox, variants };
