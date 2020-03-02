import { default as $ } from "jquery";

const contentHome: (() => void) = (): void => {
  $(() => {
    $('input:radio[name="menu1"]')
      .on("change", (event: JQuery.ChangeEvent) => {
        if ($("#op1")
            .prop("checked")) {
          $(".fixes")
            .toggleClass("dn fadein");
          $(".skims, .drills, .forces")
            .addClass("dn");
          $(".skims, .drills, .forces")
          .removeClass("fadein active");
        }

        if ($("#op2")
            .prop("checked")) {
          $(".skims")
            .toggleClass("dn fadein active");
          $(".fixes, .drills, .forces")
            .addClass("dn");
          $(".fixes, .drills, .forces")
            .removeClass("fadein active");
        }
        if ($("#op3")
            .prop("checked")) {
          $(".drills")
            .toggleClass("dn fadein active");
          $(".fixes, .skims, .forces")
            .addClass("dn");
          $(".fixes, .skims, .forces")
            .removeClass("fadein active");
        }
        if ($("#op4")
            .prop("checked")) {
          $(".forces")
            .toggleClass("dn fadein active");
          $(".fixes, .skims, .drills")
            .addClass("dn");
          $(".fixes, .skims, .drills")
            .removeClass("fadein active");
        }
    });
  });
};

contentHome();
