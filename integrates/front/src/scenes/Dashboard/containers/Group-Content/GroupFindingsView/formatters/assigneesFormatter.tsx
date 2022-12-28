import React from "react";

import { Button } from "components/Button";
import { Container } from "components/Container";
import { Dropdown } from "components/Dropdown";

export function assigneesFormatter(emails: string[]): JSX.Element {
  if (emails.length > 1) {
    return (
      <Dropdown
        button={
          <Button>
            {emails[0]}
            <b>{` +${emails.length - 1}`}</b>{" "}
          </Button>
        }
      >
        <React.Fragment>
          {emails.slice(1).map(
            (email): JSX.Element => (
              <p key={email}>{email}</p>
            )
          )}
        </React.Fragment>
      </Dropdown>
    );
  } else if (emails.length >= 1) {
    return <Button>{emails[0]}</Button>;
  }

  return (
    <Container pb={"0px"} pl={"15px"} pr={"15px"} pt={"0px"}>
      <p>{"-"}</p>
    </Container>
  );
}
