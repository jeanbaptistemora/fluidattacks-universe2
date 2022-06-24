import { Form, useFormikContext } from "formik";
import React from "react";

import { BePresentField } from "./BePresentField";
import { HasRecentAttack } from "./HasRecentAttackField";
import type { IFormValues, IHandleEditionModalFormProps } from "./types";

import { ModalConfirm } from "components/Modal";
import { Col50, Row } from "styles/styledComponents";

const HandleEditionModalForm: React.FC<IHandleEditionModalFormProps> = (
  props: IHandleEditionModalFormProps
): JSX.Element => {
  const { handleCloseModal } = props;

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
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleEditionModalForm };
