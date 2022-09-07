/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint-disable fp/no-mutation, import/no-default-export, react/jsx-props-no-spreading, react/no-multi-comp */
import type { Meta, Story } from "@storybook/react";
import React, { Fragment } from "react";

import type { IAccordionProps } from ".";
import { Accordion } from ".";

const config: Meta = {
  component: Accordion,
  title: "components/Accordion",
};

const Template: Story<IAccordionProps> = (props): JSX.Element => (
  <Fragment>
    <Accordion {...props} />
    <Accordion {...props} />
  </Fragment>
);

const Default = Template.bind({});
Default.args = {
  children: (
    <div className={"pr5"}>
      <p className={"b f3 mv3"}>{"Example title"}</p>
      <p className={"f4 mv3"}>
        {`
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec
          ultricies volutpat mauris. Etiam maximus, purus sit amet imperdiet
          aliquet, diam ex fringilla dolor, bibendum tincidunt neque neque vel
          orci. Aliquam accumsan porttitor aliquet.
        `}
      </p>
      <p className={"f4 mv3"}>
        {`
          Phasellus sit amet erat velit. Fusce bibendum risus at nisl commodo
          sagittis. Ut dictum nulla vitae ipsum luctus, at elementum sapien
          tincidunt. Cras non diam feugiat augue condimentum elementum.
        `}
      </p>
      <p className={"f4 mv3"}>
        {`
          Pellentesque eget velit in dui laoreet mattis ut et magna. Aenean
          pulvinar elit lectus, in iaculis velit ullamcorper quis. Nulla
          lobortis erat in nunc porta aliquam. Donec suscipit ante id varius
          fringilla.
        `}
      </p>
      <p className={"f4 mv3"}>
        {`
          Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam
          iaculis blandit dui, quis consequat lacus venenatis malesuada. Duis
          gravida pharetra augue non placerat.
        `}
      </p>
    </div>
  ),
  header: "Example Header",
  height: "300px",
  padding: "30px 50px",
};

export { Default };
export default config;
