import type { FC } from "react";
import React, { Fragment } from "react";
import { useTranslation } from "react-i18next";

import type { IFormValues } from "../../types";
import { Input, TextArea } from "components/Input";
import { Col, Row } from "components/Layout";

interface ICredentialsTypeProps {
  credExists: boolean;
  values: IFormValues;
}

export const CredentialsType: FC<ICredentialsTypeProps> = ({
  credExists,
  values,
}: ICredentialsTypeProps): JSX.Element | null => {
  const { t } = useTranslation();

  if (values.credentials.type === "SSH" && !credExists) {
    return (
      <TextArea
        label={t("group.scope.git.repo.credentials.sshKey")}
        name={"credentials.key"}
        placeholder={t("group.scope.git.repo.credentials.sshHint")}
      />
    );
  } else if (values.credentials.type === "HTTPS" && !credExists) {
    return (
      <Fragment>
        {values.credentials.auth === "USER" ? (
          <Row>
            <Col>
              <Input
                label={t("group.scope.git.repo.credentials.user")}
                name={"credentials.user"}
                required={true}
              />
            </Col>
            <Col>
              <Input
                label={t("group.scope.git.repo.credentials.password")}
                name={"credentials.password"}
                required={true}
              />
            </Col>
          </Row>
        ) : undefined}
        {values.credentials.auth === "TOKEN" ? (
          <Row>
            <Col>
              <Input
                label={t("group.scope.git.repo.credentials.token")}
                name={"credentials.token"}
                required={true}
              />
            </Col>
            {values.credentials.isPat ? (
              <Col>
                <Input
                  label={t(
                    "group.scope.git.repo.credentials.azureOrganization.text"
                  )}
                  name={"credentials.azureOrganization"}
                  required={true}
                  tooltip={t(
                    "group.scope.git.repo.credentials.azureOrganization.tooltip"
                  )}
                />
              </Col>
            ) : undefined}
          </Row>
        ) : undefined}
      </Fragment>
    );
  }

  return null;
};
