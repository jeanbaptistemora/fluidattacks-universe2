import React from "react";
import { useTranslation } from "react-i18next";

import { PageContainer } from "./styles";

import { Announce } from "components/Announce";
import { Button } from "components/Button";
import { Container } from "components/Container";

export const ErrorPage = (): JSX.Element => {
  const { t } = useTranslation();

  return (
    <PageContainer>
      <Container>
        <Announce message={t("app.errorPage")} />
      </Container>
      <Button variant={"primary"}>{"Return"}</Button>
    </PageContainer>
  );
};
