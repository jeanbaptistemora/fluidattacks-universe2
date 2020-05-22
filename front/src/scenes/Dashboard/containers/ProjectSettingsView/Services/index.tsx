/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import _ from "lodash";
import React from "react";
import { Col, FormGroup, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch } from "redux";
import { change, EventWithDataHandler, Field, formValueSelector, InjectedFormProps } from "redux-form";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { handleGraphQLErrors } from "../../../../../utils/formatHelpers";
import { dropdownField, switchButton } from "../../../../../utils/forms/fields";
import translate from "../../../../../utils/translations/translate";
import { GenericForm } from "../../../components/GenericForm";
import { GET_GROUP_DATA } from "../queries";

export interface IServicesProps {
  groupName: string;
}

export interface IServicesDataSet {
  canHave: boolean;
  disabled: boolean;
  onChange?: ((checked: boolean) => void);
  service: string;
}

export interface IFormData {
  drills: boolean;
  forces: boolean;
  integrates: boolean;
  type: string;
}

const isContinuousType: (type: string) => boolean = (type: string): boolean =>
  _.isUndefined(type) ? false : type.toLowerCase() === "continuous";

const services: React.FC<IServicesProps> = (props: IServicesProps): JSX.Element => {
  const { groupName } = props;

  // State management
  const dispatch: Dispatch = useDispatch();
  const selector: (state: {}, ...fields: string[]) => IFormData = formValueSelector("editGroup");
  const formValues: IFormData = useSelector((state: {}) => selector(state, "type", "drills", "forces", "integrates"));

  // GraphQL Logic
  const canHaveDrills: () => boolean = (): boolean => (
    isContinuousType(formValues.type)
  );
  const canHaveForces: () => boolean = (): boolean => (
    isContinuousType(formValues.type) && formValues.drills
  );

  // Business Logic handlers
  const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> = (
    event: React.ChangeEvent<string> | undefined, subsType: string,
  ): void => {
    dispatch(change("editGroup", "drills", isContinuousType(subsType)));
    dispatch(change("editGroup", "forces", isContinuousType(subsType)));
  };
  const handleDrillsBtnChange: ((withDrills: boolean) => void) = (withDrills: boolean): void => {
    dispatch(change("editGroup", "drills", canHaveDrills() && withDrills));

    if (!canHaveForces()) {
      dispatch(change("editGroup", "forces", false));
    }
  };
  const handleForcesBtnChange: ((withForces: boolean) => void) = (withForces: boolean): void => {
    dispatch(change("editGroup", "forces", canHaveForces() && withForces));
  };

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

  // Action handlers
  const handleSubmit: ((values: { }) => void) = (values: { }): void => undefined;

  // Rendered elements
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
  const servicesList: IServicesDataSet[] = [
    {
      canHave: true,
      disabled: true,
      service: "integrates",
    },
    {
      canHave: canHaveDrills(),
      disabled: false,
      onChange: handleDrillsBtnChange,
      service: "drills",
    },
    {
      canHave: canHaveForces(),
      disabled: false,
      onChange: handleForcesBtnChange,
      service: "forces",
    },
  ].filter((element: IServicesDataSet): boolean => element.canHave);

  const servicesDataSet: Array<{ [key: string]: JSX.Element }> = [
    {
      service: (
        <p>{translate.t("search_findings.services_table.type")}</p>
      ),
      status: (
        <Field
          component={dropdownField}
          name="type"
          onChange={handleSubscriptionTypeChange}
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
  ].concat(servicesList.map((element: IServicesDataSet) => ({
    service: (
      <p>{translate.t(`search_findings.services_table.${element.service}`)}</p>
    ),
    status: (
      <React.Fragment>
        <FormGroup>
          <Field
            component={switchButton}
            name={element.service}
            props={{
              disabled: element.disabled,
              offlabel: translate.t("search_findings.services_table.inactive"),
              onChange: _.isUndefined(element.onChange) ? undefined : element.onChange,
              onlabel: translate.t("search_findings.services_table.active"),
              onstyle: "danger",
              style: "btn-block",
            }}
            type="checkbox"
          />
        </FormGroup>
      </React.Fragment>
    ),
   })));

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
          drills: data.project.hasDrills,
          forces: data.project.hasForces,
          integrates: true,
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
      <br />
    </React.StrictMode>
  );
};

export { services as Services };
