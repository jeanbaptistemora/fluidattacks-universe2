import _ from "lodash";
import React, { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { MemoryRouter, Route } from "react-router-dom";

import { AdditionalInfo } from "./AdditionalInfo";
import { UpdateDescriptionContext, defaultValue } from "./context";
import type {
  IUpdateTreatmentVulnerabilityForm,
  IVulnRowAttr,
  IVulnerabilityModalValues,
} from "./types";
import { UpdateDescription } from "./UpdateDescription";

import { ContentTab } from "../ContentTab";
import { Modal } from "components/Modal";
import { TabsContainer } from "styles/styledComponents";

interface IAdditionalInformationModal {
  canDisplayAnalyst: boolean;
  canDeleteVulnsTags: boolean;
  canRequestZeroRiskVuln: boolean;
  canUpdateVulnsTreatment: boolean;
  clearSelectedVulns: () => void;
  closeAdditionalInfoModal: () => void;
  currentRow: IVulnRowAttr | undefined;
  findingId: string;
  groupName: string;
  isAdditionalInfoOpen: boolean;
  isFindingReleased: boolean;
}

const AdditionalInformation: React.FC<IAdditionalInformationModal> = ({
  canDisplayAnalyst,
  canDeleteVulnsTags,
  canRequestZeroRiskVuln,
  canUpdateVulnsTreatment,
  clearSelectedVulns,
  closeAdditionalInfoModal,
  currentRow = undefined,
  findingId,
  groupName,
  isAdditionalInfoOpen,
  isFindingReleased,
}: IAdditionalInformationModal): JSX.Element => {
  const { t } = useTranslation();
  const [treatmentForm, setTreatmentForm] =
    useState<IUpdateTreatmentVulnerabilityForm>(defaultValue);
  const value = useMemo(
    (): IVulnerabilityModalValues => [treatmentForm, setTreatmentForm],
    [treatmentForm, setTreatmentForm]
  );

  function onClose(): void {
    setTreatmentForm(defaultValue);
    closeAdditionalInfoModal();
  }

  return (
    <Modal
      headerTitle={t("searchFindings.tabVuln.vulnerabilityInfo")}
      open={isAdditionalInfoOpen}
      size={"largeModal"}
    >
      <UpdateDescriptionContext.Provider value={value}>
        {_.isUndefined(currentRow) ? undefined : (
          <MemoryRouter
            initialEntries={["/details", "/treatments"]}
            initialIndex={0}
          >
            {/* Use className to override default styles */}
            {/* eslint-disable-next-line react/forbid-component-props */}
            <TabsContainer className={"nt3"}>
              <ContentTab
                icon={"icon pe-7s-graph3"}
                id={"vulnerabilityDetailsTab"}
                link={"/details"}
                title={t("searchFindings.tabVuln.contentTab.details.title")}
                tooltip={t("searchFindings.tabVuln.contentTab.details.tooltip")}
              />
              {currentRow.currentState === "open" &&
              isFindingReleased &&
              (canUpdateVulnsTreatment ||
                canRequestZeroRiskVuln ||
                canDeleteVulnsTags) ? (
                <ContentTab
                  icon={"icon pe-7s-note"}
                  id={"vulnerabilityTreatmentsTab"}
                  link={"/treatments"}
                  title={t(
                    "searchFindings.tabVuln.contentTab.treatments.title"
                  )}
                  tooltip={t(
                    "searchFindings.tabVuln.contentTab.treatments.tooltip"
                  )}
                />
              ) : undefined}
            </TabsContainer>
            <Route path={"/details"}>
              <AdditionalInfo
                canDisplayAnalyst={canDisplayAnalyst}
                onClose={onClose}
                vulnerability={currentRow}
              />
            </Route>
            <Route path={"/treatments"}>
              <UpdateDescription
                findingId={findingId}
                groupName={groupName}
                handleClearSelected={clearSelectedVulns}
                handleCloseModal={onClose}
                vulnerabilities={[currentRow]}
              />
            </Route>
          </MemoryRouter>
        )}
      </UpdateDescriptionContext.Provider>
    </Modal>
  );
};

export { IAdditionalInformationModal, AdditionalInformation };
