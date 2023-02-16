import type { ApolloError } from "@apollo/client";
import { useQuery } from "@apollo/client";
import type { Dayjs } from "dayjs";
import { Formik } from "formik";
import type { GraphQLError } from "graphql";
import React, { useCallback, useMemo } from "react";
import { useTranslation } from "react-i18next";
import { array, object, string } from "yup";

import { AddModalForm } from "./form";

import { GET_ROOTS } from "../../GroupScopeView/queries";
import type { Root } from "../../GroupScopeView/types";
import { Modal } from "components/Modal";
import { Logger } from "utils/logger";

interface IFormValues {
  eventDate: Dayjs | string;
  affectsReattacks: boolean;
  affectedReattacks: string[];
  eventType: string;
  detail: string;
  files?: FileList;
  images?: FileList;
  rootId: string;
  rootNickname: string;
}

interface IAddModalProps {
  groupName: string;
  organizationName: string;
  onClose: () => void;
  onSubmit: (values: IFormValues) => Promise<void>;
}

const AddModal: React.FC<IAddModalProps> = ({
  organizationName,
  groupName,
  onClose,
  onSubmit,
}: IAddModalProps): JSX.Element => {
  const { t } = useTranslation();

  const { data } = useQuery<{ group: { roots: Root[] } }>(GET_ROOTS, {
    onError: ({ graphQLErrors }: ApolloError): void => {
      graphQLErrors.forEach((error: GraphQLError): void => {
        Logger.error("Couldn't load roots", error);
      });
    },
    variables: { groupName },
  });

  const roots = useMemo(
    (): Root[] =>
      data === undefined
        ? []
        : data.group.roots.filter((root): boolean => root.state === "ACTIVE"),
    [data]
  );

  const nicknames = roots.map((root): string => root.nickname);

  const handleSubmit = useCallback(
    async (values: IFormValues): Promise<void> => {
      return onSubmit({
        ...values,
        rootId: values.rootNickname
          ? roots[nicknames.indexOf(values.rootNickname)].id
          : "",
      });
    },
    [nicknames, onSubmit, roots]
  );

  const validations = object().shape({
    affectedReattacks: array().when("affectsReattacks", {
      is: true,
      otherwise: array().notRequired(),
      then: array().min(1, t("validations.someRequired")),
    }),
    rootNickname: string()
      .oneOf(nicknames, t("validations.oneOf"))
      .when("eventType", {
        is: "MISSING_SUPPLIES",
        otherwise: string().required(),
        then: string().notRequired(),
      }),
  });

  return (
    <Modal onClose={onClose} open={true} title={t("group.events.new")}>
      <Formik
        initialValues={{
          affectedReattacks: [],
          affectsReattacks: false,
          detail: "",
          eventDate: "",
          eventType: "",
          files: undefined,
          images: undefined,
          rootId: "",
          rootNickname: "",
        }}
        name={"newEvent"}
        onSubmit={handleSubmit}
        validationSchema={validations}
      >
        {({ dirty, isSubmitting, values, setFieldValue }): JSX.Element => {
          return (
            <AddModalForm
              dirty={dirty}
              groupName={groupName}
              isSubmitting={isSubmitting}
              nicknames={nicknames}
              onClose={onClose}
              organizationName={organizationName}
              setFieldValue={setFieldValue}
              values={values}
            />
          );
        }}
      </Formik>
    </Modal>
  );
};

export type { IFormValues };
export { AddModal };
