import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Modal } from "components/Modal";
import { ButtonToolbar, Col100, Row } from "styles/styledComponents";

interface IConcurrentSessionNoticeProps {
  open: boolean;
  onClick: () => void;
}

export const ConcurrentSessionNotice: React.FC<IConcurrentSessionNoticeProps> =
  (props: IConcurrentSessionNoticeProps): JSX.Element => {
    const { open, onClick } = props;
    const { t } = useTranslation();

    return (
      <Modal open={open} title={t("registration.concurrentSessionTitle")}>
        <React.Fragment>
          <p>{t("registration.concurrentSessionMessage")}</p>
          <hr />
          <Row>
            <Col100>
              <ButtonToolbar>
                <Button onClick={onClick} variant={"primary"}>
                  {t("registration.continueBtn")}
                </Button>
              </ButtonToolbar>
            </Col100>
          </Row>
        </React.Fragment>
      </Modal>
    );
  };
