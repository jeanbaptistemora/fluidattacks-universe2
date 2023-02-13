import { useMutation } from "@apollo/client";
import type { PureAbility } from "@casl/ability";
import { useAbility } from "@casl/react";
import { Form, Formik } from "formik";
import React, { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { object, string } from "yup";

import type { IFormValues, IZeroRiskFormProps } from "./types";

import { getRequestedZeroRiskVulns } from "../../utils";
import {
  confirmZeroRiskProps,
  isConfirmZeroRiskSelectedHelper,
  isRejectZeroRiskSelectedHelper,
  rejectZeroRiskProps,
} from "../helpers";
import {
  CONFIRM_VULNERABILITIES_ZERO_RISK,
  REJECT_VULNERABILITIES_ZERO_RISK,
} from "../queries";
import type { IVulnDataAttr } from "../types";
import { ZeroRiskTable } from "../ZeroRiskTable";
import { Select, TextArea } from "components/Input";
import { ModalConfirm } from "components/Modal";
import { authzPermissionsContext } from "utils/authz/config";

const ZeroRiskForm: React.FC<IZeroRiskFormProps> = ({
  groupName,
  findingId,
  onCancel,
  refetchData,
  vulnerabilities,
}: IZeroRiskFormProps): JSX.Element => {
  const { t } = useTranslation();
  const permissions: PureAbility<string> = useAbility(authzPermissionsContext);
  const canSeeDropDownToConfirmZeroRisk: boolean = permissions.can(
    "see_dropdown_to_confirm_zero_risk"
  );

  // State
  const [acceptanceVulnerabilities, setAcceptanceVulnerabilities] = useState<
    IVulnDataAttr[]
  >(getRequestedZeroRiskVulns(vulnerabilities));
  const [confirmedVulnerabilities, setConfirmedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);
  const [rejectedVulnerabilities, setRejectedVulnerabilities] = useState<
    IVulnDataAttr[]
  >([]);

  // GraphQL operations
  const [confirmZeroRisk, { loading: confirmingZeroRisk }] = useMutation(
    CONFIRM_VULNERABILITIES_ZERO_RISK,
    confirmZeroRiskProps(refetchData, onCancel, findingId)
  );
  const [rejectZeroRisk, { loading: rejectingZeroRisk }] = useMutation(
    REJECT_VULNERABILITIES_ZERO_RISK,
    rejectZeroRiskProps(refetchData, onCancel, groupName, findingId)
  );

  // Handle actions
  const handleSubmit = useCallback(
    (formValues: IFormValues): void => {
      isConfirmZeroRiskSelectedHelper(
        true,
        confirmZeroRisk,
        confirmedVulnerabilities,
        formValues
      );
      isRejectZeroRiskSelectedHelper(
        true,
        rejectZeroRisk,
        formValues,
        rejectedVulnerabilities
      );
    },
    [
      confirmZeroRisk,
      confirmedVulnerabilities,
      rejectZeroRisk,
      rejectedVulnerabilities,
    ]
  );

  // Side effects
  useEffect((): void => {
    setConfirmedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "APPROVED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
    setRejectedVulnerabilities(
      acceptanceVulnerabilities.reduce(
        (acc: IVulnDataAttr[], vulnerability: IVulnDataAttr): IVulnDataAttr[] =>
          vulnerability.acceptance === "REJECTED"
            ? [...acc, vulnerability]
            : acc,
        []
      )
    );
  }, [acceptanceVulnerabilities]);

  return (
    <Formik
      enableReinitialize={true}
      initialValues={{ justification: "" }}
      name={"zeroRiskForm"}
      onSubmit={handleSubmit}
      validationSchema={object().shape({
        justification: string().required(t("validations.required")),
      })}
    >
      <Form id={"zeroRiskForm"}>
        <ZeroRiskTable
          acceptanceVulns={acceptanceVulnerabilities}
          isConfirmRejectZeroRiskSelected={true}
          setAcceptanceVulns={setAcceptanceVulnerabilities}
        />
        <br />
        {canSeeDropDownToConfirmZeroRisk ? (
          <Select
            label={t(
              "searchFindings.tabDescription.remediationModal.observations"
            )}
            name={"justification"}
            required={true}
          >
            <option value={""} />
            {confirmedVulnerabilities.length > 0 ? (
              <React.Fragment>
                <option value={"FP"}>
                  {t(
                    "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.fp"
                  )}
                </option>
                <option value={"Out of the scope"}>
                  {t(
                    "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.confirmation.outOfTheScope"
                  )}
                </option>
              </React.Fragment>
            ) : undefined}
            {rejectedVulnerabilities.length > 0 ? (
              <React.Fragment>
                <option value={"FN"}>
                  {t(
                    "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.fn"
                  )}
                </option>
                <option value={"Complementary control"}>
                  {t(
                    "searchFindings.tabDescription.handleAcceptanceModal.zeroRiskJustification.rejection.complementaryControl"
                  )}
                </option>
              </React.Fragment>
            ) : undefined}
          </Select>
        ) : (
          <TextArea
            label={t(
              "searchFindings.tabDescription.remediationModal.observations"
            )}
            name={"justification"}
            required={true}
          />
        )}
        <br />
        <ModalConfirm
          disabled={
            (confirmedVulnerabilities.length === 0 &&
              rejectedVulnerabilities.length === 0) ||
            confirmingZeroRisk ||
            rejectingZeroRisk
          }
          onCancel={onCancel}
        />
      </Form>
    </Formik>
  );
};

export { ZeroRiskForm };
