/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props and
 * conditional rendering
 */

import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Row } from "react-bootstrap";
import { RouteComponentProps } from "react-router";
import { InjectedFormProps } from "redux-form";
import { Button } from "../../../../components/Button";
import { FluidIcon } from "../../../../components/FluidIcon";
import { formatFindingDescription } from "../../../../utils/formatHelpers";
import translate from "../../../../utils/translations/translate";
import { GenericForm } from "../../components/GenericForm";
import { GET_ROLE } from "../ProjectContent/queries";
import { GET_FINDING_DESCRIPTION } from "./queries";
import { IFinding } from "./types";

type DescriptionViewProps = RouteComponentProps<{ findingId: string; projectName: string }>;

const descriptionView: React.FC<DescriptionViewProps> = (props: DescriptionViewProps): JSX.Element => {
  const { findingId, projectName } = props.match.params;
  const { userName, userOrganization } = window as typeof window & Dictionary<string>;

  // Side effects
  const onMount: (() => void) = (): void => {
    mixpanel.track("FindingDescription", { Organization: userOrganization, User: userName });
  };
  React.useEffect(onMount, []);

  // State management
  const [isEditing, setEditing] = React.useState(false);
  const toggleEdit: (() => void) = (): void => { setEditing(!isEditing); };

  // GraphQL operations
  const { data: userData } = useQuery(GET_ROLE, { variables: { projectName } });
  const userRole: string = _.isUndefined(userData) || _.isEmpty(userData)
    ? "" : userData.me.role;

  const { data } = useQuery(GET_FINDING_DESCRIPTION, {
    skip: _.isEmpty(userRole),
    variables: {
      canFetchAnalyst: _.includes(["admin", "analyst"], userRole),
      canFetchUsers: _.includes(["admin", "customeradmin"], userRole),
      findingId,
      projectName,
    },
  });

  const handleSubmit: ((values: Dictionary<string>) => void) = (): void => undefined;

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const dataset: IFinding = formatFindingDescription(data.finding);

  return (
    <React.StrictMode>
      <GenericForm
        name="editDescription"
        initialValues={dataset}
        onSubmit={handleSubmit}
      >
        {({ pristine }: InjectedFormProps): React.ReactNode => (
          <React.Fragment>
            <Row>
              <ButtonToolbar className="pull-right">
                {isEditing ? (
                  <Button type="submit" disabled={pristine}>
                    <FluidIcon icon="loading" /> {translate.t("search_findings.tab_description.update")}
                  </Button>
                ) : undefined}
                <Button bsStyle="primary" onClick={toggleEdit}>
                  <FluidIcon icon="edit" /> {translate.t("search_findings.tab_description.editable")}
                </Button>
              </ButtonToolbar>
            </Row>
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { descriptionView as DescriptionView };
