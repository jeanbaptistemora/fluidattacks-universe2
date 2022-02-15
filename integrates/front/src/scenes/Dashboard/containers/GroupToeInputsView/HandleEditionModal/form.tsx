import { Form, useFormikContext } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { BePresentField } from "./BePresentField";
import { HasRecentAttack } from "./HasRecentAttackField";
import type { IFormValues, IHandleEditionModalFormProps } from "./types";

import { Button } from "components/Button";
import { ButtonToolbar, Col100, Col50, Row } from "styles/styledComponents";

const HandleEditionModalForm: React.FC<IHandleEditionModalFormProps> = (
  props: IHandleEditionModalFormProps
): JSX.Element => {
  const { handleCloseModal } = props;

  const { t } = useTranslation();

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"updateToeInput"}>
      <Row>
        <Col50>
          <BePresentField />
        </Col50>
        <Col50>
          <HasRecentAttack />
        </Col50>
      </Row>
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button onClick={handleCloseModal}>
              {t("group.toe.inputs.editModal.close")}
            </Button>
            <Button disabled={false} onClick={submitForm}>
              {t("group.toe.inputs.editModal.procced")}
            </Button>
          </ButtonToolbar>
        </Col100>
      </Row>
    </Form>
  );
};

export { HandleEditionModalForm };
