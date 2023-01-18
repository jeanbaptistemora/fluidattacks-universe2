import { faHeadset } from "@fortawesome/free-solid-svg-icons";
import React from "react";
import type { FC } from "react";
import { useTranslation } from "react-i18next";

import { UpgradeGroupsModal } from "../UpgradeGroupsModal";
import { Button } from "components/Button";
import { Container } from "components/Container";
import { Col, Row } from "components/Layout";
import { useCalendly } from "utils/hooks";

const ExpertButton: FC = (): JSX.Element => {
  const { t } = useTranslation();
  const { closeUpgradeModal, isAvailable, isUpgradeOpen, openCalendly } =
    useCalendly();

  return (
    <div>
      {isAvailable ? (
        <Container margin={"16px 0 0 0"} scroll={"none"}>
          <Row justify={"end"}>
            <Col>
              <Button
                disp={"inline-block"}
                icon={faHeadset}
                onClick={openCalendly}
                variant={"primary"}
              >
                {t("navbar.help.options.expert.title")}
              </Button>
            </Col>
          </Row>
        </Container>
      ) : (
        <div />
      )}
      {isUpgradeOpen ? (
        <UpgradeGroupsModal onClose={closeUpgradeModal} />
      ) : (
        <div />
      )}
    </div>
  );
};

export { ExpertButton };
