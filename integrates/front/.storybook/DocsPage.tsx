import {
  ArgsTable,
  Description,
  DocsContext,
  PRIMARY_STORY,
  Primary,
  Source,
  Stories,
  Subtitle,
  Title,
} from "@storybook/addon-docs";
import React, { useContext } from "react";

const ImportPath = (): JSX.Element => {
  const context = useContext(DocsContext);
  const titleParts = context.title.split("/");
  const componentName = titleParts[titleParts.length - 1];
  const path = `import { ${componentName} } from "components/${componentName}"`;

  return <Source dark={true} language={"js"} code={path} />;
};

const DocsPage = (): JSX.Element => (
  <React.Fragment>
    <Title />
    <Subtitle />
    <Description />
    <ImportPath />
    <Primary />
    <ArgsTable story={PRIMARY_STORY} />
    <Stories />
  </React.Fragment>
);

export { DocsPage };
