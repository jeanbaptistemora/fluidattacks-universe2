import React from "react";

import { Text } from "../../../../components/Typography";
import type { ITextProps } from "../../../../components/Typography";

const Paragraph: React.FC<ITextProps> = ({ children }): JSX.Element => (
  <Text color={"#535365"} mb={3} mt={3} size={"medium"}>
    {children}
  </Text>
);

export { Paragraph };
