/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import type { FC } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

import type {
  IUnfulfilledRequirementAttr,
  IUnfulfilledStandardAttr,
} from "../types";
import { Card } from "components/Card";
import { ExternalLink } from "components/ExternalLink";
import { Col } from "components/Layout/Col";
import { Row } from "components/Layout/Row";
import { Text } from "components/Text";

interface IUnfulfilledStandardCardProps {
  unfulfilledStandard: IUnfulfilledStandardAttr;
}

const BASE_CRITERIA_URL: string = "https://docs.fluidattacks.com/criteria/";

const UnfulfilledStandardCard: FC<IUnfulfilledStandardCardProps> = (
  props: IUnfulfilledStandardCardProps
): JSX.Element => {
  const {
    unfulfilledStandard: { title, unfulfilledRequirements },
  } = props;
  const { t } = useTranslation();
  const areManyRequirement = unfulfilledRequirements.length > 2;

  return (
    <Card>
      <Row>
        <Text fw={6} size={"medium"} ta={"center"}>
          {title.toUpperCase()}
        </Text>
      </Row>
      <br />
      <Row>
        <Col lg={100} md={100} sm={100}>
          <Text size={"small"} ta={"center"}>
            {t("organization.tabs.compliance.tabs.standards.cards.requirement")}
            {areManyRequirement ? ` (${unfulfilledRequirements.length})` : ""}
          </Text>
          {areManyRequirement
            ? undefined
            : unfulfilledRequirements.map(
                (requirement: IUnfulfilledRequirementAttr): JSX.Element => (
                  <Text
                    key={requirement.id}
                    size={"small"}
                    ta={"center"}
                    tone={"red"}
                  >
                    <ExternalLink
                      href={`${BASE_CRITERIA_URL}requirements/${requirement.id}`}
                    >
                      {`${requirement.id} ${requirement.title}`}
                    </ExternalLink>
                  </Text>
                )
              )}
        </Col>
      </Row>
    </Card>
  );
};
export { UnfulfilledStandardCard };
