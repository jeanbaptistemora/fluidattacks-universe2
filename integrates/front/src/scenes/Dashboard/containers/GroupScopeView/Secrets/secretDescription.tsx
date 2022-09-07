/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import React from "react";
import { useTranslation } from "react-i18next";

interface IDescriptionProps {
  description: string[];
}

const Description = ({ description }: IDescriptionProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <div>
      <h3>{t("group.scope.git.repo.credentials.secrets.description")}</h3>
      {description}
    </div>
  );
};

export const renderSecretsDescription = (
  props: IDescriptionProps
): JSX.Element => <Description description={props.description} />;
