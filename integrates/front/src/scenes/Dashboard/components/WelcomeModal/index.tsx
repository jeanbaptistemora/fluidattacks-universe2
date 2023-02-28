import React, { useCallback, useContext, useState } from "react";

import { Container } from "components/Container";
import { Lottie } from "components/Icon/Lottie";
import { Modal, ModalConfirm } from "components/Modal";
import { Text } from "components/Text";
import { radar } from "resources";
import type { IAuthContext } from "utils/auth";
import { authContext } from "utils/auth";
import { translate } from "utils/translations/translate";

const WelcomeModal: React.FC = (): JSX.Element => {
  const { t } = translate;

  const user: Required<IAuthContext> = useContext(
    authContext as React.Context<Required<IAuthContext>>
  );

  const enableWelcomeModal = !user.tours.welcome;
  const [isOpen, setIsOpen] = useState(enableWelcomeModal);

  const closeModal = useCallback((): void => {
    user.setUser({
      tours: {
        newGroup: user.tours.newGroup,
        newRiskExposure: user.tours.newRiskExposure,
        newRoot: user.tours.newRoot,
        welcome: true,
      },
      userEmail: user.userEmail,
      userIntPhone: user.userIntPhone,
      userName: user.userName,
    });
    setIsOpen(false);
  }, [user]);

  return (
    <Modal maxWidth={"750px"} open={isOpen}>
      <Container display={"flex"} justify={"center"} scroll={"none"}>
        <Lottie animationData={radar} size={200} />
      </Container>
      <Text fw={9} lineHeight={"1.4"} size={"big"} ta={"center"}>
        {t("autoenrollment.welcome.modal.title")}
      </Text>
      <Text lineHeight={"1.4"} mb={3} mt={3} size={"medium"} ta={"center"}>
        {t("autoenrollment.welcome.modal.subtitle")}
      </Text>
      <Container display={"flex"} justify={"center"} scroll={"none"}>
        <ModalConfirm
          id={"welcome-close"}
          onConfirm={closeModal}
          txtConfirm={t("autoenrollment.welcome.modal.button")}
        />
      </Container>
    </Modal>
  );
};

export { WelcomeModal };
