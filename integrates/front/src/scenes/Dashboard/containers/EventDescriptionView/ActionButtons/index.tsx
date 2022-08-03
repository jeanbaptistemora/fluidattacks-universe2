import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import {
  faCheck,
  faPen,
  faRotateRight,
  faTimes,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Tooltip } from "components/Tooltip";
import { ButtonToolbarStartRow, Row } from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { authzPermissionsContext } from "utils/authz/config";

interface IActionButtonsProps {
  isDirtyForm: boolean;
  isEditing: boolean;
  eventStatus: string;
  onEdit: () => void;
  openSolvingModal: () => void;
}

const ActionButtons: React.FC<IActionButtonsProps> = ({
  isDirtyForm,
  isEditing,
  eventStatus,
  onEdit: onToggleEdit,
  openSolvingModal,
}: IActionButtonsProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canUpdateEvent: boolean = permissions.can(
    "api_mutations_update_event_mutate"
  );
  const canUpdateEventSolvingReason: boolean = permissions.can(
    "api_mutations_update_event_solving_reason_mutate"
  );

  return (
    <Row>
      <ButtonToolbarStartRow>
        {isEditing ? undefined : eventStatus === "SOLVED" ? undefined : (
          <Can do={"api_mutations_solve_event_mutate"}>
            <Button onClick={openSolvingModal} variant={"primary"}>
              <FontAwesomeIcon icon={faCheck} />
              &nbsp;
              {t("group.events.description.markAsSolved")}
            </Button>
          </Can>
        )}
        {(canUpdateEvent || canUpdateEventSolvingReason) && isEditing ? (
          <React.Fragment>
            <Button onClick={onToggleEdit} variant={"secondary"}>
              <React.Fragment>
                <FontAwesomeIcon icon={faTimes} />
                &nbsp;
                {t("group.events.description.cancel")}
              </React.Fragment>
            </Button>
            <Tooltip
              id={"group.events.description.save.tooltip.btn"}
              tip={t("group.events.description.save.tooltip")}
            >
              <Button
                disabled={!isDirtyForm}
                type={"submit"}
                variant={"primary"}
              >
                <FontAwesomeIcon icon={faRotateRight} />
                &nbsp;
                {t("group.events.description.save.text")}
              </Button>
            </Tooltip>
          </React.Fragment>
        ) : (
          <Tooltip
            id={"group.events.description.edit.tooltip.btn"}
            tip={t("group.events.description.edit.tooltip")}
          >
            <Button onClick={onToggleEdit} variant={"secondary"}>
              <FontAwesomeIcon icon={faPen} />
              &nbsp;
              {t("group.events.description.edit.text")}
            </Button>
          </Tooltip>
        )}
      </ButtonToolbarStartRow>
    </Row>
  );
};

export type { IActionButtonsProps };
export { ActionButtons };
