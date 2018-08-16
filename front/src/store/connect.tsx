/* tslint:disable:no-any
 * Disabling here is necessary because this is a generic wrapper
 * and will receive React components with different types of props
*/
import React from "react";
import { connect } from "react-redux";
import store from "./index";

type ComponentMapping = ((
  arg1: React.StatelessComponent<any>,
  arg2: any,
  arg3: any) => React.StatelessComponent<any>);

const connectWithStore: ComponentMapping =
  (wrappedComponent: React.StatelessComponent<any>,
   mapStateToProps: any,
   mapDispatchToProps: any,
  ): React.StatelessComponent<any> => {

  /* tslint:disable-next-line:variable-name
   * Disabling here is necessary due a conflict
   * between lowerCamelCase var naming rule from tslint
   * and PascalCase rule for naming JSX elements
   */
  const ReduxWrapper: React.ComponentClass =
    connect(mapStateToProps, mapDispatchToProps)(wrappedComponent);

  return (props: any): JSX.Element => (
    <ReduxWrapper {...props} store={store}/>
  );
};

export = connectWithStore;
