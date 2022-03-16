import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Field, Label } from "./styles";

import { Col, Row } from "components/Layout";
import { commitFormatter } from "components/Table/formatters";
import { GET_VULN_ADDITIONAL_INFO } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import type { IGetVulnAdditionalInfoAttr } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/types";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { Status } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import type { IVulnRowAttr } from "scenes/Dashboard/components/Vulnerabilities/types";
import { Logger } from "utils/logger";
import { msgError } from "utils/notifications";

interface IAdditionalInfoProps {
  canRetrieveHacker: boolean;
  vulnerability: IVulnRowAttr;
}

const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canRetrieveHacker,
  vulnerability,
}: IAdditionalInfoProps): JSX.Element => {
  const { t } = useTranslation();

  const vulnId = vulnerability.id;

  const { data } = useQuery<IGetVulnAdditionalInfoAttr>(
    GET_VULN_ADDITIONAL_INFO,
    {
      onError: ({ graphQLErrors }: ApolloError): void => {
        graphQLErrors.forEach((error: GraphQLError): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred loading the vulnerability info",
            error
          );
        });
      },
      variables: {
        canRetrieveHacker,
        vulnId,
      },
    }
  );

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.StrictMode />;
  }

  const isVulnOpen: boolean = vulnerability.currentState === "open";
  const currentExpiration: string =
    isVulnOpen &&
    data.vulnerability.treatment === "ACCEPTED" &&
    !_.isNull(data.vulnerability.treatmentAcceptanceDate)
      ? data.vulnerability.treatmentAcceptanceDate.split(" ")[0]
      : "";
  const currentJustification: string =
    !isVulnOpen ||
    _.isUndefined(data.vulnerability.treatmentJustification) ||
    _.isNull(data.vulnerability.treatmentJustification)
      ? ""
      : data.vulnerability.treatmentJustification;
  const currentAssigned: string = isVulnOpen
    ? (data.vulnerability.treatmentAssigned as string)
    : "";
  const treatmentDate: string = isVulnOpen
    ? data.vulnerability.lastTreatmentDate.split(" ")[0]
    : "";

  const treatmentChanges = parseInt(data.vulnerability.treatmentChanges, 10);

  const vulnerabilityType: string = t(
    `searchFindings.tabVuln.vulnTable.vulnerabilityType.${data.vulnerability.vulnerabilityType}`
  );

  return (
    <React.StrictMode>
      <Row>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Row>
            <Col>
              <h4>{t("searchFindings.tabVuln.vulnTable.location")}</h4>
              <Field>{_.unescape(vulnerability.where)}</Field>
              {_.isEmpty(data.vulnerability.stream) ? undefined : (
                <Field>{data.vulnerability.stream}</Field>
              )}
              <Field>
                {t(
                  `searchFindings.tabVuln.vulnTable.specificType.${vulnerabilityType}`
                )}
                &nbsp;
                <Value value={vulnerability.specific} />
              </Field>
            </Col>
          </Row>
          <Row>
            <Col>
              <h4>{t("searchFindings.tabVuln.vulnTable.reattacks")}</h4>
              <Field>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.lastRequestedReattackDate"
                  )}
                </Label>
                <Value
                  value={
                    data.vulnerability.lastRequestedReattackDate?.split(
                      " "
                    )[0] ?? ""
                  }
                />
              </Field>
              <Field>
                <Label>{t("searchFindings.tabVuln.vulnTable.requester")}</Label>
                <Value value={data.vulnerability.lastReattackRequester} />
              </Field>
              <Field>
                <Label>{t("searchFindings.tabVuln.vulnTable.cycles")}</Label>
                <Value value={data.vulnerability.cycles} />
              </Field>
              <Field>
                <Label>{t("searchFindings.tabVuln.vulnTable.efficacy")}</Label>
                <Value value={data.vulnerability.efficacy} />
              </Field>
            </Col>
          </Row>
          <Row>
            <Col>
              <h4>{t("searchFindings.tabVuln.vulnTable.info")}</h4>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.reportDate")}
                </Label>
                <Value value={data.vulnerability.reportDate.split(" ")[0]} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.closingDate")}
                </Label>
                <Value
                  value={
                    vulnerability.currentState === "closed"
                      ? data.vulnerability.lastStateDate.split(" ")[0]
                      : ""
                  }
                />
              </Field>
              {_.isEmpty(data.vulnerability.commitHash) ? undefined : (
                <Field>
                  <Label>{t("searchFindings.tabVuln.commitHash")}</Label>
                  <Value
                    value={commitFormatter(
                      data.vulnerability.commitHash as string
                    )}
                  />
                </Field>
              )}
              <Field>
                <Label>{t("searchFindings.tabDescription.tag")}</Label>
                <Value value={vulnerability.tag} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabDescription.businessCriticality")}
                </Label>
                <Value
                  value={
                    data.vulnerability.severity === null ||
                    data.vulnerability.severity === "-1"
                      ? ""
                      : data.vulnerability.severity
                  }
                />
              </Field>
              <Field>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.vulnerabilityType.title"
                  )}
                </Label>
                <Value value={vulnerabilityType} />
              </Field>
              <Field>
                <Label>{t("searchFindings.tabDescription.zeroRisk")}</Label>
                {_.isEmpty(vulnerability.zeroRisk) ? (
                  <Value value={undefined} />
                ) : (
                  <Status status={vulnerability.zeroRisk as string} />
                )}
              </Field>
              {canRetrieveHacker ? (
                <Field>
                  <Label>{t("searchFindings.tabDescription.hacker")}</Label>
                  <Value value={data.vulnerability.hacker} />
                </Field>
              ) : undefined}
            </Col>
          </Row>
        </Col>
        <Col large={"50"} medium={"50"} small={"50"}>
          <Row>
            <Col>
              <h4>{t("searchFindings.tabVuln.vulnTable.treatments")}</h4>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.currentTreatment")}
                </Label>
                <Value value={vulnerability.treatment} />
              </Field>
              <Field>
                <Label>{t("searchFindings.tabVuln.vulnTable.assigned")}</Label>
                <Value value={currentAssigned} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentDate")}
                </Label>
                <Value value={treatmentDate} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentExpiration")}
                </Label>
                <Value value={currentExpiration} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentJustification")}
                </Label>
                <Value value={currentJustification} />
              </Field>
              <Field>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentChanges")}
                </Label>
                <Value value={treatmentChanges} />
              </Field>
            </Col>
          </Row>
        </Col>
      </Row>
    </React.StrictMode>
  );
};

export { AdditionalInfo };
