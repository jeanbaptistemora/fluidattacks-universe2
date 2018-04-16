/* eslint no-magic-numbers: ["error", { "ignore": [0, 13] }]*/
/* global
integrates, $, BASE, mixpanel, userMail, $xhr, Organization, userEmail, Rollbar, mixPanelDashboard, userName
*/
/**
 * @file eventualityController.js
 * @author engineering@fluidattacks.com
 */
/**
 * Cambia el formato de una de las columnas de la tabla de eventualidades
 * @function afectacionFormatter
 * @param {String} value
 * @param {Object} row
 * @param {Number} index
 */
function afectacionFormatter (value, row, index) {
  if (typeof value === "undefined") {
    return "0";
  }
  if (!isFinite(value)) {
    if (value.trim() == "") {
      return "0";
    }
  }
  return value;
}

/**
 * Calcula la afectacion total para el label resumen
 * @function evntTotalize
 * @param {Object} data
 * @return {undefined}
 */
integrates.evntTotalize = function evntTotalize (data) {
  const cardinalidad = 0;
  let afectacion = 0;
  for (let cont = 0; cont < data.data.length; cont++) {
    let auxAfectacion = 0;
    if (data.data[cont].afectacion != "") {
      auxAfectacion += parseInt(data.data[cont].afectacion, 10);
    }
    afectacion += auxAfectacion;
  }
  $("#total_eventualidades").html(data.data.length);
  $("#total_afectacion").html(afectacion);
};

/**
 * Actualiza una fila de la tabla
 * @function updateEvntRow
 * @param {Object} row
 * @return {undefined}
 */
integrates.updateEvntRow = function updateEvntRow (row) {
  const data = $("#eventualities").bootstrapTable("getData");
  const newData = [];
  for (let cont = 0; cont < data.length; cont++) {
    delete data[cont][cont.toString()];
    if (data[cont].id == row.id) {
      newData.push(row);
    }
    else {
      newData.push(data[cont]);
    }
  }
  $("#eventualities").bootstrapTable("destroy");
  $("#eventualities").bootstrapTable({"data": newData});
  $("#eventualities").bootstrapTable("refresh");
  integrates.evntTotalize({data});
};

/**
 * Crea el controlador de la funcionalidad de eventualidades
 * @name eventualityController
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {integrates.eventualityFactory} eventualityFactory
 * @return {undefined}
 */
/** @export */
integrates.controller("eventualityController", function eventualityController ($scope, $uibModal, $translate, eventualityFactory) {
  const attentTitle = $translate.instant("proj_alerts.attentTitle");
  const updatedTitle = $translate.instant("proj_alerts.updatedTitle");
  const eventTitle = $translate.instant("proj_alerts.eventTitle");
  const eventWait = $translate.instant("proj_alerts.eventWait");
  const eventSelect = $translate.instant("proj_alerts.eventSelect");
  const eventRequired = $translate.instant("proj_alerts.eventRequired");
  const eventInternal = $translate.instant("proj_alerts.eventInternal");
  const eventFormstack = $translate.instant("proj_alerts.eventFormstack");
  const eventPositiveint = $translate.instant("proj_alerts.eventPositiveint");
  const eventUpdated = $translate.instant("proj_alerts.eventUpdated");
  const eventExist = $translate.instant("proj_alerts.eventExist");

  /**
   * Inicializa las variables del controlador de eventualidades
   * @function init
   * @member integrates.eventualityController
   * @return {undefined}
   */
  $scope.init = function init () {
    $("#search_section").hide();
    $(".loader").hide();
    document.onkeypress = function onkeypress (ev) {
      // Asignar funcion a la tecla Enter
      if (ev.keyCode === 13) {
        if ($("#project").is(":focus")) {
          $scope.searchEvntByName();
        }
      }
    };
    mixpanel.track("SearchEventuality", {"Email": userEmail});
    $scope.view = {};
    $scope.view.event = false;
  };

  /**
   * Despliega la modal de ver eventualidad
   * @function openModalVer
   * @member integrates.eventualityController
   */
  $scope.openModalVer = function openModalVer () {
    const sel = $("#eventualities").bootstrapTable("getSelections");
    if (sel.length == 0) {
      Rollbar.error("Error: No events are selected");
      $.gritter.add({
        "class_name": "color warning",
        "sticky": false,
        "text": eventSelect,
        "title": "Error"
      });
      return false;
    }
    $scope.currentEventuality = sel[0];

    const modalInstance = $uibModal.open({
      "animation": true,
      "controller" ($scope, $uibModalInstance, currentEventuality) {
        if (currentEventuality.afectacion == "") {
          currentEventuality.afectacion = "0";
        }
        $scope.evnt = currentEventuality;
        $scope.evnt.afectacion = parseInt(currentEventuality.afectacion, 10);
        $scope.closeModalVer = function closeModalVer () {
          $uibModalInstance.close();
        };
      },
      "resolve": {
        "currentEventuality" () {
          return $scope.currentEventuality;
        }
      },
      "templateUrl": "ver.html",
      "windowClass": "ver-modal"
    });
  };

  /**
   * Despliega la modal de ver resumen de eventualidades
   * @function openModalAvance
   * @member integrates.eventualityController
   * @return {undefined}
   */
  $scope.openModalAvance = function openModalAvance () {
    const modalInstance = $uibModal.open({
      "animation": true,
      "controller" ($scope, $uibModalInstance) {
        $scope.rows = $("#eventualities").bootstrapTable("getData");
        $scope.closeModalAvance = function closeModalAvance () {
          $uibModalInstance.close();
        };
      },
      "resolve": {"ok": true},
      "templateUrl": "avance.html",
      "windowClass": "modal avance-modal"
    });
  };

  /**
   * Despliega la modal de editar eventualidades
   * @function openModalEditar
   * @member integrates.eventualityController
   */
  $scope.openModalEditar = function openModalEditar () {
    const sel = $("#eventualities").bootstrapTable("getSelections");
    if (sel.length == 0) {
      Rollbar.error("Error: No events are selected");
      $.gritter.add({
        "class_name": "color warning",
        "sticky": false,
        "text": eventSelect,
        "title": "Error"
      });
      return false;
    }
    $scope.currentEventuality = sel[0];


    const modalInstance = $uibModal.open({
      "animation": true,
      "controller" ($scope, $uibModalInstance, currentEventuality) {
        if (currentEventuality.afectacion == "") {
          currentEventuality.afectacion = "0";
        }
        $scope.evnt = currentEventuality;
        $scope.evnt.afectacion = parseInt(currentEventuality.afectacion, 206);

        $scope.okModalEditar = function okModalEditar () {
          const neg = "negativo";
          let submit = false;
          try {
            if (typeof $scope.evnt.afectacion == "undefined") {
              throw neg;
            }
            submit = true;
          }
          catch (err) {
            Rollbar.error("Error: Affectation can not be a negative number");
            $.gritter.add({
              "class_name": "color warning",
              "sticky": false,
              "text": eventPositiveint,
              "title": attentTitle
            });
            return false;
          }
          eventualityFactory.updateEvnt($scope.evnt).then(function resupdateEvnt (response) {
            if (!response.error) {
              $.gritter.add({
                "class_name": "color success",
                "sticky": false,
                "text": eventUpdated,
                "title": updatedTitle
              });
              integrates.updateEvntRow($scope.evnt);
              $uibModalInstance.close();
            }
            else if (response.error) {
              Rollbar.error("Error: An error occurred updating events");
              $.gritter.add({
                "class_name": "color warning",
                "sticky": false,
                "text": response.message,
                "title": "Error!"
              });
            }
          });
        };

        $scope.closeModalEditar = function closeModalEditar () {
          $uibModalInstance.close();
        };
      },
      "resolve": {
        "currentEventuality" () {
          return $scope.currentEventuality;
        }
      },
      "templateUrl": "editar.html",
      "windowClass": "ver-modal"
    });
  };
  $scope.category = "Name";
  $scope.setCategory = function setCategory (category) {
    $scope.category = category;
  };

  /**
   * Busca las eventualidades por nombre de proyecto
   * @function searchEvntByName
   * @member integrates.eventualityController
   * @return {undefined}
   */
  $scope.searchEvntByName = function searchEvntByName () {
    let vlang = "en-US";
    if (localStorage.lang === "en") {
      vlang = "en-US";
    }
    else {
      vlang = "es-CO";
    }
    const project = $scope.project;
    const category = $scope.category;
    if (typeof project !== "undefined" &&
            project !== "" &&
            typeof category !== "undefined" &&
            category !== "") {
      $scope.response = "";
      $.gritter.add({
        "class_name": "color info",
        "sticky": false,
        "text": eventWait,
        "title": eventTitle
      });
      $(".loader").show();
      $scope.maxRecursiveCall = 5;
      eventualityFactory.getEvntByName(project, category).then(function resgetEvntByName (data) {
        if (!data.error) {
          // CONFIGURACION DE TABLA
          $scope.view.event = true;
          for (let cont = 0; cont < data.data.length; cont++) {
            switch (data.data[cont].tipo) {
            case "Autorización para ataque especial":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.auth_attack");
              break;
            case "Alcance difiere a lo aprobado":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.toe_differs");
              break;
            case "Aprobación de alta disponibilidad":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.high_approval");
              break;
            case "Insumos incorrectos o faltantes":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.incor_supplies");
              break;
            case "Cliente suspende explicitamente":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.explic_suspend");
              break;
            case "Cliente aprueba cambio de alcance":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.approv_change");
              break;
            case "Cliente cancela el proyecto/hito":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.cancel_proj");
              break;
            case "Cliente detecta ataque":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.det_attack");
              break;
            case "Otro":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.other");
              break;
            case "Ambiente no accesible":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.inacc_ambient");
              break;
            case "Ambiente inestable":
              data.data[cont].tipo = $translate.instant("eventFormstack.type.uns_ambient");
              break;
            default:
              data.data[cont].tipo = $translate.instant("eventFormstack.type.unknown");
            }
            switch (data.data[cont].estado) {
            case "Pendiente":
              data.data[cont].estado = $translate.instant("eventFormstack.status.unsolve");
              break;
            case "Tratada":
              data.data[cont].estado = $translate.instant("eventFormstack.status.solve");
              break;
            default:
              data.data[cont].estado = $translate.instant("eventFormstack.status.unknown");
            }
          }
          $("#eventualities").bootstrapTable("destroy");
          $("#eventualities").bootstrapTable({
            "data": data.data,
            "locale": vlang
          });
          $("#eventualities").bootstrapTable("refresh");
          // MANEJO DEL UI
          $("#search_section").show();
          $("[data-toggle=\"tooltip\"]").tooltip();
          integrates.evntTotalize(data);
          $.gritter.add({
            "class_name": "color success",
            "sticky": false,
            "text": updatedTitle,
            "title": eventTitle
          });
        }
        else if (data.error) {
          $scope.view.event = false;
          Rollbar.error("Error: An error occurred searching events");
          $.gritter.add({
            "class_name": "color danger",
            "sticky": false,
            "text": data.message,
            "title": "Error"
          });
        }
      });
    }
    else {
      $scope.response = eventRequired;
    }
  };

  $scope.init();
});
