/* global
integrates, $
*/
/**
 * Controlador de vista de formularios
 * @name formCtr
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @param {Object} $translate
 * @param {Object} $projectFtry
 * @return {undefined}
 */
integrates.controller(
  "formCtrl",
  function (
    $scope, $location,
    $uibModal, $timeout,
    $state, $stateParams,
    $translate, projectFtry
  ) {
    // Autocompletar formularios de formstack
    const urlForm = $location.search();
    const urlLength = Object.keys(urlForm).length;
    const url_length = 0;
    if (urlLength > url_length && urlForm.autocomplete == "true") {
      // Formulario de avance
      $("#ifrmProgress").on("load", function () {
        const iframe = document.getElementById("ifrmProgress");
        const innerDoc = iframe.contentDocument || iframe.contentWindow.document;
        if (urlForm["Tipo de Avance"] == "Proyecto") {
          // InnerDoc.getElementById("field43795015_1").setAttribute("checked", true);
          innerDoc.getElementById("field28635595").value = urlForm.Talento;
          innerDoc.getElementById("field47449040").value = urlForm.Bug;
          innerDoc.getElementById("field55821593").value = urlForm["Criticidad a la fecha"];
          innerDoc.getElementById("field28634673").value = urlForm["Código"];
          innerDoc.getElementById("field28640967").value = urlForm.Documentadas;
          innerDoc.getElementById("field58043328").value = urlForm["Efectividad de Cierre"];
          innerDoc.getElementById("field56010467").value = urlForm["Entradas Evaluables"];
          innerDoc.getElementById("field56010460").value = urlForm["Entradas Evaluadas"];
          innerDoc.getElementById("field56012910").value = urlForm["Entradas Visibles"];
          innerDoc.getElementById("field28634976").value = urlForm.Evaluables;
          innerDoc.getElementById("field28634991").value = urlForm.Evaluadas;
          innerDoc.getElementById("field28689409").value = urlForm["Eventualidades abiertas"];
          innerDoc.getElementById("field47323254").value = urlForm.Interesado;
          innerDoc.getElementById("field56010469").value = urlForm["Lineas Evaluables"];
          innerDoc.getElementById("field56010465").value = urlForm["Lineas Evaluadas"];
          innerDoc.getElementById("field56012911").value = urlForm["Lineas Visibles"];
          innerDoc.getElementById("field46560485").value = urlForm.Modalidad;
          innerDoc.getElementById("field57918827").value = urlForm.OcurrenciasH;
          innerDoc.getElementById("field28635690").value = urlForm.OcurrenciasS;
          innerDoc.getElementById("field28634672").value = urlForm["Organización"];
          innerDoc.getElementById("field28640689").value = urlForm.Planeados;
          innerDoc.getElementById("field28638487").value = urlForm.Proyecto;
          innerDoc.getElementById("field56010470").value = urlForm["Puertos Evaluables"];
          innerDoc.getElementById("field56010464").value = urlForm["Puertos Evaluados"];
          innerDoc.getElementById("field56012912").value = urlForm["Puertos Visibles"];
          innerDoc.getElementById("field28640634").value = urlForm.Realizados;
          innerDoc.getElementById("field56179489").value = urlForm.Registros;
          innerDoc.getElementById("field48087363").value = urlForm.Repositorios;
          innerDoc.getElementById("field28638510").value = urlForm["Resultados preliminares"];
          innerDoc.getElementById("field28644201").value = urlForm.Soluciones;
          innerDoc.getElementById("field28640019").value = urlForm["Unidad de TOE"];
          innerDoc.getElementById("field28635413").value = urlForm.Verificables;
          innerDoc.getElementById("field28635411").value = urlForm.Verificados;
          innerDoc.getElementById("field56012915").value = urlForm.Visibles;
          innerDoc.getElementById("field57918852").value = urlForm.VulnerabilidadesH;
          innerDoc.getElementById("field28635669").value = urlForm.VulnerabilidadesS;
        }
        else if (urlForm["Tipo de Avance"] == "Standard") {
          // InnerDoc.getElementById("field43795015_2").setAttribute("checked", true);
          innerDoc.getElementById("field28635595").value = urlForm.Talento;
          innerDoc.getElementById("field28634672").value = urlForm["Organización"];
          innerDoc.getElementById("field47323254").value = urlForm.Interesado;
          innerDoc.getElementById("field43795060").value = urlForm["Qué Hice Hoy"];
          innerDoc.getElementById("field43795103").value = urlForm["Qué Haré Mañana"];
          innerDoc.getElementById("field43795173").value = urlForm["En Qué Necesito Ayuda"];
        }
      });
    }
  }
);
