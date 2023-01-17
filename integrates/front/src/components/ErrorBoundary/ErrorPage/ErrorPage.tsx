import type { FormEvent } from "react";
import React, { useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useHistory } from "react-router-dom";

import { PageContainer } from "./styles";

import { Announce } from "components/Announce";
import { Button } from "components/Button";
import { Container } from "components/Container";

export const ErrorPage = (): JSX.Element => {
  const { push } = useHistory();
  const { t } = useTranslation();

  const returnHome = useCallback(
    (_event: FormEvent): void => {
      push(`/home`);
      window.location.reload();
    },
    [push]
  );

  return (
    <PageContainer>
      <Container>
        <Announce message={t("app.errorPage")} />
      </Container>
      <Button onClick={returnHome} variant={"primary"}>
        {"Return"}
      </Button>
    </PageContainer>
  );
};
