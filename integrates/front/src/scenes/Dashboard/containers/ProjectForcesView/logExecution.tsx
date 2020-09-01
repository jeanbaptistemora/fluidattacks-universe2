/* tslint:disable:jsx-no-multiline-js
 *
 * Disabling this rule is necessary for the sake of readability
 */

// Third parties imports
import { useQuery } from "@apollo/react-hooks";
import _ from "lodash";
import React from "react";
// tslint:disable-next-line no-submodule-imports
import SyntaxHighlighter from "react-syntax-highlighter/dist/esm/light";
// tslint:disable-next-line no-submodule-imports
import { default as monokaiSublime } from "react-syntax-highlighter/dist/esm/styles/hljs/monokai-sublime";

// Local imports
import { GET_FORCES_EXECUTION } from "./queries";

interface ILogExecutionProps {
    executionId: string;
    projectName: string;
}

const logExecution: React.FC<ILogExecutionProps> = (
    props: Readonly<ILogExecutionProps>,
): JSX.Element => {
    const { loading, data } = useQuery(GET_FORCES_EXECUTION, {
        variables: {
            executionId: props.executionId,
            projectName: props.projectName,
        },
    });
    if (loading) {

        return <React.Fragment />;
    }

    return (
        <SyntaxHighlighter style={monokaiSublime} language="yaml" wrapLines={true}>
            {data.forcesExecution.log}
        </SyntaxHighlighter>
    );
};

export { logExecution as LogExecution };
