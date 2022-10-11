/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import { faAngleDown, faAngleUp } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { FC } from "react";
import React, { useState } from "react";
import { useTranslation } from "react-i18next";

import type {
  IUnfulfilledRequirementAttr,
  IUnfulfilledStandardAttr,
} from "../types";
import { Button } from "components/Button";
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
  const areManyRequirements = unfulfilledRequirements.length > 2;

  // Handle state
  const [showAllRequirements, setShowAllRequirements] = useState(
    !areManyRequirements
  );

  // Handle actions
  function handleShowAll(): void {
    setShowAllRequirements(!showAllRequirements);
  }
  function getButtonVariant(selected: boolean): "input" | "selected-input" {
    return selected ? "selected-input" : "input";
  }
  function getButtonAngle(selected: boolean): JSX.Element {
    return selected ? (
      <FontAwesomeIcon icon={faAngleDown} />
    ) : (
      <FontAwesomeIcon icon={faAngleUp} />
    );
  }
  function getRequirementsAlignment(areManyItems: boolean): "center" | "start" {
    return areManyItems ? "start" : "center";
  }

  return (
    <Card>
      <Row>
        <Text fw={6} size={"medium"} ta={"center"}>
          {title.toUpperCase()}
        </Text>
      </Row>
      <Row>
        <Col lg={100} md={100} sm={100}>
          <Text mb={2} mt={3} size={"small"} ta={"center"}>
            {t("organization.tabs.compliance.tabs.standards.cards.requirement")}
            {areManyRequirements ? ` (${unfulfilledRequirements.length})` : ""}
          </Text>
          {areManyRequirements ? (
            <div className={"mb2 mt3"}>
              <Button
                disp={"block"}
                onClick={handleShowAll}
                variant={getButtonVariant(showAllRequirements)}
              >
                <div className={"flex flex-row justify-between"}>
                  <div>
                    <Text size={"small"} ta={"start"}>
                      {t(
                        "organization.tabs.compliance.tabs.standards.cards.showAll"
                      )}
                    </Text>
                  </div>
                  <div>
                    <Text size={"small"} ta={"end"}>
                      {getButtonAngle(showAllRequirements)}
                    </Text>
                  </div>
                </div>
              </Button>
            </div>
          ) : undefined}
          {showAllRequirements
            ? unfulfilledRequirements.map(
                (requirement: IUnfulfilledRequirementAttr): JSX.Element => (
                  <Text
                    key={requirement.id}
                    size={"small"}
                    ta={getRequirementsAlignment(areManyRequirements)}
                    tone={"red"}
                  >
                    <ExternalLink
                      href={`${BASE_CRITERIA_URL}requirements/${requirement.id}`}
                    >
                      {`${requirement.id} ${requirement.title}`}
                    </ExternalLink>
                  </Text>
                )
              )
            : undefined}
        </Col>
      </Row>
    </Card>
  );
};
export { UnfulfilledStandardCard };
