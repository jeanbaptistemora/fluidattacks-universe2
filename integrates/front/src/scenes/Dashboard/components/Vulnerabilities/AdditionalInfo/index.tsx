import { useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { ClosingDateField } from "./components/ClosingDateField";
import {
  Col100,
  Col50,
  Field,
  InfoField,
  Label,
  LabelField,
  OuterRow,
  Row,
} from "./styles";

import { commitFormatter } from "components/Table/formatters";
import { GET_VULN_ADDITIONAL_INFO } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import type { IGetVulnAdditionalInfoAttr } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/types";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { PointStatus } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
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
      <div className={"pb1 pt2 w-100"}>
        <Col100>
          <b>{t("searchFindings.tabVuln.vulnTable.location")}</b>
        </Col100>
        <div className={"flex flex-wrap pb0"}>
          <div className={"pl1 pr0 pb0 w-100"}>
            <Field>{_.unescape(vulnerability.where)}</Field>
            {_.isEmpty(data.vulnerability.stream) ? undefined : (
              <Field>{data.vulnerability.stream}</Field>
            )}
          </div>
        </div>
        <OuterRow>
          <div className={"pl1 pr0 w-10-l w-100-m w-100-ns"}>
            <Label>
              {t(
                `searchFindings.tabVuln.vulnTable.specificType.${vulnerabilityType}`
              )}
            </Label>
          </div>
          <div className={"pl1 pr0 w-90-l w-100-m w-100-ns"}>
            <Field>{vulnerability.specific}</Field>
          </div>
        </OuterRow>
        <OuterRow>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.reattacks")}</b>
            </Col100>
            <Row>
              <LabelField>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.lastRequestedReattackDate"
                  )}
                </Label>
              </LabelField>
              <InfoField>
                <Value
                  value={
                    data.vulnerability.lastRequestedReattackDate?.split(
                      " "
                    )[0] ?? ""
                  }
                />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.requester")}</Label>
              </LabelField>
              <InfoField>
                <Value value={data.vulnerability.lastReattackRequester} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.cycles")}</Label>
              </LabelField>
              <InfoField>
                <Value value={data.vulnerability.cycles} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.efficacy")}</Label>
              </LabelField>
              <InfoField>
                <Value value={data.vulnerability.efficacy} />
              </InfoField>
            </Row>
          </Col50>
          <Col50>
            <Col100>
              <b>{t("searchFindings.tabVuln.vulnTable.treatments")}</b>
            </Col100>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.currentTreatment")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.treatment} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabVuln.vulnTable.assigned")}</Label>
              </LabelField>
              <InfoField>
                <p
                  className={
                    "f5 lh-title ma0 mid-gray pr1-l tr-l tl-m tl-ns truncate"
                  }
                >
                  {_.isEmpty(currentAssigned)
                    ? t("searchFindings.tabVuln.notApplicable")
                    : currentAssigned}
                </p>
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentDate")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={treatmentDate} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentExpiration")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={currentExpiration} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentJustification")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={currentJustification} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.treatmentChanges")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={treatmentChanges} />
              </InfoField>
            </Row>
          </Col50>
        </OuterRow>
        <OuterRow>
          <Col100>
            <b>{t("searchFindings.tabVuln.vulnTable.info")}</b>
          </Col100>
          <Col50>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabVuln.vulnTable.reportDate")}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={data.vulnerability.reportDate.split(" ")[0]} />
              </InfoField>
            </Row>
            <ClosingDateField
              vulnerability={vulnerability}
              vulnerabilityAdditionalInfo={data.vulnerability}
            />
            {_.isEmpty(data.vulnerability.commitHash) ? undefined : (
              <Row>
                <LabelField>
                  <Label>{t("searchFindings.tabVuln.commitHash")}</Label>
                </LabelField>
                <InfoField>
                  <p
                    className={
                      "lh-title ma0 mid-gray pr1-l tr-l tl-m tl-ns ws-pre-wrap ww-break-word"
                    }
                  >
                    {commitFormatter(data.vulnerability.commitHash as string)}
                  </p>
                </InfoField>
              </Row>
            )}
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabDescription.tag")}</Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerability.tag} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>
                  {t("searchFindings.tabDescription.businessCriticality")}
                </Label>
              </LabelField>
              <InfoField>
                <Value
                  value={
                    data.vulnerability.severity === null ||
                    data.vulnerability.severity === "-1"
                      ? ""
                      : data.vulnerability.severity
                  }
                />
              </InfoField>
            </Row>
          </Col50>
          <Col50>
            <Row>
              <LabelField>
                <Label>
                  {t(
                    "searchFindings.tabVuln.vulnTable.vulnerabilityType.title"
                  )}
                </Label>
              </LabelField>
              <InfoField>
                <Value value={vulnerabilityType} />
              </InfoField>
            </Row>
            <Row>
              <LabelField>
                <Label>{t("searchFindings.tabDescription.zeroRisk")}</Label>
              </LabelField>
              <div className={"pl1 pr0 w-70-l w-100-m w-100-ns mr"}>
                {_.isEmpty(vulnerability.zeroRisk) ? (
                  <Value value={vulnerability.zeroRisk ?? ""} />
                ) : (
                  <div className={"tr-l tl-m tl-ns"}>
                    <p className={"dib f5 ma0 mid-gray pr1-l"}>
                      <PointStatus status={vulnerability.zeroRisk as string} />
                    </p>
                  </div>
                )}
              </div>
            </Row>
            {canRetrieveHacker ? (
              <Row>
                <LabelField>
                  <Label>{t("searchFindings.tabDescription.hacker")}</Label>
                </LabelField>
                <InfoField>
                  <Value value={data.vulnerability.hacker} />
                </InfoField>
              </Row>
            ) : undefined}
          </Col50>
        </OuterRow>
      </div>
    </React.StrictMode>
  );
};

export { AdditionalInfo };
