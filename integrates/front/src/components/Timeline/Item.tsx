import React from "react";
import styled from "styled-components";

const ItemContainer = styled.li.attrs({ className: "relative" })`
  padding: 10px 40px;
  width: 50%;

  ::after {
    background-color: white;
    border-radius: 50%;
    border: 4px solid #bf0b1a;
    content: "";
    height: 24px;
    position: absolute;
    top: 15px;
    width: 24px;
    z-index: 1;
  }

  ::before {
    border-style: solid;
    content: " ";
    position: absolute;
    top: 22px;
  }

  @media (max-width: 768px) {
    padding-left: 70px;
    padding-right: 25px;
    width: 100%;
  }
`;

const ItemContent = styled.article.attrs({ className: "bg-white" })`
  border-radius: 6px;
  box-shadow: 0px 8px 16px 0px rgb(92 92 112 / 20%);
  padding: 20px 30px;
  text-align: left;

  p {
    color: #5c5c70;
  }
`;

interface ITimelineItemProps {
  children: React.ReactNode;
}

const TimelineItem: React.FC<ITimelineItemProps> = ({
  children,
}: ITimelineItemProps): JSX.Element => {
  return (
    <ItemContainer>
      <ItemContent>{children}</ItemContent>
    </ItemContainer>
  );
};

export { TimelineItem };
