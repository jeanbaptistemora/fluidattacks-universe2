import { faMagnifyingGlass } from "@fortawesome/free-solid-svg-icons";
import { Form, Formik } from "formik";
import React, { useCallback } from "react";

import type { IFormValues, ISearchBarProps } from "./types";

import { Button } from "components/Button";
import { Input } from "components/Input";

const SearchBar: React.FC<ISearchBarProps> = ({
  onSubmit,
  placeholder = "Search...",
}: Readonly<ISearchBarProps>): JSX.Element => {
  const handleSubmit = useCallback(
    ({ search }: IFormValues): void => {
      onSubmit(search);
    },
    [onSubmit]
  );

  return (
    <Formik initialValues={{ search: "" }} onSubmit={handleSubmit}>
      <Form>
        <Input
          childLeft={
            <Button icon={faMagnifyingGlass} size={"xs"} type={"submit"} />
          }
          name={"search"}
          placeholder={placeholder}
        />
      </Form>
    </Formik>
  );
};

export type { ISearchBarProps };
export { SearchBar };
