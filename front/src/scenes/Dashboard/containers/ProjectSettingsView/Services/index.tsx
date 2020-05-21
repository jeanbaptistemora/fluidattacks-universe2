/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { Col, Row } from "react-bootstrap";
import { Field, InjectedFormProps } from "redux-form";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { handleGraphQLErrors } from "../../../../../utils/formatHelpers";
import { dropdownField } from "../../../../../utils/forms/fields";
import translate from "../../../../../utils/translations/translate";
import { GenericForm } from "../../../components/GenericForm";
import { GET_GROUP_DATA } from "../queries";

export interface IServicesProps {
  groupName: string;
}

export interface IServicesDataSet {
  canHave: boolean;
  checked: boolean;
  disabled: boolean;
  onChange: ((checked: boolean) => void);
  service: string;
}

export interface IFormData {
  type: string;
}

const services: React.FC<IServicesProps> = (props: IServicesProps): JSX.Element => {
  const { groupName } = props;

  // GraphQL Logic
  const { data } = useQuery(GET_GROUP_DATA, {
    onError: (error: ApolloError): void => {
      handleGraphQLErrors("An error occurred getting group data", error);
    },
    variables: { groupName },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  const handleSubmit: ((values: { }) => void) = (values: { }): void => undefined;

  const tableHeaders: IHeader[] = [
    {
      dataField: "service",
      header: translate.t("search_findings.services_table.service"),
      width: "75%",
      wrapped: true,
    },
    {
      dataField: "status",
      header: translate.t("search_findings.services_table.status"),
      width: "25%",
      wrapped: true,
    },
  ];

  const servicesDataSet: Array<{ [key: string]: JSX.Element }> = [
    {
      service: (
        <p>{translate.t("search_findings.services_table.type")}</p>
      ),
      status: (
        <Field
          component={dropdownField}
          name="type"
        >
          <option value="CONTINUOUS">
            {translate.t("search_findings.services_table.continuous")}
          </option>
          <option value="ONESHOT">
            {translate.t("search_findings.services_table.one_shot")}
          </option>
        </Field>
      ),
    },
  ];

  return (
    <React.StrictMode>
      <Row>
        <Col lg={8} md={10} xs={7}>
          <h3>{translate.t("search_findings.services_table.services")}</h3>
        </Col>
      </Row>
      <GenericForm
        name="editGroup"
        onSubmit={handleSubmit}
        initialValues={{
          type: data.project.subscription.toUpperCase(),
        }}
      >
        {({ pristine }: InjectedFormProps): JSX.Element => (
          <React.Fragment>
            <DataTableNext
              bordered={true}
              dataset={servicesDataSet}
              exportCsv={false}
              search={false}
              headers={tableHeaders}
              id="tblServices"
              pageSize={5}
              remote={false}
              striped={true}
            />
          </React.Fragment>
        )}
      </GenericForm>
    </React.StrictMode>
  );
};

export { services as Services };
