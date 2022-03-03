import { Field, Form, Formik } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import type { IGitRootAttr } from "../../types";
import { Button } from "components/Button";
import {
  ButtonToolbar,
  Col100,
  ControlLabel,
  RequiredField,
  Row,
} from "styles/styledComponents";
import { FormikArrayField, FormikText } from "utils/forms/fields";

interface IEnvironmentsProps {
  initialValues: IGitRootAttr;
  onClose: () => void;
  onSubmit: (values: IGitRootAttr) => Promise<void>;
}

const Environments: React.FC<IEnvironmentsProps> = ({
  initialValues,
  onClose,
  onSubmit,
}: IEnvironmentsProps): JSX.Element => {
  const { t } = useTranslation();
  const validations = object().shape({
    environmentUrls: array().of(string().required(t("validations.required"))),
  });

  return (
    <Formik
      initialValues={initialValues}
      name={"gitEnvs"}
      onSubmit={onSubmit}
      validationSchema={validations}
    >
      {({ dirty, isSubmitting }): JSX.Element => (
        <Form>
          <React.Fragment>
            <ControlLabel>
              <RequiredField>{"*"}&nbsp;</RequiredField>
              {t("group.scope.git.envUrls")}
            </ControlLabel>
            <FormikArrayField
              allowEmpty={true}
              initialValue={""}
              name={"environmentUrls"}
            >
              {(fieldName: string): JSX.Element => (
                <Field component={FormikText} name={fieldName} type={"text"} />
              )}
            </FormikArrayField>
            <hr />
            <Row>
              <Col100>
                <ButtonToolbar>
                  <Button onClick={onClose} variant={"secondary"}>
                    {t("confirmmodal.cancel")}
                  </Button>
                  <Button
                    disabled={!dirty || isSubmitting}
                    id={"envs-manage-proceed"}
                    type={"submit"}
                    variant={"primary"}
                  >
                    {t("confirmmodal.proceed")}
                  </Button>
                </ButtonToolbar>
              </Col100>
            </Row>
          </React.Fragment>
        </Form>
      )}
    </Formik>
  );
};

export { Environments };
