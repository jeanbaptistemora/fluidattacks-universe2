import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface IUpgradeSubscriptionModalProps {
  onClose: () => void;
}

const UpgradeSubscriptionModal: React.FC<IUpgradeSubscriptionModalProps> = ({
  onClose,
}: IUpgradeSubscriptionModalProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <Modal headerTitle={t("upgrade.title")} open={true}>
      <p>{t("upgrade.text")}</p>
      <hr />
      <Row>
        <Col100>
          <ButtonToolbar>
            <Button onClick={onClose}>{t("upgrade.close")}</Button>
          </ButtonToolbar>
        </Col100>
      </Row>
    </Modal>
  );
};

export { UpgradeSubscriptionModal };
