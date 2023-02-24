import { Form, useFormikContext } from "formik";
import React from "react";

import { AttackedLinesField } from "./AttackedLinesField";
import { CommentsField } from "./CommentsField";
import type { IFormValues, IHandleEditionModalFormProps } from "./types";

import { Col, Row } from "components/Layout";
import { ModalConfirm } from "components/Modal";

const HandleEditionModalForm: React.FC<IHandleEditionModalFormProps> = (
  props: IHandleEditionModalFormProps
): JSX.Element => {
  const { selectedToeLinesDatas, handleCloseModal } = props;

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"updateToeLinesAttackedLines"}>
      <Row>
        <Col>
          <AttackedLinesField selectedToeLinesDatas={selectedToeLinesDatas} />
        </Col>
      </Row>
      <Row>
        <Col>
          <CommentsField />
        </Col>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleEditionModalForm };
