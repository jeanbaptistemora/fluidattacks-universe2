/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import { ActionButtons } from "./ActionButtons";
import { Detail } from "./detail";
import { UPDATE_VULNERABILITY_DESCRIPTION } from "./queries";
import type {
  IAdditionalInfoProps,
  IFormValues,
  IUpdateVulnerabilityDescriptionAttr,
} from "./types";

import { Select } from "components/Input/Fields/Select";
import { Col, Row } from "components/Layout";
import { GET_VULN_ADDITIONAL_INFO } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import type { IGetVulnAdditionalInfoAttr } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/types";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { Status } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";

function commitFormatter(value: string): string {
  const COMMIT_LENGTH: number = 7;

  return value.slice(0, COMMIT_LENGTH);
}

const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canRetrieveHacker,
  canSeeSource,
  vulnerability,
}: IAdditionalInfoProps): JSX.Element => {
  const { t } = useTranslation();

  // State
  const [isEditing, setIsEditing] = useState(false);

  // Graphql queries
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
        vulnId: vulnerability.id,
      },
    }
  );

  // Graphql mutations
  const [updateVulnerabilityDescription] = useMutation(
    UPDATE_VULNERABILITY_DESCRIPTION,
    {
      onCompleted: (mtResult: IUpdateVulnerabilityDescriptionAttr): void => {
        if (mtResult.updateVulnerabilityDescription.success) {
          msgSuccess(
            t("searchFindings.tabVuln.additionalInfo.alerts.updatedDetails"),
            t("groupAlerts.updatedTitle")
          );
          setIsEditing(false);
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach((): void => {
          msgError(t("groupAlerts.errorTextsad"));
          Logger.warning(
            "An error occurred updating the vulnerability description",
            error
          );
        });
      },
      refetchQueries: [GET_VULN_ADDITIONAL_INFO],
    }
  );

  // Get information
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

  // Handle action
  function toggleEdit(): void {
    setIsEditing(!isEditing);
  }
  function onSubmit(values: IFormValues): void {
    void updateVulnerabilityDescription({
      variables: {
        source: values.source,
        vulnerabilityId: vulnerability.id,
      },
    });
  }

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          source: data.vulnerability.source.toUpperCase(),
        }}
        name={"editvulnerability"}
        onSubmit={onSubmit}
        validationSchema={object().shape({
          source: string().required(),
        })}
      >
        {({ dirty, submitForm }): React.ReactNode => {
          function onUpdate(): void {
            void submitForm();
          }

          return (
            <Fragment>
              <ActionButtons
                isEditing={isEditing}
                isPristine={!dirty}
                onEdit={toggleEdit}
                onUpdate={onUpdate}
              />
              <Row>
                <Col lg={50} md={50} sm={50}>
                  <Row>
                    <Col>
                      <h4>{t("searchFindings.tabVuln.vulnTable.location")}</h4>
                      <Detail
                        editableField={undefined}
                        field={_.unescape(vulnerability.where)}
                        isEditing={false}
                        label={undefined}
                      />
                      {_.isEmpty(data.vulnerability.stream) ? undefined : (
                        <Detail
                          editableField={undefined}
                          field={data.vulnerability.stream}
                          isEditing={false}
                          label={undefined}
                        />
                      )}
                      <Detail
                        editableField={undefined}
                        field={<Value value={vulnerability.specific} />}
                        isEditing={false}
                        label={t(
                          `searchFindings.tabVuln.vulnTable.specificType.${vulnerabilityType}`
                        )}
                      />
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <h4>{t("searchFindings.tabVuln.vulnTable.info")}</h4>
                      <Detail
                        editableField={undefined}
                        field={
                          <Value
                            value={data.vulnerability.reportDate.split(" ")[0]}
                          />
                        }
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.reportDate")}
                      />
                      <Detail
                        editableField={undefined}
                        field={
                          <Value
                            value={
                              _.isNull(data.vulnerability.closingDate)
                                ? ""
                                : data.vulnerability.closingDate.split(" ")[0]
                            }
                          />
                        }
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.closingDate"
                        )}
                      />
                      {canSeeSource ? (
                        <Detail
                          editableField={
                            <Select id={"source"} name={"source"}>
                              <option value={""} />
                              <option value={"ANALYST"}>
                                {t(
                                  `searchFindings.tabVuln.vulnTable.vulnerabilitySource.ANALYST`
                                )}
                              </option>
                              <option value={"CUSTOMER"}>
                                {t(
                                  `searchFindings.tabVuln.vulnTable.vulnerabilitySource.CUSTOMER`
                                )}
                              </option>
                              <option value={"DETERMINISTIC"}>
                                {t(
                                  `searchFindings.tabVuln.vulnTable.vulnerabilitySource.DETERMINISTIC`
                                )}
                              </option>
                              <option value={"ESCAPE"}>
                                {t(
                                  `searchFindings.tabVuln.vulnTable.vulnerabilitySource.ESCAPE`
                                )}
                              </option>
                              <option value={"MACHINE"}>
                                {t(
                                  `searchFindings.tabVuln.vulnTable.vulnerabilitySource.MACHINE`
                                )}
                              </option>
                            </Select>
                          }
                          field={<Value value={data.vulnerability.source} />}
                          isEditing={isEditing}
                          label={t("searchFindings.tabVuln.vulnTable.source")}
                        />
                      ) : undefined}
                      {_.isEmpty(data.vulnerability.commitHash) ? undefined : (
                        <Detail
                          editableField={undefined}
                          field={
                            <Value
                              value={commitFormatter(
                                data.vulnerability.commitHash as string
                              )}
                            />
                          }
                          isEditing={false}
                          label={t("searchFindings.tabVuln.commitHash")}
                        />
                      )}
                      <Detail
                        editableField={undefined}
                        field={<Value value={vulnerability.tag} />}
                        isEditing={false}
                        label={t("searchFindings.tabDescription.tag")}
                      />
                      <Detail
                        editableField={undefined}
                        field={
                          <Value
                            value={
                              data.vulnerability.severity === null ||
                              data.vulnerability.severity === "-1"
                                ? ""
                                : data.vulnerability.severity
                            }
                          />
                        }
                        isEditing={false}
                        label={t(
                          "searchFindings.tabDescription.businessCriticality"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={vulnerabilityType} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.vulnerabilityType.title"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={
                          _.isEmpty(vulnerability.zeroRisk) ? (
                            <Value value={undefined} />
                          ) : (
                            <Status status={vulnerability.zeroRisk as string} />
                          )
                        }
                        isEditing={false}
                        label={t("searchFindings.tabDescription.zeroRisk")}
                      />
                      {canRetrieveHacker ? (
                        <Detail
                          editableField={undefined}
                          field={<Value value={data.vulnerability.hacker} />}
                          isEditing={false}
                          label={t("searchFindings.tabDescription.hacker")}
                        />
                      ) : undefined}
                    </Col>
                  </Row>
                  <Row>
                    <Col>
                      <h4>{t("searchFindings.tabVuln.vulnTable.reattacks")}</h4>
                      <Detail
                        editableField={undefined}
                        field={
                          <Value
                            value={
                              data.vulnerability.lastRequestedReattackDate?.split(
                                " "
                              )[0] ?? ""
                            }
                          />
                        }
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.lastRequestedReattackDate"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={
                          <Value
                            value={data.vulnerability.lastReattackRequester}
                          />
                        }
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.requester")}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={data.vulnerability.cycles} />}
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.cycles")}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={data.vulnerability.efficacy} />}
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.efficacy")}
                      />
                    </Col>
                  </Row>
                </Col>
                <Col lg={50} md={50} sm={50}>
                  <Row>
                    <Col>
                      <h4>
                        {t("searchFindings.tabVuln.vulnTable.treatments")}
                      </h4>
                      <Detail
                        editableField={undefined}
                        field={<Value value={vulnerability.treatment} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.currentTreatment"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={currentAssigned} />}
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.assigned")}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={treatmentDate} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.treatmentDate"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={currentExpiration} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.treatmentExpiration"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={currentJustification} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.treatmentJustification"
                        )}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={treatmentChanges} />}
                        isEditing={false}
                        label={t(
                          "searchFindings.tabVuln.vulnTable.treatmentChanges"
                        )}
                      />
                    </Col>
                  </Row>
                </Col>
              </Row>
            </Fragment>
          );
        }}
      </Formik>
    </React.StrictMode>
  );
};

export { AdditionalInfo };
