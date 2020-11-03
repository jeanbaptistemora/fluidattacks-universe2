/* eslint-disable react/forbid-component-props
  -------
  We need className to override default styles from react-boostrap.
*/
import { Button } from "components/Button/index";
import { ConfigurableValidator } from "revalidate";
import React from "react";
import { TooltipWrapper } from "components/TooltipWrapper";
import style from "scenes/Dashboard/components/AddRepositoriesModal/index.css";
import { translate } from "utils/translations/translate";
import { Col, Glyphicon, Row } from "react-bootstrap";
import { Dropdown, Text } from "utils/forms/fields";
import { Field, WrappedFieldArrayProps } from "redux-form";
import { maxLength, required, validField } from "utils/validations";

const MAX_REPO_URL_LENGTH: number = 300;
const MAX_REPO_BRANCH_LENGTH: number = 40;

const maxRepoUrlLength: ConfigurableValidator = maxLength(MAX_REPO_URL_LENGTH);
const maxRepoBranchLength: ConfigurableValidator = maxLength(
  MAX_REPO_BRANCH_LENGTH
);
const RepositoryFields: React.FC<WrappedFieldArrayProps> = (
  props: WrappedFieldArrayProps
): JSX.Element => {
  const { fields } = props;
  function addItem(): void {
    //This is not a mutator, it dispatches an action which updates the state
    //eslint-disable-next-line fp/no-mutating-methods
    fields.push({ branch: "", urlRepo: "" });
  }

  return (
    <React.Fragment>
      {fields.map(
        (fieldName: string, index: number): React.ReactFragment => {
          function removeItem(): void {
            props.fields.remove(index);
          }

          return (
            <React.Fragment key={fieldName}>
              {index > 0 ? (
                <React.Fragment>
                  <br />
                  <hr />
                </React.Fragment>
              ) : undefined}
              <Row>
                <Col md={3}>
                  <TooltipWrapper
                    message={translate.t(
                      "search_findings.tab_resources.protocol.tooltip"
                    )}
                    placement={"top"}
                  >
                    <label>
                      <label className={style.lbl}>{"* "}</label>
                      {translate.t(
                        "search_findings.tab_resources.protocol.label"
                      )}
                    </label>
                  </TooltipWrapper>
                  <Field
                    component={Dropdown}
                    name={`${fieldName}.protocol`}
                    validate={[required]}
                  >
                    <option selected={true} value={""} />
                    <option value={"HTTPS"}>
                      {translate.t("search_findings.tab_resources.https")}
                    </option>
                    <option value={"SSH"}>
                      {translate.t("search_findings.tab_resources.ssh")}
                    </option>
                  </Field>
                </Col>
                <Col md={7}>
                  <TooltipWrapper
                    message={translate.t(
                      "search_findings.tab_resources.repository.tooltip"
                    )}
                    placement={"top"}
                  >
                    <label>
                      <label className={style.lbl}>{"* "}</label>
                      {translate.t(
                        "search_findings.tab_resources.repository.label"
                      )}
                    </label>
                  </TooltipWrapper>
                  <Field
                    component={Text}
                    name={`${fieldName}.urlRepo`}
                    placeholder={translate.t(
                      "search_findings.tab_resources.base_url_placeholder"
                    )}
                    type={"text"}
                    validate={[required, validField, maxRepoUrlLength]}
                  />
                </Col>
              </Row>
              <Row>
                <Col md={5}>
                  <TooltipWrapper
                    message={translate.t(
                      "search_findings.tab_resources.branch.tooltip"
                    )}
                    placement={"top"}
                  >
                    <label>
                      <label className={style.lbl}>{"* "}</label>
                      {translate.t(
                        "search_findings.tab_resources.branch.label"
                      )}
                    </label>
                  </TooltipWrapper>
                  <Field
                    component={Text}
                    name={`${fieldName}.branch`}
                    placeholder={translate.t(
                      "search_findings.tab_resources.branch_placeholder"
                    )}
                    type={"text"}
                    validate={[required, validField, maxRepoBranchLength]}
                  />
                </Col>
                {index > 0 ? (
                  <Col className={style.removeBtn} md={2} mdOffset={5}>
                    <TooltipWrapper
                      message={translate.t(
                        "search_findings.tab_resources.modal_trash_btn.tooltip"
                      )}
                      placement={"top"}
                    >
                      <Button onClick={removeItem}>
                        <Glyphicon glyph={"trash"} />
                      </Button>
                    </TooltipWrapper>
                  </Col>
                ) : undefined}
              </Row>
            </React.Fragment>
          );
        }
      )}
      <br />
      <TooltipWrapper
        message={translate.t(
          "search_findings.tab_resources.modal_plus_btn.tooltip"
        )}
        placement={"top"}
      >
        <Button onClick={addItem}>
          <Glyphicon glyph={"plus"} />
        </Button>
      </TooltipWrapper>
    </React.Fragment>
  );
};

export { RepositoryFields };
