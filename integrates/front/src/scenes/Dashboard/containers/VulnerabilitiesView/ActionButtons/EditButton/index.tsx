import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { faPen, faRotateRight } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import React, { useMemo } from "react";
import { useTranslation } from "react-i18next";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Tooltip } from "components/Tooltip";
import { authzPermissionsContext } from "utils/authz/config";

interface IEditButtonProps {
  isDisabled: boolean;
  isEditing: boolean;
  isFindingReleased: boolean;
  isRequestingReattack: boolean;
  isVerifying: boolean;
  onEdit: () => void;
}

const EditButton: React.FC<IEditButtonProps> = ({
  isDisabled,
  isEditing,
  isFindingReleased,
  isRequestingReattack,
  isVerifying,
  onEdit,
}: IEditButtonProps): JSX.Element => {
  const { t } = useTranslation();

  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canRequestZeroRiskVuln: boolean = permissions.can(
    "api_mutations_request_vulnerabilities_zero_risk_mutate"
  );
  const canUpdateVulnsTreatment: boolean = permissions.can(
    "api_mutations_update_vulnerabilities_treatment_mutate"
  );
  const shouldRenderEditBtn: boolean =
    isFindingReleased &&
    !(isRequestingReattack || isVerifying) &&
    (canRequestZeroRiskVuln || canUpdateVulnsTreatment);

  const tooltipMessage = useMemo((): string => {
    if (isEditing) {
      return t("searchFindings.tabDescription.save.tooltip");
    }

    return t("searchFindings.tabVuln.buttonsTooltip.edit");
  }, [isEditing, t]);

  return (
    <React.StrictMode>
      {shouldRenderEditBtn ? (
        <Container>
          <Tooltip
            disp={"inline-block"}
            id={"searchFindings.tabDescription.saveEdit.tooltip.id"}
            tip={tooltipMessage}
          >
            <Button
              disabled={isRequestingReattack || isVerifying || isDisabled}
              id={"vulnerabilities-edit"}
              onClick={onEdit}
              variant={"ghost"}
            >
              {isEditing ? (
                <React.Fragment>
                  <FontAwesomeIcon icon={faRotateRight} />
                  &nbsp;{t("searchFindings.tabDescription.save.text")}
                </React.Fragment>
              ) : (
                <React.Fragment>
                  <FontAwesomeIcon icon={faPen} />
                  &nbsp;{t("searchFindings.tabVuln.buttons.edit")}
                </React.Fragment>
              )}
            </Button>
          </Tooltip>
        </Container>
      ) : undefined}
    </React.StrictMode>
  );
};

export type { IEditButtonProps };
export { EditButton };
