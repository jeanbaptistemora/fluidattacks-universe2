import { faCircleInfo } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Field, Form, Formik } from "formik";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";
import { array, object, string } from "yup";

import { Button } from "components/Button";
import { Col, Row } from "components/Layout";
import { TooltipWrapper } from "components/TooltipWrapper";
import { FormikDropdown, FormikText } from "utils/forms/fields";

const AddRoot: React.FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { goBack } = useHistory();

  const handleSubmit = useCallback((): void => {
    localStorage.clear();
    sessionStorage.clear();
  }, []);

  const validations = object().shape({
    branch: string().required(),
    credentialName: string().required(),
    credentialType: string().required(),
    environment: string().required(),
    exclusions: array().of(string()).required(),
    url: string().required(),
  });

  return (
    <div>
      <Formik
        enableReinitialize={true}
        initialValues={{
          branch: "",
          credentialName: "",
          credentialType: "",
          environment: "",
          exclusions: "",
          url: "",
        }}
        name={"newRoot"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        <Form>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.url.label")}</strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"urlTooltip"}
                    message={t("autoenrollment.addRoot.url.tooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"url"}
                    placeholder={t("autoenrollment.addRoot.url.placeholder")}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.branch.label")}</strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"branch"}
                    placeholder={t("autoenrollment.addRoot.branch.placeholder")}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>{t("autoenrollment.addRoot.credentialType")}</strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field component={FormikDropdown} name={"credentialType"}>
                    <option value={""}>{""}</option>
                    <option value={"HTTPS"}>
                      {t("group.scope.git.repo.credentials.https")}
                    </option>
                    <option value={"SSH"}>
                      {t("group.scope.git.repo.credentials.ssh")}
                    </option>
                  </Field>
                </Col>
              </Row>
            </Col>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.credentialName.label")}
                  </strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"credentialName"}
                    placeholder={t(
                      "autoenrollment.addRoot.credentialName.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.environment.label")}
                  </strong>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"environment"}
                    placeholder={t(
                      "autoenrollment.addRoot.environment.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"flex-start"}>
            <Col large={"50"} medium={"50"} small={"50"}>
              <Row>
                <Col>
                  <strong>
                    {t("autoenrollment.addRoot.exclusions.label")}
                  </strong>
                </Col>
                <Col>
                  <TooltipWrapper
                    id={"urlTooltip"}
                    message={t("autoenrollment.addRoot.exclusions.tooltip")}
                    placement={"top"}
                  >
                    <FontAwesomeIcon icon={faCircleInfo} />
                  </TooltipWrapper>
                </Col>
              </Row>
              <Row>
                <Col>
                  <Field
                    component={FormikText}
                    name={"exclusions"}
                    placeholder={t(
                      "autoenrollment.addRoot.exclusions.placeholder"
                    )}
                    type={"text"}
                  />
                </Col>
              </Row>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button disabled={false} type={"submit"} variant={"primary"}>
                {t("autoenrollment.addRoot.proceed.checkAccess")}
              </Button>
            </Col>
          </Row>
          <Row justify={"center"}>
            <Col>
              <Button onClick={goBack} variant={"secondary"}>
                {t("confirmmodal.cancel")}
              </Button>
            </Col>
          </Row>
        </Form>
      </Formik>
    </div>
  );
};

export { AddRoot };
