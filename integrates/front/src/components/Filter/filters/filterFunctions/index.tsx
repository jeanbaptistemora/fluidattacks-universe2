import type {
  IPermanentData,
  IPermanentValuesProps,
} from "components/Filter/types";

const setPermanentValues = ({
  permaValue,
  permaValues,
  setPermaValues,
}: IPermanentValuesProps): void => {
  setPermaValues?.(
    permaValues.map((permadata): IPermanentData => {
      if (permadata.id === permaValue.id) {
        return {
          ...permadata,
          checkValues: permaValue.checkValues,
          rangeValues: permaValue.rangeValues,
          value: permaValue.value,
        };
      }

      return permadata;
    })
  );
};

export { setPermanentValues };
