import { Form, useFormikContext } from "formik";
import React from "react";
import { useTranslation } from "react-i18next";

import { AttackedLinesField } from "./AttackedLinesField";
import { CommentsField } from "./CommentsField";
import type { IFormValues, IHandleEditionModalFormProps } from "./types";

import { Button } from "components/Button";
import { ModalFooter } from "components/Modal";
import { Col100, Col50, Row } from "styles/styledComponents";

const HandleEditionModalForm: React.FC<IHandleEditionModalFormProps> = (
  props: IHandleEditionModalFormProps
): JSX.Element => {
  const { selectedToeLinesDatas, handleCloseModal } = props;

  const { t } = useTranslation();

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
      <ModalFooter>
        <Button onClick={handleCloseModal} variant={"secondary"}>
          {t("group.toe.lines.editModal.close")}
        </Button>
        <Button onClick={submitForm} variant={"primary"}>
          {t("group.toe.lines.editModal.procced")}
        </Button>
      </ModalFooter>
    </Form>
  );
};

export { HandleEditionModalForm };
