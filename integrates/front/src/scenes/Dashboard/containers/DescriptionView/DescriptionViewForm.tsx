import { Field, Form, useFormikContext } from "formik";
import yaml from "js-yaml";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import type { ReactElement } from "react";
import type { ConfigurableValidator } from "revalidate";

import { TooltipWrapper } from "components/TooltipWrapper";
import { ActionButtons } from "scenes/Dashboard/containers/DescriptionView/ActionButtons";
import type {
  IFinding,
  IFindingDescriptionData,
} from "scenes/Dashboard/containers/DescriptionView/types";
import type {
  IRequirementData,
  IVulnData,
} from "scenes/Dashboard/containers/GroupDraftsView/types";
import {
  Col100,
  Col45,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import {
  EditableField,
  FormikDropdown,
  FormikTextArea,
} from "utils/forms/fields";
import { translate } from "utils/translations/translate";
import {
  composeValidators,
  maxLength,
  required,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 500;
const MAX_IMPACTS_LENGTH = 300;
const MAX_AFFECTED_SYSTEMS_LENGTH = 200;
const MAX_THREAT_LENGTH = 300;
const MAX_RECOMENDATION_LENGTH = 300;
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxImpactsLength: ConfigurableValidator = maxLength(MAX_IMPACTS_LENGTH);
const maxAffectedSystemsLength: ConfigurableValidator = maxLength(
  MAX_AFFECTED_SYSTEMS_LENGTH
);
const maxThreatLength: ConfigurableValidator = maxLength(MAX_THREAT_LENGTH);
const maxRecommendationLength: ConfigurableValidator = maxLength(
  MAX_RECOMENDATION_LENGTH
);

interface IDescriptionViewFormProps {
  data: IFindingDescriptionData | undefined;
  isEditing: boolean;
  groupLanguage: string | undefined;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const DescriptionViewForm: React.FC<IDescriptionViewFormProps> = ({
  data,
  isEditing,
  groupLanguage,
  setEditing,
}: IDescriptionViewFormProps): JSX.Element => {
  const { dirty, resetForm, submitForm } = useFormikContext();

  const isDescriptionPristine = !dirty;

  const criteriaIdSlice: number = 3;
  const baseUrl: string =
    "https://gitlab.com/api/v4/projects/20741933/repository/files";
  const branchRef: string = "master";
  const baseCriteriaUrl: string = "https://docs.fluidattacks.com/criteria/";

  const [reqsList, setReqsList] = useState<string[]>([]);

  const toggleEdit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      resetForm();
    }
    setEditing(!isEditing);
  }, [isDescriptionPristine, isEditing, resetForm, setEditing]);

  const handleSubmit: () => void = useCallback((): void => {
    if (!isDescriptionPristine) {
      void submitForm();
    }
  }, [isDescriptionPristine, submitForm]);

  const findingNumber = data
    ? data.finding.title.slice(0, criteriaIdSlice)
    : "";

  function getRequirementsText(
    requirements: string[],
    language: string | undefined,
    criteriaData: Record<string, IRequirementData> | undefined
  ): string[] {
    if (criteriaData === undefined) {
      return requirements;
    }
    const requirementsSummaries: string[] = requirements.map(
      (key: string): string => {
        const summary =
          language === "ES"
            ? criteriaData[key].es.summary
            : criteriaData[key].en.summary;

        return `${key}. ${summary}`;
      }
    );

    return requirementsSummaries;
  }

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const vulnsFileId: string =
        "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Fvulnerabilities%2Fdata.yaml";
      const vulnsResponseFile: Response = await fetch(
        `${baseUrl}/${vulnsFileId}/raw?ref=${branchRef}`
      );
      const vulnsYamlFile: string = await vulnsResponseFile.text();
      const vulnsData = vulnsYamlFile
        ? (yaml.load(vulnsYamlFile) as Record<string, IVulnData>)
        : undefined;

      const requirementsFileId: string =
        "makes%2Ffoss%2Fmodules%2Fmakes%2Fcriteria%2Fsrc%2Frequirements%2Fdata.yaml";
      const requirementsResponseFile: Response = await fetch(
        `${baseUrl}/${requirementsFileId}/raw?ref=${branchRef}`
      );
      const requirementsYamlFile: string =
        await requirementsResponseFile.text();
      const requirementsData = requirementsYamlFile
        ? (yaml.load(requirementsYamlFile) as Record<string, IRequirementData>)
        : undefined;

      if (!_.isNil(vulnsData) && !_.isNil(findingNumber)) {
        const { requirements } = vulnsData[findingNumber];
        setReqsList(
          getRequirementsText(requirements, groupLanguage, requirementsData)
        );
      }
    }
    void fetchData();
  }, [findingNumber, groupLanguage, setReqsList]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;

  return (
    <Form id={"editDescription"}>
      <ActionButtons
        isEditing={isEditing}
        isPristine={isDescriptionPristine}
        onEdit={toggleEdit}
        onUpdate={handleSubmit}
      />
      <br />
      <div>
        <div>
          <Row>
            <Can do={"api_resolvers_finding_hacker_resolve"}>
              <Col45>
                <FormGroup>
                  <ControlLabel>
                    <b>{translate.t("searchFindings.tabDescription.hacker")}</b>
                  </ControlLabel>
                  <p className={"ma0"}>{dataset.hacker}</p>
                </FormGroup>
              </Col45>
            </Can>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col100>
                  <TooltipWrapper
                    id={"searchFindings.tabDescription.title.tooltip"}
                    message={translate.t(
                      "searchFindings.tabDescription.title.tooltip"
                    )}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>
                          {translate.t(
                            "searchFindings.tabDescription.title.text"
                          )}
                        </b>
                      </ControlLabel>
                      <p className={"ma0"}>{dataset.title}</p>
                    </FormGroup>
                  </TooltipWrapper>
                </Col100>
              </Row>
            ) : undefined}
          </Can>
          <Row>
            <Col100>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.description}
                    id={"searchFindings.tabDescription.description.tooltip"}
                    infoLink={`${baseCriteriaUrl}vulnerabilities/${findingNumber}`}
                    infoLinkText={translate.t(
                      "searchFindings.tabDescription.description.infoLinkText"
                    )}
                    label={translate.t(
                      "searchFindings.tabDescription.description.text"
                    )}
                    name={"description"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.description.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxDescriptionLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Row>
            <Col100>
              <TooltipWrapper
                id={"searchFindings.tabDescription.requirements.tooltip.id"}
                message={translate.t(
                  "searchFindings.tabDescription.requirements.tooltip"
                )}
              >
                <FormGroup>
                  <ControlLabel>
                    <b>
                      {translate.t(
                        "searchFindings.tabDescription.requirements.text"
                      )}
                    </b>
                  </ControlLabel>
                  {reqsList.length === 0 ? (
                    <p>
                      {translate.t(
                        "searchFindings.tabDescription.requirements.loadingText"
                      )}
                    </p>
                  ) : (
                    <p className={"ws-pre-wrap"}>
                      {reqsList.map((req: string): ReactElement => {
                        return (
                          <a
                            href={`${baseCriteriaUrl}requirements/${req.slice(
                              0,
                              criteriaIdSlice
                            )}`}
                            key={req}
                            rel={"noopener noreferrer"}
                            target={"_blank"}
                          >
                            {req}
                          </a>
                        );
                      })}
                    </p>
                  )}
                </FormGroup>
              </TooltipWrapper>
            </Col100>
          </Row>
          <Row>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.attackVectorDescription}
                    id={"searchFindings.tabDescription.attackVectors.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.attackVectors.text"
                    )}
                    name={"attackVectorDescription"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.attackVectors.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxImpactsLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.affectedSystems}
                    id={"searchFindings.tabDescription.affectedSystems.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.affectedSystems.text"
                    )}
                    name={"affectedSystems"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.affectedSystems.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxAffectedSystemsLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
          </Row>
          <Row>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.threat}
                    id={"searchFindings.tabDescription.threat.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.threat.text"
                    )}
                    name={"threat"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.threat.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxThreatLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col45>
          </Row>
          <Row>
            <Col100>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <EditableField
                    component={FormikTextArea}
                    currentValue={dataset.recommendation}
                    id={"searchFindings.tabDescription.recommendation.tooltip"}
                    label={translate.t(
                      "searchFindings.tabDescription.recommendation.text"
                    )}
                    name={"recommendation"}
                    renderAsEditable={isEditing}
                    tooltip={translate.t(
                      "searchFindings.tabDescription.recommendation.tooltip"
                    )}
                    type={"text"}
                    validate={composeValidators([
                      required,
                      validTextField,
                      maxRecommendationLength,
                    ])}
                    visibleWhileEditing={canEdit}
                  />
                )}
              </Can>
            </Col100>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col45>
                  <TooltipWrapper
                    id={"searchFindings.tabDescription.sorts.tooltip"}
                    message={translate.t(
                      "searchFindings.tabDescription.sorts.tooltip"
                    )}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>
                          {translate.t(
                            "searchFindings.tabDescription.sorts.text"
                          )}
                        </b>
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikDropdown}
                        name={"sorts"}
                        type={"text"}
                        validate={composeValidators([required])}
                      >
                        <option value={""} />
                        <option value={"NO"}>
                          {translate.t("group.findings.boolean.False")}
                        </option>
                        <option value={"YES"}>
                          {translate.t("group.findings.boolean.True")}
                        </option>
                      </Field>
                    </FormGroup>
                  </TooltipWrapper>
                </Col45>
              </Row>
            ) : undefined}
          </Can>
        </div>
      </div>
    </Form>
  );
};

export { DescriptionViewForm };
