import type { IPaymentMethodAttr } from "./types";

const getPaymentMethodsId: (paymentMethodsData: IPaymentMethodAttr) => string =
  (paymentMethodsData: IPaymentMethodAttr): string => paymentMethodsData.id;

const getPaymentMethodsIds: (paymentMethods: IPaymentMethodAttr[]) => string[] =
  (paymentMethods: IPaymentMethodAttr[]): string[] =>
    paymentMethods.map((paymentMethodsData: IPaymentMethodAttr): string =>
      getPaymentMethodsId(paymentMethodsData)
    );

const getPaymentMethodsIndex: (
  selectedPaymentMethodsDatas: IPaymentMethodAttr[],
  allPaymentMethodsDatas: IPaymentMethodAttr[]
) => number[] = (
  selectedPaymentMethodsDatas: IPaymentMethodAttr[],
  allPaymentMethodsDatas: IPaymentMethodAttr[]
): number[] => {
  const selectPaymentMethodsIds: string[] = getPaymentMethodsIds(
    selectedPaymentMethodsDatas
  );

  return allPaymentMethodsDatas.reduce(
    (
      selectedPaymentMethodsIndex: number[],
      currentPaymentMethodsData: IPaymentMethodAttr,
      currentPaymentMethodsDataIndex: number
    ): number[] =>
      selectPaymentMethodsIds.includes(
        getPaymentMethodsId(currentPaymentMethodsData)
      )
        ? [...selectedPaymentMethodsIndex, currentPaymentMethodsDataIndex]
        : selectedPaymentMethodsIndex,
    []
  );
};

const onSelectSeveralPaymentMethodsHelper = (
  isSelect: boolean,
  paymentMethodsDatasSelected: IPaymentMethodAttr[],
  selectedPaymentMethodsDatas: IPaymentMethodAttr[],
  setSelectedPaymentMethods: (
    value: React.SetStateAction<IPaymentMethodAttr[]>
  ) => void
): string[] => {
  if (isSelect) {
    const paymentMethodsToSet: IPaymentMethodAttr[] = Array.from(
      new Set([...selectedPaymentMethodsDatas, ...paymentMethodsDatasSelected])
    );
    setSelectedPaymentMethods(paymentMethodsToSet);

    return paymentMethodsToSet.map(
      (paymentMethodsData: IPaymentMethodAttr): string =>
        getPaymentMethodsId(paymentMethodsData)
    );
  }
  const paymentMethodsIds: string[] = getPaymentMethodsIds(
    paymentMethodsDatasSelected
  );
  setSelectedPaymentMethods(
    Array.from(
      new Set(
        selectedPaymentMethodsDatas.filter(
          (selectedPaymentMethodsData: IPaymentMethodAttr): boolean =>
            !paymentMethodsIds.includes(
              getPaymentMethodsId(selectedPaymentMethodsData)
            )
        )
      )
    )
  );

  return selectedPaymentMethodsDatas.map(
    (paymentMethodsData: IPaymentMethodAttr): string =>
      getPaymentMethodsId(paymentMethodsData)
  );
};

export { getPaymentMethodsIndex, onSelectSeveralPaymentMethodsHelper };
