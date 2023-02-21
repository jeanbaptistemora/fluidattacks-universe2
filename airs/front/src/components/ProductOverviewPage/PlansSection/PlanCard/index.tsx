/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React, { useCallback, useState } from "react";
import { FiMinus, FiPlus } from "react-icons/fi";

import {
  CardContainer,
  CardItem,
  CardItemsContainer,
  CardParagraph,
  CardTitle,
  CardTitleContainer,
  MachineButton,
  OpenButton,
} from "./styledComponents";
import type { IPlansCard } from "./types";

import { CloudImage } from "../../../CloudImage";

const PlanCard: React.FC<IPlansCard> = ({
  description,
  isMachine,
  items,
  title,
}: IPlansCard): JSX.Element => {
  const [isOpen, setIsOpen] = useState(false);
  const handleOpenClose = useCallback((): void => {
    setIsOpen(!isOpen);
  }, [isOpen]);

  return (
    <div className={"w-100 mh3"}>
      {isMachine ? (
        <Link to={"/contact-us-demo/"}>
          <MachineButton>{"Try for free 30 days"}</MachineButton>
        </Link>
      ) : undefined}
      <CardContainer isMachine={isMachine}>
        <CardTitleContainer isOpen={isOpen}>
          <CardTitle>
            <CloudImage
              alt={`Plan ${title} Fluid Attacks`}
              src={`airs/platform/plans-section/${
                isMachine ? "machine" : "squad"
              }`}
              styles={"mr1"}
            />
            {title}
            <OpenButton onClick={handleOpenClose}>
              {isOpen ? <FiPlus /> : <FiMinus />}
            </OpenButton>
          </CardTitle>
        </CardTitleContainer>
        <CardItemsContainer isOpen={isOpen}>
          <CardParagraph isOpen={isOpen}>{description}</CardParagraph>
          {items.map((item): JSX.Element => {
            return (
              <CardItem key={`${item.text}`}>
                <CloudImage
                  alt={`plan-check`}
                  src={`airs/platform/plans-section/${
                    item.check ? "check" : "xmark"
                  }`}
                  styles={"mr3 check-icon"}
                />
                {item.text}
              </CardItem>
            );
          })}
        </CardItemsContainer>
      </CardContainer>
    </div>
  );
};

export { PlanCard };
