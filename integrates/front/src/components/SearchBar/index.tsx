import { Form, Formik } from "formik";
import React, { useCallback } from "react";

import type { IFormValues, ISearchBarProps } from "./types";

import { Button } from "components/Button";
import { Input } from "components/Input";
import { Col, Row } from "components/Layout";

const SearchBar: React.FC<ISearchBarProps> = ({
  onSubmit,
  placeholder = "Search",
}: Readonly<ISearchBarProps>): JSX.Element => {
  const handleSubmit = useCallback(
    ({ search }: IFormValues): void => {
      onSubmit(search);
    },
    [onSubmit]
  );

  return (
    <div>
      <Formik initialValues={{ search: "" }} onSubmit={handleSubmit}>
        {({ resetForm }): JSX.Element => {
          function clear(): void {
            resetForm();
          }

          return (
            <Form>
              <Row justify={"start"} role={"searchbox"}>
                <Col lg={30} md={40} sm={60}>
                  <Input name={"search"} placeholder={placeholder} />
                </Col>
                <Col>
                  <Button onClick={clear} variant={"secondary"}>
                    {"Clear"}
                  </Button>
                </Col>
              </Row>
            </Form>
          );
        }}
      </Formik>
    </div>
  );
};

export type { ISearchBarProps };
export { SearchBar };
