import React from "react";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import type { IEditGroupInformation } from "scenes/Dashboard/components/EditGroupInformationModal/types";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";
import { translate } from "utils/translations/translate";

const EditGroupInformationModal: React.FC<IEditGroupInformation> = (
  props: IEditGroupInformation
): JSX.Element => {
  const { isOpen, onClose } = props;
  const tempText: string = "This function will be available soon";

  return (
    <React.StrictMode>
      <Modal
        headerTitle={translate.t(
          "searchFindings.tabResources.modalEditGroupInformation"
        )}
        onEsc={onClose}
        open={isOpen}
      >
        {tempText}
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button id={"edit-group-inf-cancel"} onClick={onClose}>
                {translate.t("confirmmodal.cancel")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </Modal>
    </React.StrictMode>
  );
};

export { EditGroupInformationModal };
