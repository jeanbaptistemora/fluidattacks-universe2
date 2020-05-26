/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for using components with render props
 */
import { useMutation, useQuery } from "@apollo/react-hooks";
import { ApolloError } from "apollo-client";
import { GraphQLError } from "graphql";
import _ from "lodash";
import mixpanel from "mixpanel-browser";
import React from "react";
import { ButtonToolbar, Col, FormGroup, Row } from "react-bootstrap";
import { useDispatch, useSelector } from "react-redux";
import { Dispatch } from "redux";
import { change, EventWithDataHandler, Field, formValueSelector, InjectedFormProps } from "redux-form";
import { Button } from "../../../../../components/Button/index";
import { DataTableNext } from "../../../../../components/DataTableNext";
import { IHeader } from "../../../../../components/DataTableNext/types";
import { handleGraphQLErrors } from "../../../../../utils/formatHelpers";
import { dropdownField, switchButton } from "../../../../../utils/forms/fields";
import { msgError, msgSuccess } from "../../../../../utils/notifications";
import rollbar from "../../../../../utils/rollbar";
import translate from "../../../../../utils/translations/translate";
import { GenericForm } from "../../../components/GenericForm";
import { EDIT_GROUP_DATA, GET_GROUP_DATA } from "../queries";

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

  // Business Logic handlers
  const handleSubscriptionTypeChange: EventWithDataHandler<React.ChangeEvent<string>> = (
    event: React.ChangeEvent<string> | undefined, subsType: string,
  ): void => {
    dispatch(change("editGroup", "drills", isContinuousType(subsType)));
    dispatch(change("editGroup", "forces", isContinuousType(subsType)));
  };
  const handleDrillsBtnChange: ((withDrills: boolean) => void) = (withDrills: boolean): void => {
    dispatch(change("editGroup", "drills", isContinuousType(formValues.type) && withDrills));

    if (!withDrills) {
      dispatch(change("editGroup", "forces", false));
    }
  };
  const handleForcesBtnChange: ((withForces: boolean) => void) = (withForces: boolean): void => {
    dispatch(change("editGroup", "forces", isContinuousType(formValues.type) && withForces));

    if (withForces) {
      dispatch(change("editGroup", "drills", true));
    }
  };

  // GraphQL Logic
  const { data, loading: loadingGroupData, refetch: refetchGroupData } = useQuery(GET_GROUP_DATA, {
    onError: (error: ApolloError): void => {
      handleGraphQLErrors("An error occurred getting group data", error);
    },
    variables: { groupName },
  });

  const [editGroupData, { loading: submittingGroupData }] = useMutation(EDIT_GROUP_DATA, {
    onCompleted: (): void => {
      mixpanel.track("EditGroupData", formValues);
      msgSuccess(
        translate.t("search_findings.services_table.success"),
        translate.t("search_findings.services_table.success_title"),
      );

      refetchGroupData({ groupName });
    },
    onError: (error: ApolloError): void => {
      error.graphQLErrors.forEach(({ message }: GraphQLError): void => {
        let msg: string;

        switch (message) {
          case "Exception - Forces is only available when Drills is too":
            msg = "search_findings.services_table.errors.forces_only_if_drills";
            break;
          case "Exception - Drills is only available in projects of type Continuous":
            msg = "search_findings.services_table.errors.drills_only_if_continuous";
            break;
          case "Exception - Forces is only available in projects of type Continuous":
            msg = "search_findings.services_table.errors.forces_only_if_continuous";
            break;
          default:
            msg = "proj_alerts.error_textsad";
            rollbar.error("An error occurred editing group services", error);
        }

        msgError(translate.t(msg));
      });
    },
  });

  if (_.isUndefined(data) || _.isEmpty(data)) {
    return <React.Fragment />;
  }

  // Action handlers
  const handleSubmit: ((values: IFormData) => void) = (values: IFormData): void => {
    editGroupData({
      variables: {
        groupName,
        hasDrills: values.drills,
        hasForces: values.forces,
        subscription: values.type,
      },
    });
  };

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
      canHave: isContinuousType(formValues.type),
      disabled: false,
      onChange: handleDrillsBtnChange,
      service: "drills",
    },
    {
      canHave: isContinuousType(formValues.type),
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
            {/* Intentionally hidden while loading/submitting to offer a better UX
              *   this way the button does not twinkle and is visually stable
              */}
            {pristine || loadingGroupData || submittingGroupData ? undefined : (
              <ButtonToolbar className="pull-right">
                <Button bsStyle="success" type="submit">
                  {translate.t("confirmmodal.proceed")}
                </Button>
              </ButtonToolbar>
            )}
            <br/>
            <br/>
          </React.Fragment>
        )}
      </GenericForm>
      <br />
    </React.StrictMode>
  );
};

export { services as Services };
