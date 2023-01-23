import { Field, Form, useFormikContext } from "formik";
import _ from "lodash";
import React, { useCallback, useEffect, useState } from "react";
import type { ReactElement } from "react";
import { useTranslation } from "react-i18next";
import type { ConfigurableValidator } from "revalidate";

import {
  getRequerimentsData,
  getRequirementsText,
  getVulnsData,
} from "./utils";

import { ExternalLink } from "components/ExternalLink";
import { Editable, TextArea } from "components/Input";
import { Tooltip } from "components/Tooltip";
import { ActionButtons } from "scenes/Dashboard/containers/Finding-Content/DescriptionView/ActionButtons";
import type {
  IFinding,
  IFindingDescriptionData,
} from "scenes/Dashboard/containers/Finding-Content/DescriptionView/types";
import { validateNotEmpty } from "scenes/Dashboard/containers/Group-Content/GroupDraftsView/utils";
import {
  Col100,
  Col45,
  ControlLabel,
  FormGroup,
  Row,
} from "styles/styledComponents";
import { Can } from "utils/authz/Can";
import { Have } from "utils/authz/Have";
import { FormikAutocompleteText, FormikDropdown } from "utils/forms/fields";
import {
  composeValidators,
  maxLength,
  required,
  validDraftTitle,
  validFindingTypology,
  validTextField,
} from "utils/validations";

const MAX_DESCRIPTION_LENGTH = 500;
const MAX_IMPACTS_LENGTH = 300;
const MAX_THREAT_LENGTH = 300;
const MAX_RECOMENDATION_LENGTH = 300;
const maxDescriptionLength: ConfigurableValidator = maxLength(
  MAX_DESCRIPTION_LENGTH
);
const maxImpactsLength: ConfigurableValidator = maxLength(MAX_IMPACTS_LENGTH);
const maxThreatLength: ConfigurableValidator = maxLength(MAX_THREAT_LENGTH);
const maxRecommendationLength: ConfigurableValidator = maxLength(
  MAX_RECOMENDATION_LENGTH
);

interface IDescriptionViewFormProps {
  data: IFindingDescriptionData | undefined;
  isDraft: boolean;
  isEditing: boolean;
  groupLanguage: string | undefined;
  setEditing: React.Dispatch<React.SetStateAction<boolean>>;
}

const DescriptionViewForm: React.FC<IDescriptionViewFormProps> = ({
  data,
  isDraft,
  isEditing,
  groupLanguage,
  setEditing,
}: IDescriptionViewFormProps): JSX.Element => {
  const { dirty, resetForm, submitForm } = useFormikContext();
  const { t } = useTranslation();

  const isDescriptionPristine = !dirty;

  const criteriaIdSlice: number = 3;
  const baseCriteriaUrl: string = "https://docs.fluidattacks.com/criteria/";

  const [reqsList, setReqsList] = useState<string[]>([]);
  const [titleSuggestions, setTitleSuggestions] = useState<string[]>([]);

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

  useEffect((): void => {
    async function fetchData(): Promise<void> {
      const vulnsData = await getVulnsData();
      const requirementsData = await getRequerimentsData();

      if (!_.isNil(vulnsData) && !_.isNil(findingNumber)) {
        const { requirements } = vulnsData[findingNumber];
        setReqsList(
          getRequirementsText(requirements, requirementsData, groupLanguage)
        );
        const titlesList = Object.keys(vulnsData).map((key: string): string => {
          return groupLanguage === "ES"
            ? `${key}. ${validateNotEmpty(vulnsData[key].es.title)}`
            : `${key}. ${validateNotEmpty(vulnsData[key].en.title)}`;
        });
        setTitleSuggestions(titlesList);
      }
    }
    void fetchData();
  }, [findingNumber, groupLanguage, setReqsList]);

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <div />;
  }

  const dataset: IFinding = data.finding;

  const validateFindingTypology: ConfigurableValidator =
    validFindingTypology(titleSuggestions);

  return (
    <Form id={"editDescription"}>
      <Have I={"can_report_vulnerabilities"}>
        <ActionButtons
          isEditing={isEditing}
          isPristine={isDescriptionPristine}
          onEdit={toggleEdit}
          onUpdate={handleSubmit}
        />
      </Have>
      <br />
      <div>
        <div>
          <Row>
            <Can do={"api_resolvers_finding_hacker_resolve"}>
              <Col45>
                <FormGroup>
                  <ControlLabel>
                    <b>{t("searchFindings.tabDescription.hacker")}</b>
                  </ControlLabel>
                  <p className={"ma0"}>{dataset.hacker}</p>
                </FormGroup>
              </Col45>
            </Can>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing && isDraft ? (
              <Row>
                <Col100>
                  <Tooltip
                    id={"searchFindings.tabDescription.title.tooltip"}
                    tip={t("searchFindings.tabDescription.title.tooltip")}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>{t("searchFindings.tabDescription.title.text")}</b>
                      </ControlLabel>
                      <br />
                      <Field
                        component={FormikAutocompleteText}
                        name={"title"}
                        suggestions={_.sortBy(titleSuggestions)}
                        type={"text"}
                        validate={composeValidators([
                          required,
                          validDraftTitle,
                          validateFindingTypology,
                        ])}
                      />
                    </FormGroup>
                  </Tooltip>
                </Col100>
              </Row>
            ) : undefined}
          </Can>
          <Row>
            <Can
              do={"api_mutations_update_finding_description_mutate"}
              passThrough={true}
            >
              {(canEdit: boolean): JSX.Element => (
                <Col100>
                  <Editable
                    currentValue={dataset.description}
                    isEditing={isEditing && canEdit}
                    label={t("searchFindings.tabDescription.description.text")}
                    tooltip={t(
                      "searchFindings.tabDescription.description.tooltip"
                    )}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.description.tooltip"}
                      label={t(
                        "searchFindings.tabDescription.description.text"
                      )}
                      name={"description"}
                      tooltip={t(
                        "searchFindings.tabDescription.description.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxDescriptionLength,
                      ])}
                    />
                  </Editable>
                  {isEditing && canEdit ? undefined : (
                    <ExternalLink
                      href={`${baseCriteriaUrl}vulnerabilities/${findingNumber}`}
                    >
                      {t(
                        "searchFindings.tabDescription.description.infoLinkText"
                      )}
                    </ExternalLink>
                  )}
                </Col100>
              )}
            </Can>
          </Row>
          <Row>
            <Col100>
              <Tooltip
                id={"searchFindings.tabDescription.requirements.tooltip.id"}
                tip={t("searchFindings.tabDescription.requirements.tooltip")}
              >
                <FormGroup>
                  <ControlLabel>
                    <b>
                      {t("searchFindings.tabDescription.requirements.text")}
                    </b>
                  </ControlLabel>
                  {reqsList.length === 0 ? (
                    <p>
                      {t(
                        "searchFindings.tabDescription.requirements.loadingText"
                      )}
                    </p>
                  ) : (
                    <div className={"ws-pre-wrap"}>
                      {reqsList.map((req: string): ReactElement => {
                        return (
                          <div className={"w-100"} key={req}>
                            <ExternalLink
                              href={`${baseCriteriaUrl}requirements/${req.slice(
                                0,
                                criteriaIdSlice
                              )}`}
                            >
                              {req}
                            </ExternalLink>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </FormGroup>
              </Tooltip>
            </Col100>
          </Row>
          <Row>
            <Col45>
              <Can
                do={"api_mutations_update_finding_description_mutate"}
                passThrough={true}
              >
                {(canEdit: boolean): JSX.Element => (
                  <Editable
                    currentValue={dataset.attackVectorDescription}
                    isEditing={isEditing && canEdit}
                    label={t(
                      "searchFindings.tabDescription.attackVectors.text"
                    )}
                    tooltip={t(
                      "searchFindings.tabDescription.attackVectors.tooltip"
                    )}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.attackVectors.tooltip"}
                      label={t(
                        "searchFindings.tabDescription.attackVectors.text"
                      )}
                      name={"attackVectorDescription"}
                      tooltip={t(
                        "searchFindings.tabDescription.attackVectors.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxImpactsLength,
                      ])}
                    />
                  </Editable>
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
                  <Editable
                    currentValue={dataset.threat}
                    isEditing={isEditing && canEdit}
                    label={t("searchFindings.tabDescription.threat.text")}
                    tooltip={t("searchFindings.tabDescription.threat.tooltip")}
                  >
                    <TextArea
                      id={"searchFindings.tabDescription.threat.tooltip"}
                      label={t("searchFindings.tabDescription.threat.text")}
                      name={"threat"}
                      tooltip={t(
                        "searchFindings.tabDescription.threat.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxThreatLength,
                      ])}
                    />
                  </Editable>
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
                  <Editable
                    currentValue={dataset.recommendation}
                    isEditing={isEditing && canEdit}
                    label={t(
                      "searchFindings.tabDescription.recommendation.text"
                    )}
                    tooltip={t(
                      "searchFindings.tabDescription.recommendation.tooltip"
                    )}
                  >
                    <TextArea
                      id={
                        "searchFindings.tabDescription.recommendation.tooltip"
                      }
                      label={t(
                        "searchFindings.tabDescription.recommendation.text"
                      )}
                      name={"recommendation"}
                      tooltip={t(
                        "searchFindings.tabDescription.recommendation.tooltip"
                      )}
                      validate={composeValidators([
                        required,
                        validTextField,
                        maxRecommendationLength,
                      ])}
                    />
                  </Editable>
                )}
              </Can>
            </Col100>
          </Row>
          <Can do={"api_mutations_update_finding_description_mutate"}>
            {isEditing ? (
              <Row>
                <Col45>
                  <Tooltip
                    id={"searchFindings.tabDescription.sorts.tooltip"}
                    tip={t("searchFindings.tabDescription.sorts.tooltip")}
                  >
                    <FormGroup>
                      <ControlLabel>
                        <b>{t("searchFindings.tabDescription.sorts.text")}</b>
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
                          {t("group.findings.boolean.False")}
                        </option>
                        <option value={"YES"}>
                          {t("group.findings.boolean.True")}
                        </option>
                      </Field>
                    </FormGroup>
                  </Tooltip>
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
