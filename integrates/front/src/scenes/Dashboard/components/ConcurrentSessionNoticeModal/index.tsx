import { Button } from "components/Button";
import { Modal } from "components/Modal";
import React from "react";
import { useTranslation } from "react-i18next";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface IConcurrentSessionNoticeProps {
  open: boolean;
  onClick: () => void;
}

export const ConcurrentSessionNotice: React.FC<IConcurrentSessionNoticeProps> = (
  props: IConcurrentSessionNoticeProps
): JSX.Element => {
  const { open, onClick } = props;
  const { t } = useTranslation();

  return (
    <Modal headerTitle={t("registration.concurrent_session_title")} open={open}>
      <React.Fragment>
        <p>{t("registration.concurrent_session_message")}</p>
        <hr />
        <Row>
          <Col100>
            <ButtonToolbar>
              <Button onClick={onClick}>
                {t("registration.continue_btn")}
              </Button>
            </ButtonToolbar>
          </Col100>
        </Row>
      </React.Fragment>
    </Modal>
  );
};
