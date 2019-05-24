import React from "react";
import { MutationFn } from "react-apollo";
import { InferableComponentEnhancer, lifecycle } from "recompose";

/**
 * Mutation to be triggered on mount event
 */
interface IMutationTriggerProps {
  onMount: MutationFn;
}

const enhance: InferableComponentEnhancer<{}> = lifecycle<IMutationTriggerProps, {}>({
  componentDidMount(): void {
    this.props.onMount()
      .catch();
  },
});

const mutationTrigger: React.ComponentClass<IMutationTriggerProps> =
  enhance((): JSX.Element => (<React.Fragment />));

export { mutationTrigger as MutationTrigger };
