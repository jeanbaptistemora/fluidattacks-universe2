/* eslint-disable react/forbid-component-props */
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faExternalLinkAlt } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Label } from "components/Input";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import styles from "scenes/Dashboard/containers/Organization-Content/PoliciesView/index.css";
import type { IPolicies } from "scenes/Dashboard/containers/Organization-Content/PoliciesView/types";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";
import { FormikText } from "utils/forms/fields";
import {
  composeValidators,
  isFloatOrInteger,
  isZeroOrPositive,
  numberBetween,
  numeric,
} from "utils/validations";

const translationStart = "organization.tabs.policies.";
const policiesUrl =
  "https://docs.fluidattacks.com/machine/web/organization/policies";

const Policies: React.FC<IPolicies> = ({
  handleSubmit,
  loadingPolicies,
  maxAcceptanceDays,
  maxAcceptanceSeverity,
  maxNumberAcceptances,
  minAcceptanceSeverity,
  minBreakingSeverity,
  permission,
  vulnerabilityGracePeriod,
  savingPolicies,
  tooltipMessage = undefined,
  inactivityPeriod = undefined,
}: IPolicies): JSX.Element => {
  const { t } = useTranslation();
  const minInactivityPeriod: number = 21;
  const maxInactivityPeriod: number = 999;
  const minSeverity: number = 0.0;
  const maxSeverity: number = 10.0;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{
        inactivityPeriod: _.isNil(inactivityPeriod)
          ? ""
          : inactivityPeriod.toString(),
        maxAcceptanceDays: _.isNull(maxAcceptanceDays)
          ? ""
          : maxAcceptanceDays.toString(),
        maxAcceptanceSeverity: parseFloat(maxAcceptanceSeverity)
          .toFixed(1)
          .toString(),
        maxNumberAcceptances: _.isNull(maxNumberAcceptances)
          ? ""
          : maxNumberAcceptances.toString(),
        minAcceptanceSeverity: parseFloat(minAcceptanceSeverity)
          .toFixed(1)
          .toString(),
        minBreakingSeverity: _.isNull(minBreakingSeverity)
          ? "0.0"
          : parseFloat(minBreakingSeverity).toFixed(1).toString(),
        vulnerabilityGracePeriod: _.isNull(vulnerabilityGracePeriod)
          ? ""
          : vulnerabilityGracePeriod.toString(),
      }}
      name={"policies"}
      onSubmit={handleSubmit}
    >
      {({ dirty, isSubmitting }): JSX.Element => (
        <Form id={"policies"}>
          <Text fw={7} mb={3} mt={4} size={"big"}>
            {tooltipMessage === undefined ? (
              <React.StrictMode>
                {t(`${translationStart}title`)}
              </React.StrictMode>
            ) : (
              <Tooltip
                disp={"inline-block"}
                id={"policies.tooltip.id"}
                tip={tooltipMessage}
              >
                {t(`${translationStart}title`)}
              </Tooltip>
            )}
          </Text>
          <Row>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"maxAcceptanceDays"}>
                  {t(`${translationStart}policies.maxAcceptanceDays`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#maximum-number-of-calendar-days-a-finding-can-be-temporarily-accepted`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxAcceptanceDays-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"maxAcceptanceDays-tooltip"}
                  place={"bottom"}
                  tip={t(`${translationStart}recommended.maxAcceptanceDays`)}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"maxAcceptanceDays"}
                    type={"text"}
                    validate={composeValidators([isZeroOrPositive, numeric])}
                  />
                </Tooltip>
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"maxNumberAcceptances"}>
                  {t(`${translationStart}policies.maxNumberAcceptances`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#maximum-number-of-times-a-finding-can-be-accepted`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxNumberAcceptances-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"maxNumberAcceptances-tooltip"}
                  place={"bottom"}
                  tip={t(`${translationStart}recommended.maxNumberAcceptances`)}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"maxNumberAcceptances"}
                    type={"text"}
                    validate={composeValidators([isZeroOrPositive, numeric])}
                  />
                </Tooltip>
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"vulnerabilityGracePeriod"}>
                  {t(`${translationStart}policies.vulnerabilityGracePeriod`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#grace-period-where-newly-reported-vulnerabilities-wont-break-the-build`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"vulnerabilityGracePeriod-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"vulnerabilityGracePeriod-tooltip"}
                  place={"bottom"}
                  tip={t(
                    `${translationStart}recommended.vulnerabilityGracePeriod`
                  )}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"vulnerabilityGracePeriod"}
                    type={"text"}
                    validate={composeValidators([isZeroOrPositive, numeric])}
                  />
                </Tooltip>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"minAcceptanceSeverity"}>
                  {t(`${translationStart}policies.minAcceptanceSeverity`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#temporal-acceptance-minimum-cvss-31-score-allowed-for-assignment`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"minAcceptanceSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"minAcceptanceSeverity-tooltip"}
                  place={"bottom"}
                  tip={t(
                    `${translationStart}recommended.minAcceptanceSeverity`
                  )}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"minAcceptanceSeverity"}
                    type={"text"}
                    validate={composeValidators([
                      isFloatOrInteger,
                      numberBetween(minSeverity, maxSeverity),
                    ])}
                  />
                </Tooltip>
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"maxAcceptanceSeverity"}>
                  {t(`${translationStart}policies.maxAcceptanceSeverity`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#temporal-acceptance-maximum-cvss-31-score-allowed-for-assignment`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"maxAcceptanceSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"maxAcceptanceSeverity-tooltip"}
                  place={"bottom"}
                  tip={t(
                    `${translationStart}recommended.maxAcceptanceSeverity`
                  )}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"maxAcceptanceSeverity"}
                    type={"text"}
                    validate={composeValidators([
                      isFloatOrInteger,
                      numberBetween(minSeverity, maxSeverity),
                    ])}
                  />
                </Tooltip>
              </Card>
            </Col>
            <Col lg={33} md={50} sm={100}>
              <Card>
                <Label htmlFor={"minBreakingSeverity"}>
                  {t(`${translationStart}policies.minBreakingSeverity`)}
                  <ExternalLink
                    className={`${styles["link-to-policies-docs"]} f7`}
                    href={`${policiesUrl}#minimum-cvss-31-score-of-an-open-vulnerability-for-devsecops`}
                  >
                    <Tooltip
                      disp={"inline-block"}
                      id={"minBreakingSeverity-tooltip"}
                      place={"bottom"}
                      tip={t(`${translationStart}externalTooltip`)}
                    >
                      <FontAwesomeIcon icon={faExternalLinkAlt} />
                    </Tooltip>
                  </ExternalLink>
                </Label>
                <Tooltip
                  disp={"inline"}
                  id={"minBreakingSeverity-tooltip"}
                  place={"bottom"}
                  tip={t(`${translationStart}recommended.minBreakingSeverity`)}
                >
                  <Field
                    component={FormikText}
                    disabled={permissions.cannot(permission)}
                    name={"minBreakingSeverity"}
                    type={"text"}
                    validate={composeValidators([
                      isFloatOrInteger,
                      numberBetween(minSeverity, maxSeverity),
                    ])}
                  />
                </Tooltip>
              </Card>
            </Col>
          </Row>
          {_.isNil(inactivityPeriod) ? undefined : (
            <Row>
              <Col lg={33} md={50} sm={100}>
                <Card>
                  <Label htmlFor={"inactivityPeriod"}>
                    {t(`${translationStart}policies.inactivityPeriod`)}
                  </Label>
                  <Tooltip
                    disp={"inline"}
                    id={"inactivityPeriod-tooltip"}
                    place={"bottom"}
                    tip={t(`${translationStart}recommended.inactivityPeriod`)}
                  >
                    <Field
                      component={FormikText}
                      disabled={permissions.cannot(permission)}
                      name={"inactivityPeriod"}
                      type={"text"}
                      validate={composeValidators([
                        numeric,
                        numberBetween(minInactivityPeriod, maxInactivityPeriod),
                      ])}
                    />
                  </Tooltip>
                </Card>
              </Col>
            </Row>
          )}
          <div className={"mt2"} />
          <Can do={permission}>
            {!dirty ||
            loadingPolicies ||
            isSubmitting ||
            savingPolicies ? undefined : (
              <Button type={"submit"} variant={"secondary"}>
                {t(`${translationStart}save`)}
              </Button>
            )}
          </Can>
        </Form>
      )}
    </Formik>
  );
};

export { Policies };
