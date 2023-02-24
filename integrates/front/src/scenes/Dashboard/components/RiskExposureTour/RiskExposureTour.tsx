import { faClose } from "@fortawesome/free-solid-svg-icons";
import React, { useCallback, useContext, useState } from "react";
import { useHistory, useRouteMatch } from "react-router-dom";

import type { IRiskExposureTourProps } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";
import { BaseStep, Tour } from "components/Tour";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";

const RiskExposureTour: React.FC<IRiskExposureTourProps> = ({
  findingId,
  findingRiskExposure,
  step,
}): JSX.Element => {
  const { push } = useHistory();
  const { url } = useRouteMatch();

  const tourStyle = {
    options: {
      arrowColor: "#2e2e38",
      backgroundColor: "#2e2e38",
      overlayColor: "transparent",
      primaryColor: "#000",
      textColor: "#fff",
      width: 450,
    },
  };

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const enableExposureRiskTour = !user.tours.newRiskExposure;
  const [runRiskExposureTour, setRunRiskExposureTour] = useState(
    enableExposureRiskTour
  );

  const finishTour = useCallback((): void => {
    user.setUser({
      tours: {
        newGroup: user.tours.newGroup,
        newRiskExposure: true,
        newRoot: user.tours.newRoot,
        welcome: user.tours.welcome,
      },
      userEmail: user.userEmail,
      userIntPhone: user.userIntPhone,
      userName: user.userName,
    });
    setRunRiskExposureTour(false);
  }, [setRunRiskExposureTour, user]);

  const goToFirstFinding = useCallback((): void => {
    push(`${url}/${findingId ?? ""}/locations`);
  }, [findingId, push, url]);

  if (runRiskExposureTour && step === 1) {
    return (
      <Tour
        onFinish={finishTour}
        run={runRiskExposureTour}
        steps={[
          {
            ...BaseStep,
            content: (
              <Container>
                <Container align={"center"} display={"flex"} justify={"end"}>
                  <Button
                    icon={faClose}
                    id={"close-tour"}
                    onClick={finishTour}
                    variant={"secondary"}
                  />
                </Container>
                <Container pt={"10px"}>
                  <Text
                    fw={7}
                    mb={2}
                    tone={"light"}
                  >{`New feature: ${findingRiskExposure} Risk Exposure.`}</Text>
                  <Text tone={"light"}>
                    <Text disp={"inline"} fw={7} tone={"light"}>
                      {"Accelerate remediation "}
                    </Text>
                    {"prioritizing by Risk Exposure."}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text tone={"light"}>{"1/2"}</Text>
                  <Button onClick={goToFirstFinding} variant={"secondary"}>
                    {"Next"}
                  </Button>
                </Container>
              </Container>
            ),
            hideCloseButton: true,
            placement: "auto",
            styles: tourStyle,
            target: "#riskExposureColumn",
          },
        ]}
      />
    );
  }

  if (runRiskExposureTour && step === 2) {
    return (
      <Tour
        onFinish={finishTour}
        run={runRiskExposureTour}
        steps={[
          {
            ...BaseStep,
            content: (
              <Container>
                <Container align={"center"} display={"flex"} justify={"end"}>
                  <Button
                    icon={faClose}
                    id={"close-tour"}
                    onClick={finishTour}
                    variant={"secondary"}
                  />
                </Container>
                <Container pt={"10px"}>
                  <Text fw={7} mb={2} tone={"light"}>
                    {"% Risk Exposure"}
                  </Text>
                  <Text tone={"light"}>
                    {`For example, decrease ${findingRiskExposure} of your Total Risk Exposure by fixing all the vulnerabilities of this type`}
                  </Text>
                </Container>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text tone={"light"}>{"2/2"}</Text>
                  <Button onClick={finishTour} variant={"secondary"}>
                    {"Close"}
                  </Button>
                </Container>
              </Container>
            ),
            hideCloseButton: true,
            placement: "auto",
            styles: tourStyle,
            target: "#riskExposureCard",
          },
        ]}
      />
    );
  }

  return <div />;
};

export { RiskExposureTour };
