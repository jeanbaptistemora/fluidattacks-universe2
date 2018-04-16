/* eslint no-magic-numbers: ["error", { "ignore": [-1,0,0.950,1,2,5] }]*/
/* global document, $, alertify, setInterval, timew, Tabletop, v:true, obj:true, $msg */
let remember = null;
$(document).ready(function ready () {
  remember = function () {
    try {
      alertify.log("<div class=\"\" style=\"padding: 8px;\"><p class=\"text-center\">Recordatorio</p><p class=\"text-left\"> Recuerda personalizar los campos dependiendo de la situación que vas a reportar!</p> </div>");
    }
    catch (err) {
      return false;
    }
  };
  remember();
  const timew = 35000;
  setInterval(function setInterval () {
    remember();
  }, timew);
  document.getElementsByTagName("select")[5].onchange = function onchange () {
    const verf = document.getElementsByTagName("select")[5].value;
    if (verf == "Verificación") {
      alertify.success("<p class=\"text-center\"> Información: </p> <p class=\"text-left\"> Verificacion debe usarse para reportar hallazgos en chequeos cruzados </p>");
    }
  };
});

/**
 * Function isUpperCase return input string in uppercase
 */
function isUpperCase (str) {
  return str === str.toUpperCase();
}

String.prototype.capitalizeFirstLetter = function capitalizeFirstLetter () { /* eslint no-extend-native: ["error", { "exceptions": ["String"] }]*/
  return this.charAt(0).toUpperCase() + this.slice(1);
};

const description = $("#field32202728");
const requirement = $("#field38254586");
const solution = $("#field38619077");
const threat = $("#field38193361");
const risk = $("#field38193362");
const donde = $("#field38193357");
const hasSolution = $("#field38861717_1");
const hasNoSolution = $("#field38861717_2");
const solutionKb = $("#field38861739");
const tipo = $("#field54319180");
const debilidad = $("#field38899046");
const solutionPdf = $("#field38307753");
const evidenciaHallazgo = $("#field32202896");
const exploit = $("#field38307199");
const evidenciaExplotacion = $("#field38307222");
const animacion = $("#field38307272");
const siEvidente = $("#field49132420_1");
const noEvidente = $("#field49132420_2");
const publicSpreadsheetUrl = "https://docs.google.com/spreadsheets/d/1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc/pubhtml";

/**
 * Function showInfo return info about findings
 */
function showInfo (data, tabletop) {
  const obj = $.parseJSON(JSON.stringify(data));
  $("#field32201810").change(function change () {
    const title = $("#field32201810").val();
    for (let cont = 0; cont < obj.length; cont++) {
      if (obj[cont].Titulo == title) {
        description.val(obj[cont].Descripcion);
        requirement.val(obj[cont].Requisito);
        solution.val(obj[cont].Recomendacion);
        donde.attr("placeholder", obj[cont].Donde);
        debilidad.val(obj[cont].CWE.split("/")[5].split(".")[0]);
        tipo.val(obj[cont].Tipo);
        if (obj[cont].Evidente == "Sí") {
          siEvidente.attr("checked", true);
        }
        else {
          noEvidente.attr("checked", true);
        }
        if (obj[cont].Solucion_KB != "-") {
          hasSolution.attr("checked", true);
          $("#fsCell38861739").removeClass("fsHidden");
          $("#fsCell38307753").removeClass("fsHidden");
          solutionPdf.removeAttr("disabled");
          solutionKb.val(obj[cont].Solucion_KB);
        }
        else if (obj[cont].Solucion_KB == "-") {
          hasNoSolution.attr("checked", true);
          $("#fsCell38861739").addClass("fsHidden");
          $("#fsCell38307753").addClass("fsHidden");
          solutionPdf.attr("disabled");
        }

        if ($("#field38392454").val() == "Detallado") {
          threat.val(obj[cont].Amenaza);
          risk.val(obj[cont].Riesgo);
        }

        // If(obj[cont].Exploit == "Sí"){
        if ($("#field38529253").val() == 0.950) {
          exploit.prop("required", true);
          exploit.addClass("fsRequired");
          exploit.attr("aria-required", true);
          exploit.attr("fsRequired");
          evidenciaExplotacion.prop("required", true);
          evidenciaExplotacion.addClass("fsRequired");
          evidenciaExplotacion.attr("aria-required", true);
          evidenciaExplotacion.attr("fsRequired");
        }
        else {
          exploit.prop("required", false);
          exploit.removeClass("fsRequired");
          exploit.attr("aria-required", false);
          evidenciaExplotacion.prop("required", false);
          evidenciaExplotacion.removeClass("fsRequired");
          evidenciaExplotacion.attr("aria-required", false);
          animacion.prop("required", false);
          animacion.removeClass("fsRequired");
          animacion.attr("aria-required", false);
        }
        break;
      }
      if (cont == obj.length - 1) {
        description.val("");
        requirement.val("");
        solution.val("");
        threat.val("");
        risk.val("");
        tipo.val("");
        debilidad.val(0);
        donde.attr("placeholder", "Formato DONDE dependiendo de la vulnerabilidad.");
        $("#fsCell38861739").addClass("fsHidden");
        $("#fsCell38307753").addClass("fsHidden");
        $("#field38307753").attr("disabled");
      }
    }
  });
}

Tabletop.init({
  "callback": showInfo,
  "key": publicSpreadsheetUrl,
  "prettyColumnNames": true,
  "simpleSheet": true
});
$(donde).focusout(function focusoutDonde () {
  donde.val($.trim(donde.val()));
});

$(requirement).focusout(function focusoutRequirement () {
  requirement.val($.trim(requirement.val()));
  if (requirement.val()[requirement.val().length - 1] != ".") {
    requirement.val(`${requirement.val()}.`);
  }
  if (isUpperCase(requirement.val()[0]) == false) {
    requirement.val(requirement.val().capitalizeFirstLetter());
  }
});

$(description).focusout(function focusoutDescription () {
  description.val($.trim(description.val()));
  if (description.val()[description.val().length - 1] != ".") {
    description.val(`${description.val()}.`);
  }
  if (isUpperCase(description.val()[0]) == false) {
    description.val(description.val().capitalizeFirstLetter());
  }
  description.val(description.val());
});

$(solution).focusout(function focusoutSolution () {
  solution.val($.trim(solution.val()));
  if (solution.val()[solution.val().length - 1] != ".") {
    solution.val(`${solution.val()}.`);
  }
  if (isUpperCase(solution.val()[0]) == false) {
    solution.val(solution.val().capitalizeFirstLetter());
  }
});

$(risk).focusout(function focusoutRisk () {
  risk.val($.trim(risk.val()));
  if (risk.val()[risk.val().length - 1] != ".") {
    risk.val(`${risk.val()}.`);
  }
  if (isUpperCase(risk.val()[0]) == false) {
    risk.val(risk.val().capitalizeFirstLetter());
  }
});

$(threat).focusout(function focusoutThreat () {
  threat.val($.trim(threat.val()));
  if (threat.val()[threat.val().length - 1] != ".") {
    threat.val(`${threat.val()}.`);
  }
  if (isUpperCase(threat.val()[0]) == false) {
    threat.val(threat.val().capitalizeFirstLetter());
  }
});

$(evidenciaHallazgo).change(function changeEvidence () {
  const hallazgoUpload = $(evidenciaHallazgo).val().
    split("\\")[2].split(".")[0];
  const substring = "evidencia";
  if (hallazgoUpload.indexOf(substring) === -1) {
    $msg.error("El archivo se debe contener la palabra evidencia");
    evidenciaHallazgo.val("");
  }
});

$(exploit).change(function changeExploit () {
  const exploitUpload = $(exploit).val().
    split("\\")[2].split(".")[0];
  if (exploitUpload != "exploit") {
    $msg.error("El archivo se debe llamar: exploit");
    exploit.val("");
  }
  else if (exploitUpload == "exploit") {
    exploit.attr("aria-invalid", false);
  }
});

$(evidenciaExplotacion).change(function changeExploitation () {
  const explotacionUpload = $(evidenciaExplotacion).val().
    split("\\")[2].split(".")[0];
  if (explotacionUpload != "evidencia-de-explotacion") {
    $msg.error("El archivo se debe llamar: evidencia-de-explotacion");
    evidenciaExplotacion.val("");
  }
  else if (explotacionUpload == "evidencia-de-explotacion") {
    evidenciaExplotacion.attr("aria-invalid", false);
  }
});

$(animacion).change(function changeAnimation () {
  const animacionUpload = $(animacion).val().
    split("\\")[2].split(".")[0];
  if (animacionUpload != "animacion-de-explotacion") {
    $msg.error("El archivo se debe llamar: animacion-de-explotacion");
    animacion.val("");
  }
  else if (animacionUpload == "animacion-de-explotacion") {
    animacion.attr("aria-invalid", false);
  }
});

$(solutionPdf).change(function changeSolution () {
  const solUpload = $(solutionPdf).val().
    split("\\")[2].split(".")[0];
  if (solUpload != "solucion") {
    $msg.error("El archivo se debe llamar: solucion");
    solutionPdf.val("");
  }
});
