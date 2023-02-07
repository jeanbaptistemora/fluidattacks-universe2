import { useMutation } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import React, { useCallback, useContext, useState } from "react";
import { useTranslation } from "react-i18next";
import { useHistory, useRouteMatch } from "react-router-dom";

import type { IRiskExposureTourProps } from "./types";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Text } from "components/Text";
import { BaseStep, Tour } from "components/Tour";
import { UPDATE_TOURS } from "components/Tour/queries";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

const RiskExposureTour: React.FC<IRiskExposureTourProps> = ({
  findingId,
  findingRiskExposure,
  step,
}): JSX.Element => {
  const { push } = useHistory();
  const { url } = useRouteMatch();
  const { t } = useTranslation();

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const enableExposureRiskTour = !user.tours.newRiskExposure;
  const [runRiskExposureTour, setRunRiskExposureTour] = useState(
    enableExposureRiskTour
  );

  const [updateTours] = useMutation(UPDATE_TOURS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error): void => {
        msgError(t("groupAlerts.errorTextsad"));
        Logger.warning("An error occurred fetching exposure risk tour", error);
      });
    },
  });

  const finishTour = useCallback((): void => {
    void updateTours({
      variables: {
        newGroup: user.tours.newGroup,
        newRiskExposure: true,
        newRoot: user.tours.newRoot,
      },
    });
    setRunRiskExposureTour(false);
  }, [setRunRiskExposureTour, updateTours, user]);

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
              <Container pt={"10px"}>
                <Text
                  fw={7}
                  mb={2}
                >{`New feature: ${findingRiskExposure} Risk Exposure.`}</Text>
                <Text>
                  <Text disp={"inline"} fw={7}>
                    {"Accelerate remediation "}
                  </Text>
                  {"prioritizing by Risk Exposure."}
                </Text>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text>{"1/2"}</Text>
                  <Button onClick={goToFirstFinding} variant={"primary"}>
                    {"Next"}
                  </Button>
                </Container>
              </Container>
            ),
            placement: "auto",
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
              <Container pt={"10px"}>
                <Text fw={7} mb={2}>
                  {"% Risk Exposure"}
                </Text>
                <Text>
                  {`For example, decrease ${findingRiskExposure} of your Total Risk Exposure by fixing all the vulnerabilities of this type`}
                </Text>
                <Container
                  align={"center"}
                  display={"flex"}
                  justify={"space-between"}
                  pt={"10px"}
                >
                  <Text>{"2/2"}</Text>
                  <Button onClick={finishTour} variant={"primary"}>
                    {"Close"}
                  </Button>
                </Container>
              </Container>
            ),
            placement: "auto",
            target: "#riskExposureCard",
          },
        ]}
      />
    );
  }

  return <div />;
};

export { RiskExposureTour };
