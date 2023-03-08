/* eslint @typescript-eslint/no-unnecessary-condition:0 */
import { faFileExcel, faMinus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Form, Formik } from "formik";
import _ from "lodash";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";
import type { TestContext } from "yup";
import { array, date, number, object } from "yup";

import { Button } from "components/Button";
import {
  Checkbox,
  Input,
  InputDate,
  InputNumber,
  Select,
} from "components/Input";
import { Col, Hr, Row } from "components/Layout";
import type { IVerifyFn } from "scenes/Dashboard/components/VerifyDialog/types";
import {
  composeValidators,
  isGreaterDate,
  maxLength,
  validTextField,
} from "utils/validations";

interface IFilterFormProps {
  requestGroupReport: (
    age: number | undefined,
    closingDate: string | undefined,
    findingTitle: string | undefined,
    lastReport: number | undefined,
    location: string | undefined,
    maxReleaseDate: string | undefined,
    maxSeverity: number | undefined,
    minReleaseDate: string | undefined,
    minSeverity: number | undefined,
    states: string[],
    treatments: string[] | undefined,
    verifications: string[],
    verificationCode: string
  ) => void;
  setIsVerifyDialogOpen: React.Dispatch<React.SetStateAction<boolean>>;
  setVerifyCallbacks: IVerifyFn;
  typesOptions: string[];
}

interface IFormValues {
  age: number | undefined;
  closingDate: string;
  findingTitle: string;
  lastReport: number | undefined;
  location: string;
  maxReleaseDate: string;
  maxSeverity: number | undefined;
  minReleaseDate: string;
  minSeverity: number | undefined;
  states: string[];
  treatments: string[];
  verifications: string[];
}

const MAX_LENGTH: number = 100;
const maxLocationLength: ConfigurableValidator = maxLength(MAX_LENGTH);

export const FilterForm: React.FC<IFilterFormProps> = ({
  requestGroupReport,
  setIsVerifyDialogOpen,
  setVerifyCallbacks,
  typesOptions,
}: IFilterFormProps): JSX.Element => {
  const { t } = useTranslation();

  const validations = object().shape({
    maxReleaseDate: date()
      .max(new Date(), t("validations.greaterDate"))
      .test({
        exclusive: false,
        message: "Must be greater than or equal to Min release date",
        name: "min",
        params: {},
        test: (value: Date | undefined, thisContext: TestContext): boolean => {
          const { minReleaseDate } = thisContext.parent;

          return value === undefined || minReleaseDate === undefined
            ? true
            : value >= minReleaseDate;
        },
      }),
    maxSeverity: number()
      .max(10)
      .test({
        exclusive: false,
        message: "Must be greater than or equal to Min severity",
        name: "min",
        params: {},
        test: (
          value: number | undefined,
          thisContext: TestContext
        ): boolean => {
          const { minSeverity } = thisContext.parent;

          return value === undefined || minSeverity === undefined
            ? true
            : value >= (minSeverity ?? 0);
        },
      }),
    minReleaseDate: date()
      .max(new Date(), t("validations.greaterDate"))
      .test({
        exclusive: false,
        message: "Must be less than or equal to Max release date",
        name: "max",
        params: {},
        test: (value: Date | undefined, thisContext: TestContext): boolean => {
          const { maxReleaseDate } = thisContext.parent;

          return value === undefined || maxReleaseDate === undefined
            ? true
            : value <= maxReleaseDate;
        },
      }),
    minSeverity: number()
      .min(0)
      .test({
        exclusive: false,
        message: "Must be less than or equal to Max severity",
        name: "max",
        params: {},
        test: (
          value: number | undefined,
          thisContext: TestContext
        ): boolean => {
          const { maxSeverity } = thisContext.parent;

          return value === undefined || maxSeverity === undefined
            ? true
            : value <= (maxSeverity ?? 10);
        },
      }),
    states: array().min(1, t("validations.someRequired")),
    treatments: array().when("closingDate", {
      is: (closingDate: string): boolean => _.isEmpty(closingDate),
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
  });

  const findingTitle = (values: IFormValues): string | undefined =>
    _.isEmpty(values.findingTitle) ? undefined : values.findingTitle;

  const lastReport = (values: IFormValues): number | undefined =>
    values.lastReport === null || _.isEmpty(String(values.lastReport))
      ? undefined
      : Number(values.lastReport);

  const getMaxSeverity = (values: IFormValues): number | undefined =>
    _.isEmpty(String(values.maxSeverity)) || values.maxSeverity === null
      ? undefined
      : Number(values.maxSeverity);

  const getMinSeverity = (values: IFormValues): number | undefined =>
    values.minSeverity === null || _.isEmpty(String(values.minSeverity))
      ? undefined
      : Number(values.minSeverity);

  const getAge = (values: IFormValues): number | undefined =>
    values.age === null || _.isEmpty(String(values.age))
      ? undefined
      : values.age;

  const location = (values: IFormValues): string | undefined =>
    _.isEmpty(values.location) ? undefined : values.location;

  const onRequestReport = useCallback(
    (values: IFormValues): void => {
      setVerifyCallbacks(
        (verificationCode: string): void => {
          requestGroupReport(
            getAge(values),
            _.isEmpty(values.closingDate) ? undefined : values.closingDate,
            findingTitle(values),
            lastReport(values),
            location(values),
            _.isEmpty(values.maxReleaseDate)
              ? undefined
              : values.maxReleaseDate,
            getMaxSeverity(values),
            _.isEmpty(values.minReleaseDate)
              ? undefined
              : values.minReleaseDate,
            getMinSeverity(values),
            values.states,
            _.isEmpty(values.closingDate) ? values.treatments : undefined,
            values.verifications,
            verificationCode
          );
        },
        (): void => {
          setIsVerifyDialogOpen(false);
        }
      );
      setIsVerifyDialogOpen(true);
    },
    [requestGroupReport, setIsVerifyDialogOpen, setVerifyCallbacks]
  );

  return (
    <Formik
      initialValues={{
        age: undefined,
        closingDate: "",
        findingTitle: "",
        lastReport: undefined,
        location: "",
        maxReleaseDate: "",
        maxSeverity: undefined,
        minReleaseDate: "",
        minSeverity: undefined,
        states: [],
        treatments: [],
        verifications: [],
      }}
      name={"reportTreatments"}
      onSubmit={onRequestReport}
      validationSchema={validations}
    >
      {({ values }): JSX.Element => {
        return (
          <Form>
            <p className={"mb0"}>
              {t("group.findings.report.filterReportDescription")}
            </p>
            <Row align={"start"} justify={"start"}>
              <Col lg={50} md={50} sm={50}>
                <Select
                  label={t("group.findings.report.findingTitle.text")}
                  name={"findingTitle"}
                  tooltip={t("group.findings.report.findingTitle.tooltip")}
                >
                  <option value={""} />
                  {typesOptions.map(
                    (typeCode: string): JSX.Element => (
                      <option key={typeCode} value={typeCode}>
                        {typeCode}
                      </option>
                    )
                  )}
                </Select>
              </Col>
              <Col lg={50} md={50} sm={90}>
                <Row align={"start"} justify={"start"}>
                  <Col lg={45} md={45} sm={45}>
                    <Col lg={100} md={100} sm={100}>
                      <InputDate
                        label={t("group.findings.report.minReleaseDate.text")}
                        name={"minReleaseDate"}
                        tooltip={t(
                          "group.findings.report.minReleaseDate.tooltip"
                        )}
                      />
                    </Col>
                  </Col>
                  <Col lg={5} md={5} sm={5} />
                  <Col lg={45} md={45} sm={45}>
                    <Col lg={100} md={100} sm={100}>
                      <InputDate
                        label={t("group.findings.report.maxReleaseDate.text")}
                        name={"maxReleaseDate"}
                        tooltip={t(
                          "group.findings.report.maxReleaseDate.tooltip"
                        )}
                      />
                    </Col>
                  </Col>
                </Row>
              </Col>
              <Col lg={45} md={45} sm={50}>
                <Input
                  label={t("group.findings.report.location.text")}
                  name={"location"}
                  tooltip={t("group.findings.report.location.tooltip")}
                  type={"text"}
                  validate={composeValidators([
                    maxLocationLength,
                    validTextField,
                  ])}
                />
              </Col>
              <Col lg={15} md={15} sm={50}>
                <InputNumber
                  label={t("group.findings.report.lastReport.text")}
                  max={10000}
                  min={0}
                  name={"lastReport"}
                  tooltip={t("group.findings.report.lastReport.tooltip")}
                />
              </Col>
              <Col lg={25} md={25} sm={90}>
                <Row align={"start"} justify={"between"}>
                  <Col lg={45} md={45} sm={45}>
                    <InputNumber
                      decimalPlaces={1}
                      label={t("group.findings.report.minSeverity.text")}
                      max={10}
                      min={0}
                      name={"minSeverity"}
                      tooltip={t("group.findings.report.minSeverity.tooltip")}
                    />
                  </Col>
                  <Col lg={10} md={10} sm={50}>
                    <Row align={"center"} justify={"center"}>
                      <Col lg={100} md={100} sm={50}>
                        <FontAwesomeIcon
                          // eslint-disable-next-line react/forbid-component-props
                          className={"pt4"}
                          color={"gray"}
                          icon={faMinus}
                        />
                      </Col>
                    </Row>
                  </Col>
                  <Col lg={45} md={45} sm={45}>
                    <InputNumber
                      decimalPlaces={1}
                      label={t("group.findings.report.maxSeverity.text")}
                      max={10}
                      min={0}
                      name={"maxSeverity"}
                      tooltip={t("group.findings.report.maxSeverity.tooltip")}
                    />
                  </Col>
                </Row>
              </Col>
              <Col lg={15} md={15} sm={50}>
                <InputNumber
                  label={t("group.findings.report.age.text")}
                  max={10000}
                  min={0}
                  name={"age"}
                  tooltip={t("group.findings.report.age.tooltip")}
                />
              </Col>
              <Col lg={90} md={90} sm={90}>
                <Col lg={50} md={50} sm={50}>
                  <InputDate
                    label={t("group.findings.report.closingDate.text")}
                    name={"closingDate"}
                    tooltip={t("group.findings.report.closingDate.tooltip")}
                    validate={composeValidators([isGreaterDate])}
                  />
                </Col>
              </Col>
              {_.isEmpty(values.closingDate) ? (
                <Col lg={50} md={50} sm={50}>
                  <p className={"mb1 mt1"}>
                    <span className={"fw8"}>
                      {t("group.findings.report.treatment")}
                    </span>
                  </p>
                  {[
                    "ACCEPTED",
                    "ACCEPTED_UNDEFINED",
                    "IN_PROGRESS",
                    "UNTREATED",
                  ].map(
                    (treatment): JSX.Element => (
                      <Checkbox
                        disabled={!_.isEmpty(values.closingDate)}
                        key={treatment}
                        label={t(
                          `searchFindings.tabDescription.treatment.${_.camelCase(
                            treatment
                          )}`
                        )}
                        name={"treatments"}
                        value={treatment}
                      />
                    )
                  )}
                </Col>
              ) : undefined}
              <Col lg={30} md={30} sm={30}>
                <p className={"mb1 mt1"}>
                  <span className={"fw8"}>
                    {t("group.findings.report.reattack.title")}
                  </span>
                </p>
                {_.isEmpty(values.closingDate) ? (
                  <React.Fragment>
                    {["REQUESTED", "ON_HOLD", "VERIFIED"].map(
                      (verification): JSX.Element => (
                        <Checkbox
                          key={verification}
                          label={t(
                            `group.findings.report.reattack.${verification.toLowerCase()}`
                          )}
                          name={"verifications"}
                          value={verification}
                        />
                      )
                    )}
                  </React.Fragment>
                ) : (
                  <React.Fragment>
                    {["VERIFIED"].map(
                      (verification): JSX.Element => (
                        <Checkbox
                          key={verification}
                          label={t(
                            `group.findings.report.reattack.${verification.toLowerCase()}`
                          )}
                          name={"verifications"}
                          value={verification}
                        />
                      )
                    )}
                  </React.Fragment>
                )}
              </Col>
              <Col lg={20} md={20} sm={20}>
                <p className={"mb1 mt1"}>
                  <span className={"fw8"}>
                    {t("group.findings.report.state")}
                  </span>
                </p>
                {_.isEmpty(values.closingDate) ? (
                  <React.Fragment>
                    {["SAFE", "VULNERABLE"].map(
                      (state): JSX.Element => (
                        <Checkbox
                          key={state}
                          label={t(
                            `searchFindings.tabVuln.${state.toLowerCase()}`
                          )}
                          name={"states"}
                          value={state}
                        />
                      )
                    )}
                  </React.Fragment>
                ) : (
                  <React.Fragment>
                    {["SAFE"].map(
                      (state): JSX.Element => (
                        <Checkbox
                          key={state}
                          label={t(
                            `searchFindings.tabVuln.${state.toLowerCase()}`
                          )}
                          name={"states"}
                          value={state}
                        />
                      )
                    )}
                  </React.Fragment>
                )}
              </Col>
            </Row>
            <Hr />
            <Button id={"report-excel"} type={"submit"} variant={"primary"}>
              <FontAwesomeIcon icon={faFileExcel} />
              &nbsp;{t("group.findings.report.generateXls")}
            </Button>
          </Form>
        );
      }}
    </Formik>
  );
};
