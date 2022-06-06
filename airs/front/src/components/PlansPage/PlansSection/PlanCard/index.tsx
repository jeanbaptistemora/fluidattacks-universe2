/* eslint react/forbid-component-props: 0 */
import { Link } from "gatsby";
import React from "react";

import {
  CardContainer,
  CardItem,
  CardItemsContainer,
  CardTitleContainer,
  MachineHead,
} from "./styledComponents";
import type { IPlansCard } from "./types";

import {
  NewRegularRedButton,
  PhantomRegularRedButton,
} from "../../../../styles/styledComponents";
import { CloudImage } from "../../../CloudImage";
import { Paragraph, Title } from "../../../Texts";

const PlanCard: React.FC<IPlansCard> = ({
  description,
  isMachine,
  items,
  title,
}: IPlansCard): JSX.Element => {
  return (
    <div className={"mh3"}>
      {isMachine ? (
        <MachineHead>{"Try it free for 30 days"}</MachineHead>
      ) : undefined}
      <CardContainer isMachine={isMachine}>
        <CardTitleContainer>
          <CloudImage
            alt={`Plan ${title} Fluid Attacks`}
            src={`airs/plans/${isMachine ? "machine" : "squad"}`}
            styles={`mr1 ${isMachine ? "machine-icon" : "squad-icon"}`}
          />
          <Title fColor={"#24252d"} fSize={"32"} marginTop={"1"}>
            {title}
          </Title>
        </CardTitleContainer>
        <CardItemsContainer>
          <Paragraph fColor={"#5c5c70"} fSize={"20"}>
            {description}
          </Paragraph>
          {isMachine ? (
            <Link to={"/contact-us"}>
              <NewRegularRedButton className={"mv4 w-100"}>
                {"Contact sales"}
              </NewRegularRedButton>
            </Link>
          ) : (
            <Link to={"/contact-us"}>
              <PhantomRegularRedButton className={"mv4 w-100"}>
                {"Contact sales"}
              </PhantomRegularRedButton>
            </Link>
          )}
          {items.map((item): JSX.Element => {
            return (
              <CardItem key={`${item.text}`}>
                <CloudImage
                  alt={`plan-check`}
                  src={`airs/plans/${item.check ? "check" : "xmark"}`}
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
