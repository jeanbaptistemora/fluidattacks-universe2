import { Form, useFormikContext } from "formik";
import React from "react";

import { AttackedLinesField } from "./AttackedLinesField";
import { CommentsField } from "./CommentsField";
import type { IFormValues, IHandleEditionModalFormProps } from "./types";

import { ModalConfirm } from "components/Modal";
import { Col100, Col50, Row } from "styles/styledComponents";

const HandleEditionModalForm: React.FC<IHandleEditionModalFormProps> = (
  props: IHandleEditionModalFormProps
): JSX.Element => {
  const { selectedToeLinesDatas, handleCloseModal } = props;

  const { submitForm } = useFormikContext<IFormValues>();

  return (
    <Form id={"updateToeLinesAttackedLines"}>
      <Row>
        <Col50>
          <AttackedLinesField selectedToeLinesDatas={selectedToeLinesDatas} />
        </Col50>
      </Row>
      <Row>
        <Col100>
          <CommentsField />
        </Col100>
      </Row>
      <ModalConfirm onCancel={handleCloseModal} onConfirm={submitForm} />
    </Form>
  );
};

export { HandleEditionModalForm };
