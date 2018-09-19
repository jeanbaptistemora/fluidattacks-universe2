/* tslint:disable no-any
 * Disabling this rule is necessary to use the gritter notification
 * plugin, which (for now) is only available for JQuery
 */
declare var $: any;
// tslint:enable no-any

export const msgSuccess: ((arg1: string, arg2: string) => void) =
(text: string, title: string): void => {
  $.gritter.add({
    class_name: "color info",
    sticky: false,
    text,
    title,
  });
};

export const msgError: ((arg1: string, arg2?: string | undefined) => void) =
  (text: string, title: string = "Oops!"): void => {
  $.gritter.add({
    class_name: "color danger",
    sticky: false,
    text,
    title,
  });
};

export const msgInfo: ((arg1: string, arg2: string) => void) =
  (text: string, title: string): void => {
  $.gritter.add({
    class_name: "color info",
    sticky: false,
    text,
    title,
  });
};

export const msgWarning: ((arg1: string, arg2: string) => void) =
  (text: string, title: string): void => {
  $.gritter.add({
    class_name: "color warning",
    sticky: false,
    text,
    title,
  });
};
