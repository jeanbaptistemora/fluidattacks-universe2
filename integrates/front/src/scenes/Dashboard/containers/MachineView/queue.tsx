import { Field, Form, Formik } from "formik";
import React, { useState } from "react";

import type { IQueue } from "./types";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, FormGroup, Row } from "styles/styledComponents";
import { FormikCheckbox } from "utils/forms/fields";
import style from "utils/forms/index.css";
import { translate } from "utils/translations/translate";

const Queue: React.FC<IQueue> = (props: Readonly<IQueue>): JSX.Element => {
  const { rootNicknames, onClose, onSubmit } = props;

  const [isJobSubmitted, setJObSubmitted] = useState(false);

  function handleClose(): void {
    onClose();
  }
  async function handleSubmit(values: Record<string, unknown>): Promise<void> {
    setJObSubmitted(true);
    const nicknames = Object.keys(values);
    await onSubmit(nicknames);
    onClose();
  }

  return (
    <div>
      <p>{"Roots to execute"}</p>
      <Formik initialValues={{}} onSubmit={handleSubmit}>
        <Form>
          <div>
            <FormGroup>
              <ul className={style.suggestionList}>
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
              </ul>
              <Row>
                <Col100>
                  <ButtonToolbar>
                    <Button id={"cancel-job"} onClick={handleClose}>
                      {translate.t("confirmmodal.cancel")}
                    </Button>
                    <Button
                      disabled={isJobSubmitted}
                      id={"submit-job"}
                      type={"submit"}
                    >
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
