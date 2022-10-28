/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

import {
  faPen,
  faRotateRight,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { ButtonToolbarRow } from "styles/styledComponents";
import { Can } from "utils/authz/Can";

interface IActionButtonsProps {
  isEditing: boolean;
  isPristine: boolean;
  onEdit: () => void;
  onUpdate: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isEditing,
  isPristine,
  onEdit,
  onUpdate,
}: IActionButtonsProps): JSX.Element => {
  const { t } = useTranslation();

  return (
    <ButtonToolbarRow>
      <Can do={"api_mutations_update_vulnerability_description_mutate"}>
        {isEditing ? (
          <Tooltip
            id={"searchFindings.tabVuln.additionalInfo.buttons.save.tooltip"}
            tip={t(
              "searchFindings.tabVuln.additionalInfo.buttons.save.tooltip"
            )}
          >
            <Button
              disabled={isPristine}
              onClick={onUpdate}
              variant={"primary"}
            >
              <FontAwesomeIcon icon={faRotateRight} />
              &nbsp;
              {t("searchFindings.tabVuln.additionalInfo.buttons.save.text")}
            </Button>
          </Tooltip>
        ) : undefined}
        <Tooltip
          id={"searchFindings.tabVuln.additionalInfo.buttons.cancel.edit"}
          tip={
            isEditing
              ? t(
                  "searchFindings.tabVuln.additionalInfo.buttons.cancel.tooltip"
                )
              : t("searchFindings.tabVuln.additionalInfo.buttons.edit.tooltip")
          }
        >
          <Button onClick={onEdit} variant={"secondary"}>
            {isEditing ? (
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {t("searchFindings.tabVuln.additionalInfo.buttons.cancel.text")}
              </React.Fragment>
            ) : (
              <React.Fragment>
                <FontAwesomeIcon icon={faPen} />
                &nbsp;
                {t("searchFindings.tabVuln.additionalInfo.buttons.edit.text")}
              </React.Fragment>
            )}
          </Button>
        </Tooltip>
      </Can>
    </ButtonToolbarRow>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
