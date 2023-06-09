/* eslint react/jsx-no-bind:0 */
/* eslint react/forbid-component-props: 0 */
import { useMatomo } from "@datapunt/matomo-tracker-react";
import { Link } from "gatsby";
import React, { useCallback } from "react";

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
import { Text } from "../../../Typography";

const PlanCard: React.FC<IPlansCard> = ({
  description,
  isMachine,
  items,
  title,
}: IPlansCard): JSX.Element => {
  const { trackEvent } = useMatomo();

  const matomoFreeTrialEvent = useCallback((): void => {
    trackEvent({
      action: "card-free-trial-click",
      category: "plans",
    });
  }, [trackEvent]);

  return (
    <div className={"mh3"}>
      {isMachine ? (
        <MachineHead>{"Try it free for 21 days"}</MachineHead>
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
          <Paragraph
            fColor={"#5c5c70"}
            fSize={"20"}
            marginBottom={isMachine ? "1.3" : "0"}
          >
            {description}
          </Paragraph>
          {isMachine ? (
            <Link onClick={matomoFreeTrialEvent} to={"/free-trial"}>
              <NewRegularRedButton className={"mv4 w-100"}>
                <Text color={"inherit"}>{"Start free trial"}</Text>
              </NewRegularRedButton>
            </Link>
          ) : (
            <Link to={"/contact-us-demo"}>
              <PhantomRegularRedButton className={"mv4 w-100"}>
                <Text color={"inherit"}>{"Request a demo"}</Text>
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
                <Text color={"inherit"}>{item.text}</Text>
              </CardItem>
            );
          })}
        </CardItemsContainer>
      </CardContainer>
    </div>
  );
};

export { PlanCard };
