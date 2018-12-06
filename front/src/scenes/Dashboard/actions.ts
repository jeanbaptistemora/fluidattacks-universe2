/* tslint:disable:no-any
 * Disabling this rule is necessary because the payload type may differ between
 * actions
 */
import { AxiosError, AxiosResponse } from "axios";
import { Action, AnyAction, Dispatch } from "redux";
import { reset } from "redux-form";
import { ThunkAction, ThunkDispatch } from "redux-thunk";
import { formatUserlist } from "../../utils/formatHelpers";
import { msgError, msgSuccess } from "../../utils/notifications";
import rollbar from "../../utils/rollbar";
import translate from "../../utils/translations/translate";
import Xhr from "../../utils/xhr";
import * as actionType from "./actionTypes";
import { IProjectUsersViewProps, IUserData } from "./components/ProjectUsersView/index";
import { IRecordsViewProps } from "./components/RecordsView";
import { IResourcesViewProps } from "./components/ResourcesView";
import { ISeverityViewProps } from "./components/SeverityView";

export interface IActionStructure {
  payload: any;
  type: string;
}

type DashboardAction = ((...args: any[]) => IActionStructure);
type ThunkDispatcher = Dispatch<Action> & ThunkDispatch<{}, {}, AnyAction>;
type ThunkActionStructure = ((...args: any[]) => ThunkAction<void, {}, {}, AnyAction>);

export const removeRepo: ThunkActionStructure =
  (projectName: string, repository: string, branch: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      removeRepositories (
        repositoryData: ${JSON.stringify(JSON.stringify({ urlRepo: repository, branch }))},
        projectName: "${projectName}"
      ) {
        success
        resources {
          environments
          repositories
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred removing repositories")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      if (data.removeRepositories.success) {
        dispatch({
          payload: {
            environments: JSON.parse(data.removeRepositories.resources.environments),
            repositories: JSON.parse(data.removeRepositories.resources.repositories),
          },
          type: actionType.LOAD_RESOURCES,
        });
        msgSuccess(
          translate.t("search_findings.tab_resources.success_remove"),
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error("An error occurred removing repositories");
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const removeEnv: ThunkActionStructure =
  (projectName: string, envToRemove: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      removeEnvironments (
        repositoryData: ${JSON.stringify(JSON.stringify({ urlEnv: envToRemove }))},
        projectName: "${projectName}"
      ) {
        success
        resources {
          environments
          repositories
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred removing environments")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      if (data.removeEnvironments.success) {
        dispatch({
          payload: {
            environments: JSON.parse(data.removeEnvironments.resources.environments),
            repositories: JSON.parse(data.removeEnvironments.resources.repositories),
          },
          type: actionType.LOAD_RESOURCES,
        });
        msgSuccess(
          translate.t("search_findings.tab_resources.success_remove"),
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error("An error occurred removing environments");
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const clearResources: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_RESOURCES,
});

export const loadResources: ThunkActionStructure =
  (projectName: IResourcesViewProps["projectName"]): ThunkAction<void, {}, {}, Action> =>
  (dispatch: ThunkDispatcher): void => {
    dispatch(clearResources());
    let gQry: string;
    gQry = `{
        resources (projectName: "${projectName}") {
          environments
          repositories
        }
    }`;
    new Xhr().request(gQry, "An error occurred getting repositories")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      dispatch({
        payload: {
          environments: JSON.parse(data.resources.environments),
          repositories: JSON.parse(data.resources.repositories),
        },
        type: actionType.LOAD_RESOURCES,
      });
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const addRepositoryField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_REPO_FIELD,
});

export const removeRepositoryField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_REPO_FIELD,
});

export const addEnvironmentField: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.ADD_ENV_FIELD,
});

export const removeEnvironmentField: DashboardAction =
  (index: number): IActionStructure => ({
      payload: { index },
      type: actionType.REMOVE_ENV_FIELD,
});

export const openAddModal: DashboardAction =
  (type: "repository" | "environment"): IActionStructure => ({
      payload: { type },
      type: actionType.OPEN_ADD_MODAL,
});

export const closeAddModal: DashboardAction =
  (): IActionStructure => ({
      payload: undefined,
      type: actionType.CLOSE_ADD_MODAL,
});

export const saveRepos: ThunkActionStructure =
  (projectName: string, reposData: IResourcesViewProps["addModal"]["repoFields"],
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      addRepositories (
        resourcesData: ${JSON.stringify(JSON.stringify(reposData))},
        projectName: "${projectName}") {
        success
        resources {
          environments
          repositories
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred adding repositories")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      if (data.addRepositories.success) {
        dispatch(closeAddModal());
        dispatch({
          payload: {
            environments: JSON.parse(data.addRepositories.resources.environments),
            repositories: JSON.parse(data.addRepositories.resources.repositories),
          },
          type: actionType.LOAD_RESOURCES,
        });
        msgSuccess(
          translate.t("search_findings.tab_resources.success"),
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error("An error occurred adding repositories");
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const saveEnvs: ThunkActionStructure =
  (projectName: string,
   envsData: IResourcesViewProps["addModal"]["envFields"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      addEnvironments (
        resourcesData: ${JSON.stringify(JSON.stringify(envsData))},
        projectName: "${projectName}") {
        success
        resources {
          environments
          repositories
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred adding environments")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      if (data.addEnvironments.success) {
      dispatch(closeAddModal());
      dispatch({
          payload: {
            environments: JSON.parse(data.addEnvironments.resources.environments),
            repositories: JSON.parse(data.addEnvironments.resources.repositories),
          },
          type: actionType.LOAD_RESOURCES,
        });
      msgSuccess(
          translate.t("search_findings.tab_resources.success"),
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error("An error occurred adding repositories");
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const modifyRepoUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_URL,
});

export const modifyRepoBranch: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_REPO_BRANCH,
});

export const modifyEnvUrl: DashboardAction =
  (index: number, newValue: string): IActionStructure => ({
      payload: {
        index,
        newValue,
      },
      type: actionType.MODIFY_ENV_URL,
});

export const addFileName: DashboardAction =
  (newValue: string): IActionStructure => ({
      payload: {
        newValue,
      },
      type: actionType.ADD_FILE_NAME,
});

export const clearUsers: DashboardAction =
  (): IActionStructure => ({
  payload: undefined,
  type: actionType.CLEAR_USERS,
});

export const loadUsers: ThunkActionStructure =
  (
    projectName: IProjectUsersViewProps["projectName"],
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    dispatch(clearUsers());
    let gQry: string;
    gQry = `{
      projectUsers(projectName:"${projectName}"){
        email
        role
        responsability
        phoneNumber
        organization
        firstLogin
        lastLogin
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting project users")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      dispatch({
          payload: { userlist: formatUserlist(data.projectUsers) },
          type: actionType.LOAD_USERS,
      });
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const removeUser: ThunkActionStructure =
  (
    projectName: IProjectUsersViewProps["projectName"],
    email: IUserData["email"],
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      removeUserAccess(projectName: "${projectName}", userEmail: "${email}"){
        removedEmail
        success
      }
    }`;
    new Xhr().request(gQry, "An error occurred removing users")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.removeUserAccess.success) {
        const removedEmail: string = data.removeUserAccess.removedEmail;

        dispatch({
          payload: { removedEmail },
          type: actionType.REMOVE_USER,
        });
        msgSuccess(
          `${email} ${translate.t("search_findings.tab_users.success_delete")}`,
          translate.t("search_findings.tab_users.title_success"),
        );
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const openUsersMdl: DashboardAction =
  (type: "add" | "edit", initialValues?: {}): IActionStructure => ({
    payload: { type, initialValues },
    type: actionType.OPEN_USERS_MDL,
});

export const closeUsersMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_USERS_MDL,
});

export const addUser: ThunkActionStructure =
 (
   newUser: IUserData,
   projectName: IProjectUsersViewProps["projectName"],
 ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
   let gQry: string;
   gQry = `mutation {
     grantUserAccess(
       email: "${newUser.email}",
       organization: "${newUser.organization}",
       phoneNumber: "${newUser.phone}",
       projectName: "${projectName}",
       responsibility: "${newUser.responsability}",
       role: "${newUser.role}"
     ) {
       success
       grantedUser {
         email
         role
         responsability
         phoneNumber
         organization
         firstLogin
         lastLogin
       }
     }
   }`;
   new Xhr().request(gQry, "An error occurred adding user to project")
   .then((response: AxiosResponse) => {
     const { data } = response.data;

     if (data.grantUserAccess.success) {
       msgSuccess(
         `${newUser.email}${translate.t("search_findings.tab_users.success")}`,
         translate.t("search_findings.tab_users.title_success"),
       );
       dispatch(reset("addUser"));
       dispatch(closeUsersMdl());
       dispatch({
         payload: { newUser: formatUserlist([data.grantUserAccess.grantedUser])[0] },
         type: actionType.ADD_USER,
       });
     } else {
       msgError(translate.t("proj_alerts.error_textsad"));
     }
   })
   .catch((error: AxiosError) => {
     if (error.response !== undefined) {
       const { errors } = error.response.data;

       msgError(translate.t("proj_alerts.error_textsad"));
       rollbar.error(error.message, errors);
     }
   });
};

export const loadVulnerabilities: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        id
        success
        errorMessage
        portsVulns: vulnerabilities(
          vulnType: "ports") {
          ...vulnInfo
        }
        linesVulns: vulnerabilities(
          vulnType: "lines") {
          ...vulnInfo
        }
        inputsVulns: vulnerabilities(
          vulnType: "inputs") {
          ...vulnInfo
        }
      }
    }
    fragment vulnInfo on Vulnerability {
      vulnType
      where
      specific
      currentState
      id
      findingId
    }`;
    new Xhr().request(gQry, "An error occurred getting vulnerabilities")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.finding.success) {
        dispatch({
          payload: {
            dataInputs: data.finding.inputsVulns,
            dataLines: data.finding.linesVulns,
            dataPorts: data.finding.portsVulns,
          },
          type: actionType.LOAD_VULNERABILITIES,
        });
      } else if (data.finding.errorMessage === "Error in file") {
        msgError(translate.t("search_findings.tab_description.errorFileVuln"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const deleteVulnerability: ThunkActionStructure =
  (vulnInfo: { [key: string]: string }): ThunkAction<void, {}, {}, Action> =>
    (_: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      deleteVulnerability(id: "${vulnInfo.id}", findingId: "${vulnInfo.findingId}"){
        success
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting vulnerabilities")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.deleteVulnerability.success) {
        msgSuccess(
          translate.t("search_findings.tab_description.vulnDeleted"),
          translate.t("proj_alerts.title_success"));
        location.reload();
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const editUser: ThunkActionStructure =
 (
   modifiedUser: IUserData,
   projectName: IProjectUsersViewProps["projectName"],
 ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
   let gQry: string;
   gQry = `mutation {
     editUser(
       projectName: "${projectName}",
       email: "${modifiedUser.email}",
       organization: "${modifiedUser.organization}",
       phoneNumber: "${modifiedUser.phone}",
       responsibility: "${modifiedUser.responsability}",
       role: "${modifiedUser.role}"
     ) {
       success
     }
   }`;
   new Xhr().request(gQry, "An error occurred editing user information")
   .then((response: AxiosResponse) => {
     const { data } = response.data;

     if (data.editUser.success) {
       msgSuccess(
         translate.t("search_findings.tab_users.success_admin"),
         translate.t("search_findings.tab_users.title_success"),
       );
       dispatch(reset("addUser"));
       dispatch(closeUsersMdl());
       location.reload();
     } else {
       msgError(translate.t("proj_alerts.error_textsad"));
     }
   })
   .catch((error: AxiosError) => {
     if (error.response !== undefined) {
       const { errors } = error.response.data;

       msgError(translate.t("proj_alerts.error_textsad"));
       rollbar.error(error.message, errors);
     }
   });
};

export const loadRecords: ThunkActionStructure =
(
  findingId: IRecordsViewProps["findingId"],
): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `{
    finding(identifier: "${findingId}") {
      records
    }
  }`;
  new Xhr().request(gQry, "An error occurred getting compromised records")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    dispatch({
      payload: { records: JSON.parse(data.finding.records) },
      type: actionType.LOAD_RECORDS,
    });
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      msgError("There was an error :(");
      rollbar.error(error.message, errors);
    }
  });
};

export const editRecords: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_RECORDS,
});

export const updateRecords: ThunkActionStructure =
  (
    findingId: string, projectName: string,
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `mutation {
    updateEvidence (
      id: "8",
      findingId: "${findingId}",
      projectName: "${projectName}") {
      success
      finding {
        records
      }
    }
  }`;
  new Xhr().upload(gQry, "#evidence8", "An error occurred updating records")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    if (data.updateEvidence.success) {
      dispatch({
        payload: { records: JSON.parse(data.updateEvidence.finding.records) },
        type: actionType.LOAD_RECORDS,
      });
      msgSuccess(
        translate.t("proj_alerts.file_updated"),
        translate.t("search_findings.tab_users.title_success"),
      );
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
    }
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      switch (errors[0].message) {
        case "File exceeds the size limits":
          msgError(translate.t("proj_alerts.file_size"));
          break;
        case "Extension not allowed":
          msgError(translate.t("proj_alerts.file_type_wrong"));
          break;
        default:
          msgError(translate.t("proj_alerts.no_file_update"));
          rollbar.error(error.message, errors);
      }

    }
  });
};

export const loadTracking: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        success
        tracking
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting tracking")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.finding.success) {
        dispatch({
          payload: {
            closings: data.finding.tracking,
          },
          type: actionType.LOAD_TRACKING,
        });
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const editSeverity: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_SEVERITY,
  });

export const calcCVSSv2: DashboardAction =
  (data: ISeverityViewProps["dataset"]): IActionStructure => {
    let BASESCORE_FACTOR_1: number; BASESCORE_FACTOR_1 = 0.6;
    let BASESCORE_FACTOR_2: number; BASESCORE_FACTOR_2 = 0.4;
    let BASESCORE_FACTOR_3: number; BASESCORE_FACTOR_3 = 1.5;
    let IMPACT_FACTOR: number; IMPACT_FACTOR = 10.41;
    let EXPLOITABILITY_FACTOR: number; EXPLOITABILITY_FACTOR = 20;
    let F_IMPACT_FACTOR: number; F_IMPACT_FACTOR = 1.176;

    const impCon: number = parseFloat(data.confidentialityImpact);
    const impInt: number = parseFloat(data.integrityImpact);
    const impDis: number = parseFloat(data.availabilityImpact);
    const accCom: number = parseFloat(data.accessComplexity);
    const accVec: number = parseFloat(data.accessVector);
    const auth: number = parseFloat(data.authentication);
    const explo: number = parseFloat(data.exploitability);
    const resol: number = parseFloat(data.resolutionLevel);
    const confi: number = parseFloat(data.confidenceLevel);

    /*
     * The constants above are part of the BaseScore, Impact and
     * Exploibility equations
     * More information in https://www.first.org/cvss/v2/guide
     */
    const impact: number = IMPACT_FACTOR * (1 - ((1 - impCon) * (1 - impInt) * (1 - impDis)));
    const exploitabilty: number = EXPLOITABILITY_FACTOR * accCom * auth * accVec;
    const baseScore: number = ((BASESCORE_FACTOR_1 * impact) + (BASESCORE_FACTOR_2 * exploitabilty)
                              - BASESCORE_FACTOR_3) * F_IMPACT_FACTOR;
    const temporal: number = baseScore * explo * resol * confi;

    return ({
      payload: {
        baseScore: baseScore.toFixed(1),
        temporal: temporal.toFixed(1),
      },
      type: actionType.CALC_CVSSV2,
    });
  };

export const loadSeverity: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        severity
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting severity")
    .then((response: AxiosResponse) => {
      const { data } = response.data;
      dispatch(calcCVSSv2(data.finding.severity));
      dispatch({
        payload: {
          dataset: data.finding.severity,
        },
        type: actionType.LOAD_SEVERITY,
      });
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const openConfirmMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.OPEN_CONFIRM_MDL,
});

export const closeConfirmMdl: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_CONFIRM_MDL,
});

export const updateSeverity: ThunkActionStructure =
  (findingId: string, values: ISeverityViewProps["dataset"],
   criticity: ISeverityViewProps["criticity"]): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `mutation {
      updateSeverity(
        findingId: "${findingId}",
        data: {
          accessComplexity: "${values.accessComplexity}",
          accessVector: "${values.accessVector}",
          authentication: "${values.authentication}",
          availabilityImpact: "${values.availabilityImpact}",
          confidenceLevel: "${values.confidenceLevel}",
          confidentialityImpact: "${values.confidentialityImpact}",
          criticity: "${criticity}",
          exploitability: "${values.exploitability}",
          id: "${findingId}",
          integrityImpact: "${values.integrityImpact}",
          resolutionLevel: "${values.resolutionLevel}",
        }
      ) {
        success
        finding {
          severity
        }
      }
    }`;
    new Xhr().request(gQry, "An error occurred updating severity")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      if (data.updateSeverity.success) {
        dispatch(calcCVSSv2(data.updateSeverity.finding.severity));
        dispatch({
          payload: {
            dataset: data.updateSeverity.finding.severity,
          },
          type: actionType.LOAD_SEVERITY,
        });
        dispatch(editSeverity());
        dispatch(closeConfirmMdl());
      } else {
        msgError(translate.t("proj_alerts.error_textsad"));
      }
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const loadExploit: ThunkActionStructure =
  (findingId: string): ThunkAction<void, {}, {}, Action> =>
    (dispatch: ThunkDispatcher): void => {
    let gQry: string;
    gQry = `{
      finding(identifier: "${findingId}") {
        exploit
      }
    }`;
    new Xhr().request(gQry, "An error occurred getting exploit")
    .then((response: AxiosResponse) => {
      const { data } = response.data;

      dispatch({
        payload: {
          code: data.finding.exploit,
        },
        type: actionType.LOAD_EXPLOIT,
      });
    })
    .catch((error: AxiosError) => {
      if (error.response !== undefined) {
        const { errors } = error.response.data;

        msgError(translate.t("proj_alerts.error_textsad"));
        rollbar.error(error.message, errors);
      }
    });
};

export const editExploit: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.EDIT_EXPLOIT,
  });

export const updateExploit: ThunkActionStructure =
  (
    findingId: string, projectName: string,
  ): ThunkAction<void, {}, {}, Action> => (dispatch: ThunkDispatcher): void => {
  let gQry: string;
  gQry = `mutation {
    updateEvidence (
      id: "7",
      findingId: "${findingId}",
      projectName: "${projectName}") {
      success
      finding {
        exploit
      }
    }
  }`;
  new Xhr().upload(gQry, "#evidence7", "An error occurred updating exploit")
  .then((response: AxiosResponse) => {
    const { data } = response.data;
    if (data.updateEvidence.success) {
      dispatch({
        payload: { code: data.updateEvidence.finding.exploit },
        type: actionType.LOAD_EXPLOIT,
      });
      msgSuccess(
        translate.t("proj_alerts.file_updated"),
        translate.t("search_findings.tab_users.title_success"),
      );
    } else {
      msgError(translate.t("proj_alerts.error_textsad"));
    }
  })
  .catch((error: AxiosError) => {
    if (error.response !== undefined) {
      const { errors } = error.response.data;

      switch (errors[0].message) {
        case "File exceeds the size limits":
          msgError(translate.t("proj_alerts.file_size"));
          break;
        case "Extension not allowed":
          msgError(translate.t("proj_alerts.file_type_wrong"));
          break;
        default:
          msgError(translate.t("proj_alerts.no_file_update"));
          rollbar.error(error.message, errors);
      }
    }
  });
};

export const openEvidence: DashboardAction =
  (imgIndex: number): IActionStructure => ({
    payload: { imgIndex },
    type: actionType.OPEN_EVIDENCE,
  });

export const closeEvidence: DashboardAction =
  (): IActionStructure => ({
    payload: undefined,
    type: actionType.CLOSE_EVIDENCE,
  });

export const moveEvidenceIndex: DashboardAction =
  (currentIndex: number, totalImages: number, direction: "next" | "previous"): IActionStructure => ({
    payload: {
      index: (direction === "next" ? (currentIndex + 1) : (currentIndex + totalImages - 1))
        % totalImages,
    },
    type: actionType.MOVE_EVIDENCE,
  });
