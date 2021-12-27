import { Field, Form, Formik } from "formik";
import React from "react";

import type { IQueue } from "./types";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, FormGroup, Row } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import { translate } from "utils/translations/translate";

const Queue: React.FC<IQueue> = (props: Readonly<IQueue>): JSX.Element => {
  const { rootNicknames, onClose, onSubmit } = props;

  async function handleSubmit(values: Record<string, unknown>): Promise<void> {
    const nicknames = Object.keys(values);
    await onSubmit(nicknames);
    onClose();
  }

  return (
    <div>
      <Formik initialValues={{}} onSubmit={handleSubmit}>
        <Form>
          <div>
            <p>{"Roots to execute"}</p>
            <FormGroup>
              {rootNicknames.map((root): JSX.Element => {
                return (
                  <Field
                    component={FormikCheckbox}
                    key={root}
                    label={root}
                    name={`root_nick_${root}`}
                    type={"checkbox"}
                    value={root}
                  />
                );
              })}
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"submit-job"} type={"submit"}>
                      {translate.t("confirmmodal.proceed")}
                    </Button>
                  </ButtonToolbar>
                </Col100>
              </Row>
            </FormGroup>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export { Queue };
