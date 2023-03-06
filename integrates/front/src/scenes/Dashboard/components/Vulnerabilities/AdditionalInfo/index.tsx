import { useMutation, useQuery } from "@apollo/client";
import type { ApolloError } from "@apollo/client";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import _ from "lodash";
import React, { Fragment, useCallback, useMemo, useState } from "react";
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

import { Input } from "components/Input/Fields/Input";
import { Select } from "components/Input/Fields/Select";
import { Col, Row } from "components/Layout";
import { GET_VULN_ADDITIONAL_INFO } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/queries";
import type { IGetVulnAdditionalInfoAttr } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/types";
import { Value } from "scenes/Dashboard/components/Vulnerabilities/AdditionalInfo/value";
import { Status } from "scenes/Dashboard/components/Vulnerabilities/Formatter/index";
import type { IErrorInfoAttr } from "scenes/Dashboard/components/Vulnerabilities/uploadFile";
import { formatTreatment } from "scenes/Dashboard/components/Vulnerabilities/utils";
import { Logger } from "utils/logger";
import { msgError, msgSuccess } from "utils/notifications";
import { regExps } from "utils/validations";

function commitFormatter(value: string): string {
  const COMMIT_LENGTH: number = 7;

  return value.slice(0, COMMIT_LENGTH);
}

const AdditionalInfo: React.FC<IAdditionalInfoProps> = ({
  canRetrieveHacker,
  canSeeSource,
  refetchData,
  vulnerability,
}: IAdditionalInfoProps): JSX.Element => {
  const { t } = useTranslation();

  const formatError = useCallback(
    (errorName: string, errorValue: string): string =>
      ` ${t(errorName)} "${errorValue}" ${t("groupAlerts.invalid")}. `,
    [t]
  );

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
          refetchData();
        }
      },
      onError: (error: ApolloError): void => {
        error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
          if (message.includes("Exception - Error in path value")) {
            const errorObject: IErrorInfoAttr = JSON.parse(message);
            msgError(`${t("groupAlerts.portValue")}
            ${formatError("groupAlerts.value", errorObject.values)}`);
          } else if (message === "Invalid, vulnerability already exists") {
            msgError(t("validations.vulnerabilityAlreadyExists"));
          } else if (message === "Exception - Unsanitized input found") {
            msgError(t("validations.unsanitizedInputFound"));
          } else if (
            message.includes(
              "Exception - The vulnerability path does not exist in the toe lines"
            )
          ) {
            msgError(
              t(
                "searchFindings.tabVuln.alerts.uploadFile.linesPathDoesNotExist",
                {
                  path: t("searchFindings.tabVuln.vulnTable.location"),
                }
              )
            );
          } else if (
            message.includes(
              "Exception -  The vulnerability URL and field do not exist in the toe inputs"
            )
          ) {
            msgError(
              t(
                "searchFindings.tabVuln.alerts.uploadFile.inputUrlAndFieldDoNotExist",
                {
                  path: t("searchFindings.tabVuln.vulnTable.location"),
                }
              )
            );
          } else if (
            message.includes(
              "Exception -  The line does not exist in the range of 0 and lines of code"
            )
          ) {
            const destructMsg: { msg: string; path: string } =
              JSON.parse(message);
            msgError(
              t(
                "searchFindings.tabVuln.alerts.uploadFile.lineDoesNotExistInLoc",
                {
                  line: destructMsg.msg.split("code: ")[1],
                  path: t("searchFindings.tabVuln.vulnTable.location"),
                }
              )
            );
          } else {
            msgError(t("groupAlerts.errorTextsad"));
            Logger.warning(
              "An error occurred updating the vulnerability description",
              error
            );
          }
        });
      },
      refetchQueries: [
        {
          query: GET_VULN_ADDITIONAL_INFO,
          variables: {
            canRetrieveHacker,
            vulnId: vulnerability.id,
          },
        },
      ],
    }
  );

  const treatmentLabel = useMemo((): string => {
    if (data === undefined) {
      return "";
    }

    return formatTreatment(
      data.vulnerability.treatmentStatus,
      vulnerability.state,
      data.vulnerability.treatmentAcceptanceStatus
    );
  }, [data, vulnerability]);

  // Handle action
  const toggleEdit = useCallback((): void => {
    setIsEditing((currentValue: boolean): boolean => !currentValue);
  }, []);

  const onSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      await updateVulnerabilityDescription({
        variables: {
          commit: values.type === "lines" ? values.commitHash : undefined,
          source: values.source === "ASM" ? undefined : values.source,
          vulnerabilityId: vulnerability.id,
        },
      });
    },
    [vulnerability, updateVulnerabilityDescription]
  );

  const isVulnOpen: boolean = vulnerability.state === "VULNERABLE";
  const vulnerabilityType = useMemo((): string => {
    if (data === undefined) {
      return t("searchFindings.tabVuln.vulnTable.vulnerabilityType.inputs");
    }

    return t(
      `searchFindings.tabVuln.vulnTable.vulnerabilityType.${data.vulnerability.vulnerabilityType}`
    );
  }, [t, data]);

  const currentExpiration: string =
    isVulnOpen &&
    data?.vulnerability.treatmentStatus === "ACCEPTED" &&
    !_.isNull(data.vulnerability.treatmentAcceptanceDate)
      ? data.vulnerability.treatmentAcceptanceDate.split(" ")[0]
      : "";

  const currentJustification: string =
    !isVulnOpen ||
    _.isUndefined(vulnerability.treatmentJustification) ||
    _.isNull(vulnerability.treatmentJustification)
      ? ""
      : vulnerability.treatmentJustification;
  const currentAssigned: string = isVulnOpen
    ? (vulnerability.treatmentAssigned as string)
    : "";
  const treatmentDate: string = isVulnOpen
    ? vulnerability.lastTreatmentDate.split(" ")[0]
    : "";

  const treatmentChanges = parseInt(
    data?.vulnerability.treatmentChanges ?? "0",
    10
  );

  return (
    <React.StrictMode>
      <Formik
        enableReinitialize={true}
        initialValues={{
          commitHash: data?.vulnerability.commitHash ?? "",
          source: data?.vulnerability.source.toUpperCase() ?? "",
          type: data?.vulnerability.vulnerabilityType ?? "",
        }}
        name={"editVulnerability"}
        onSubmit={onSubmit}
        validationSchema={object().shape({
          commitHash: string().when("type", {
            is: "lines",
            otherwise: string().nullable(),
            then: string()
              .required(t("validations.required"))
              .matches(regExps.commitHash, t("validations.commitHash"))
              .nullable(),
          }),
          source: string().required(t("validations.required")),
        })}
      >
        {({ dirty, submitForm, values }): React.ReactNode => {
          return (
            <Fragment>
              <ActionButtons
                isEditing={isEditing}
                isPristine={!dirty}
                onEdit={toggleEdit}
                onUpdate={submitForm}
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
                      {_.isEmpty(vulnerability.stream) ? undefined : (
                        <Detail
                          editableField={undefined}
                          field={vulnerability.stream}
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
                            value={vulnerability.reportDate.split(" ")[0]}
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
                              _.isNull(data?.vulnerability.closingDate) ||
                              vulnerability.state !== "SAFE"
                                ? ""
                                : data?.vulnerability.closingDate.split(" ")[0]
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
                          field={<Value value={data?.vulnerability.source} />}
                          isEditing={isEditing}
                          label={t("searchFindings.tabVuln.vulnTable.source")}
                        />
                      ) : undefined}
                      {(_.isEmpty(values.commitHash) && !isEditing) ||
                      data?.vulnerability.vulnerabilityType !==
                        "lines" ? undefined : (
                        <Detail
                          editableField={<Input name={"commitHash"} />}
                          field={
                            <Value
                              value={
                                _.isNull(data.vulnerability.commitHash)
                                  ? undefined
                                  : commitFormatter(
                                      data.vulnerability.commitHash
                                    )
                              }
                            />
                          }
                          isEditing={isEditing}
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
                              vulnerability.severity === null ||
                              vulnerability.severity === "-1"
                                ? ""
                                : vulnerability.severity
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
                          field={<Value value={data?.vulnerability.hacker} />}
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
                              data?.vulnerability.lastRequestedReattackDate?.split(
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
                            value={data?.vulnerability.lastReattackRequester}
                          />
                        }
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.requester")}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={data?.vulnerability.cycles} />}
                        isEditing={false}
                        label={t("searchFindings.tabVuln.vulnTable.cycles")}
                      />
                      <Detail
                        editableField={undefined}
                        field={<Value value={data?.vulnerability.efficacy} />}
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
                        field={<Value value={treatmentLabel} />}
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
