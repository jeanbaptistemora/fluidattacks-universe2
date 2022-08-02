import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import _ from "lodash";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Card } from "components/Card";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";
import { Tooltip } from "components/Tooltip";
import type { IPolicies } from "scenes/Dashboard/containers/PoliciesView/types";
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
}: IPolicies): JSX.Element => {
  const { t } = useTranslation();
  const minSeverity: number = 0.0;
  const maxSeverity: number = 10.0;
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{
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
          <Text fw={7} mb={3} mt={4} size={5}>
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
                <Text mb={2}>
                  {t(`${translationStart}policies.maxAcceptanceDays`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"maxAcceptanceDays"}
                    tip={t(`${translationStart}recommended.maxAcceptanceDays`)}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.maxAcceptanceDays.tooltip`}
                  place={"top"}
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
                <Text mb={2}>
                  {t(`${translationStart}policies.maxNumberAcceptances`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"maxNumberAcceptances"}
                    tip={t(
                      `${translationStart}recommended.maxNumberAcceptances`
                    )}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.maxNumberAcceptances.tooltip`}
                  place={"top"}
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
                <Text mb={2}>
                  {t(`${translationStart}policies.vulnerabilityGracePeriod`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"vulnerabilityGracePeriod"}
                    tip={t(
                      `${translationStart}recommended.vulnerabilityGracePeriod`
                    )}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.vulnerabilityGracePeriod.tooltip`}
                  place={"top"}
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
                <Text mb={2}>
                  {t(`${translationStart}policies.minAcceptanceSeverity`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"maxAcceptanceDays"}
                    tip={t(`${translationStart}recommended.maxAcceptanceDays`)}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.minAcceptanceSeverity.tooltip`}
                  place={"top"}
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
                <Text mb={2}>
                  {t(`${translationStart}policies.maxAcceptanceSeverity`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"maxAcceptanceDays"}
                    tip={t(`${translationStart}recommended.maxAcceptanceDays`)}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.maxAcceptanceSeverity.tooltip`}
                  place={"top"}
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
                <Text mb={2}>
                  {t(`${translationStart}policies.minBreakingSeverity`)}
                  &nbsp;
                  <Tooltip
                    disp={"inline"}
                    id={"minBreakingSeverity"}
                    tip={t(
                      `${translationStart}recommended.minBreakingSeverity`
                    )}
                  >
                    <Button disabled={true} size={"sm"}>
                      <FontAwesomeIcon color={"#5c5c70"} icon={faCircleInfo} />
                    </Button>
                  </Tooltip>
                </Text>
                <Tooltip
                  id={`${translationStart}recommended.minBreakingSeverity.tooltip`}
                  place={"top"}
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
