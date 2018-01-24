/**
 * @file findingcontentCtrl.js
 * @author engineering@fluid.la
 */
/**
 * Funciones para administrar el UI del resumen de un hallazgo
 * @name findingContentCtrl.js
 * @param {Object} $scope
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $translate
 * @param {Object} ngNotify
 * @return {undefined}
 */
integrates.controller("findingcontentCtrl", function($scope, $stateParams, $timeout,
                                                          $uibModal, $translate, $state,
                                                          ngNotify, findingFactory, projectFtry) {
    $scope.findingHeaderBuilding = function(){
        //console.log($scope.finding);
        $scope.header = {};
        var cierres = $scope.finding.cierres;
        var cierresTmp = [];
        for(var i = 0; i < cierres.length ; i++){
            cierre = cierres[i];
            cierre.position = i+1;
            cierresTmp.push(cierre);
        }
        $scope.finding.cierres = cierresTmp;
        $scope.header.findingTitle = $scope.finding.hallazgo;
        $scope.header.findingType = $scope.finding.tipo_prueba;
        $scope.header.findingRisk = "";
        $scope.header.findingState = $scope.finding.estado;
        $scope.header.findingID = $scope.finding.id;
        $scope.header.findingValue = $scope.finding.criticidad;
        $scope.header.findingTreatment = $scope.finding.tratamiento;
        var findingValue = parseFloat($scope.finding.criticidad);
        if(findingValue >= 7){
            $scope.header.findingValueDescription = $translate.instant('finding_formstack.criticity_header.high');
            $scope.header.findingValueColor = $scope.colors.critical;
        }else if(findingValue >= 4 && findingValue <= 6.9){
            $scope.header.findingValueDescription = $translate.instant('finding_formstack.criticity_header.moderate');
            $scope.header.findingValueColor = $scope.colors.moderate;
        }else{
            $scope.header.findingValueDescription = $translate.instant('finding_formstack.criticity_header.tolerable');
            $scope.header.findingValueColor = $scope.colors.tolerable;
        }

        if($scope.header.findingState == "Abierto" || $scope.header.findingState == "Open" ){
            $scope.header.findingStateColor = $scope.colors.critical;
        }else if($scope.header.findingState == "Parcialmente cerrado" || $scope.header.findingState == "Partially closed"){
            $scope.header.findingStateColor = $scope.colors.moderate;
        }else{
            $scope.header.findingStateColor = $scope.colors.ok;
        }

        $scope.header.findingCount = $scope.finding.cardinalidad;
    };
    String.prototype.replaceAll = function(search, replace)
    {
        if (replace === undefined) {
            return this.toString();
        }
        return this.replace(new RegExp('[' + search + ']', 'g'), replace);
    };
    $scope.findingExploitTab = function(){
        var url_pre = BASE.url + "get_exploit?id=";
        $scope.hasExploit = false;
        if($scope.finding.exploit !== undefined && $scope.finding.cierres.length == 0){
            var url = url_pre + $scope.finding.exploit;
            var exploit = projectFtry.getExploit(url);
            $scope.hasExploit = true;
            exploit.then(function(response){
                if(!response.error){
                    response = response.replaceAll("<", "&lt;");
                    response = response.replaceAll(">", "&gt;");
                    $scope.exploitURL = response;
                } else {
                  Rollbar.error(response.message);
                }
            });
        } else {
            $scope.hasExploit = false;
        }
    };
    $scope.cssv2Editable = function(){
        if($scope.onlyReadableTab2 == false){
            $scope.onlyReadableTab2 = true;
        }else{
            $scope.onlyReadableTab2 = false;
        }
    };
    $scope.descriptionEditable = function(){
        if($scope.onlyReadableTab1 == false){
            $scope.onlyReadableTab1 = true;
        }else{
            $scope.onlyReadableTab1 = false;
        }
    };
    $scope.evidenceEditable = function(){
        if($scope.onlyReadableTab3 == false){
            $scope.onlyReadableTab3 = true;
        }else{
            $scope.onlyReadableTab3 = false;
        }
    };
    $scope.treatmentEditable = function(){
      if($scope.onlyReadableTab4 == false){
          $scope.finding.responsable_tratamiento = userEmail;
          $scope.onlyReadableTab4 = true;
          $scope.finding.tratamiento = $scope.aux.tratamiento
          $scope.finding.razon_tratamiento = $scope.aux.razon
      }else if($scope.onlyReadableTab4 == true){
          $scope.finding.tratamiento = $scope.aux.tratamiento
          $scope.finding.razon_tratamiento = $scope.aux.razon
          $scope.finding.responsable_tratamiento = $scope.aux.responsable
          $scope.onlyReadableTab4 = false;
      }
    };
    $scope.updateCSSv2 = function(){
        //Obtener datos de las listas
        var cssv2Data = {
            id: $scope.finding.id,
            vector_acceso: $scope.finding.vector_acceso,
            impacto_confidencialidad: $scope.finding.impacto_confidencialidad,
            autenticacion: $scope.finding.autenticacion,
            impacto_integridad: $scope.finding.impacto_integridad,
            explotabilidad: $scope.finding.explotabilidad,
            impacto_disponibilidad: $scope.finding.impacto_disponibilidad,
            nivel_confianza: $scope.finding.nivel_confianza,
            nivel_resolucion: $scope.finding.nivel_resolucion,
            complejidad_acceso: $scope.finding.complejidad_acceso
        };
        //Recalcular CSSV2
        $scope.findingCalculateCSSv2();
        cssv2Data.criticidad = $scope.finding.criticidad;
        //Instanciar modal de confirmacion
        var modalInstance = $uibModal.open({
            templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
            animation: true,
            backdrop: 'static',
            resolve: { updateData: cssv2Data },
            controller: function($scope, $uibModalInstance, updateData){
                $scope.modalTitle = $translate.instant('confirmmodal.title_cssv2');
                $scope.ok = function(){
                    //Consumir el servicio
                    var req = projectFtry.UpdateCSSv2(updateData);
                    //Capturar la Promisse
                    req.then(function(response){
                        if(!response.error){
                            var updated_at = $translate.instant('proj_alerts.updated_title');
                            var updated_ac = $translate.instant('proj_alerts.updated_cont');
                            $msg.success(updated_ac,updated_at);
                            $uibModalInstance.close();
                            location.reload();
                        }else{
                            var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                            Rollbar.error("Error: An error occurred updating CSSv2");
                            $msg.error(error_ac1);
                        }
                    });
                };
                $scope.close = function(){
                    $uibModalInstance.close();
                };
            }
        });
    };
    $scope.updateEvidenceText = function(target){
        console.log(target);
        $msg.info($translate.instant('search_findings.tab_evidence.alert'));
        return false;
    };
    $scope.deleteFinding = function(){
            //Obtener datos
            descData = {
                id: $scope.finding.id
            };
            var modalInstance = $uibModal.open({
                templateUrl: BASE.url + 'assets/views/project/deleteMdl.html',
                animation: true,
                backdrop: 'static',
                resolve: { updateData: descData },
                controller: function($scope, $uibModalInstance, updateData, $stateParams, $state){
                    $scope.vuln = {};
                    $scope.modalTitle = $translate.instant('confirmmodal.title_finding');
                    $scope.ok = function(){
                        $scope.vuln.id = updateData.id;
                        //Consumir el servicio
                        var req = projectFtry.DeleteFinding($scope.vuln);
                        //Capturar la Promisse
                        req.then(function(response){
                            if(!response.error){
                                var updated_at = $translate.instant('proj_alerts.updated_title');
                                var updated_ac = $translate.instant('proj_alerts.updated_cont');
                                $msg.success(updated_ac,updated_at);
                                $uibModalInstance.close();
                                $state.go("ProjectNamed", {project: $stateParams.project});
                                //Tracking mixpanel
                                mixPanelDashboard.trackFinding("DeleteFinding", userEmail, descData.id);
                            }else{
                              var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                              Rollbar.error("Error: An error occurred deleting finding");
                              $msg.error(error_ac1);
                            }
                        });
                    };
                    $scope.close = function(){
                        $uibModalInstance.close();
                    };
                }
            });
        };
    $scope.goUp = function(){
         $('html, body').animate({ scrollTop: 0 }, 'fast');
     };
    $scope.loadFindingByID = function(id){
        var findingObj = undefined;
        var req = findingFactory.getVulnById(id);
        req.then(function(response){
            if(!response.error && $stateParams.project == response.data.proyecto_fluid.toLowerCase()){
                $scope.finding = response.data;
                $scope.aux={};
                $scope.aux.tratamiento = $scope.finding.tratamiento;
                $scope.aux.razon = $scope.finding.razon_tratamiento;
                $scope.aux.responsable = $scope.finding.responsable_tratamiento;
                   switch ($scope.finding.actor) {
                     case "​Cualquier persona en Internet":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_internet');;
                       break;
                     case "Cualquier cliente de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_costumer');;
                       break;
                     case "Solo algunos clientes de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.some_costumer');;
                       break;
                     case "Cualquier persona con acceso a la estación":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_access');;
                       break;
                     case "Cualquier empleado de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_employee');;
                       break;
                     case "Solo algunos empleados":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.some_employee');;
                       break;
                     case "Solo un empleado":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.one_employee');;
                       break;
                     default:
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.default');;
                   }
                   switch ($scope.finding.autenticacion) {
                     case "0.704 | Ninguna: No se requiere autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.any_authen');;
                       break;
                     case "0.560 | Única: Único punto de autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.single_authen');;
                       break;
                     case "0.450 | Multiple: Multiples puntos de autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.multiple_authen');;
                       break;
                     default:
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.default');;
                   }
                   switch ($scope.finding.categoria) {
                     case "Actualizar y configurar las líneas base de seguridad de los componentes":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.update_base');;
                       break;
                     case "Definir el modelo de autorización considerando el principio de mínimo privilegio":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.define_model');;
                       break;
                     case "Desempeño":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.performance');;
                       break;
                     case "Eventualidad":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.event');;
                       break;
                     case "Evitar exponer la información técnica de la aplicación, servidores y plataformas":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.avoid_technical');;
                       break;
                     case "Excluir datos sensibles del código fuente y del registro de eventos":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.exclude_finding');;
                       break;
                     case "Fortalecer controles en autenticación y manejo de sesión":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_authen');;
                       break;
                     case "Fortalecer controles en el procesamiento de archivos":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_process');;
                       break;
                     case "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_protect');;
                       break;
                     case "Implementar controles para validar datos de entrada":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.validate_input');;
                       break;
                     case "Mantenibilidad":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.maintain');;
                       break;
                     case "Registrar eventos para trazabilidad y auditoría":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.record_event');;
                       break;
                     case "Utilizar protocolos de comunicación seguros":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.secure_protoc');;
                       break;
                     case "Validar la integridad de las transacciones en peticiones HTTP":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.validate_http');;
                       break;
                     default:
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.default');;
                   }
                   switch ($scope.finding.complejidad_acceso) {
                     case "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.high_complex');;
                       break;
                     case "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.medium_complex');;
                       break;
                     case "0.710 | Bajo: No se requiere ninguna condición especial":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.low_complex');;
                       break;
                     default:
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.default');;
                   }
                   switch ($scope.finding.escenario) {
                     case "Anónimo desde Internet":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.anon_inter');;
                       break;
                     case "Anónimo desde Intranet":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.anon_intra');;
                       break;
                     case "Escaneo de Infraestructura":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.infra_scan');;
                       break;
                     case "Extranet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_extra');;
                       break;
                     case "Internet usuario autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.auth_inter');;
                       break;
                     case "Internet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_inter');;
                       break;
                     case "Intranet usuario autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.auth_intra');;
                       break;
                     case "Intranet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_inter');;
                        break;
                     default:
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.default');;
                   }
                   switch ($scope.finding.estado) {
                     case "Abierto":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.open');;
                       break;
                     case "Cerrado":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.close');;
                       break;
                     case "Parcialmente cerrado":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.part_close');;
                       break;
                     default:
                       $scope.finding.estado = $translate.instant('finding_formstack.status.default');;
                   }
                   switch ($scope.finding.explotabilidad) {
                     case "0.850 | Improbable: No existe un exploit":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.improbable');;
                       break;
                     case "0.900 | Conceptual: Existen pruebas de laboratorio":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.conceptual');;
                       break;
                     case "0.950 | Funcional: Existe exploit":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.functional');;
                       break;
                     case "1.000 | Alta: No se requiere exploit o se puede automatizar":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.high');;
                       break;
                     default:
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.default');;
                   }
                   switch ($scope.finding.explotable) {
                     case "Si":
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.yes');;
                       break;
                     case "No":
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.no');;
                       break;
                     default:
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.default');;
                   }
                   switch ($scope.finding.impacto_confidencialidad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.none');;
                       break;
                     case "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.partial');
                       break;
                     case "0.660 | Completo: Se controla toda la información relacionada con el objetivo":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.complete');
                       break;
                     default:
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.default');;
                   }
                   switch ($scope.finding.impacto_disponibilidad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.none');;
                       break;
                     case "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.partial');;
                       break;
                     case "0.660 | Completo: Hay una caída total del objetivo":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.complete');;
                       break;
                     default:
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.default');;
                   }
                   switch ($scope.finding.impacto_integridad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.none');;
                       break;
                     case "0.275 | Parcial: Es posible modificar cierta información del objetivo":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.partial');;
                       break;
                     case "0.660 | Completo: Es posible modificar toda la información del objetivo":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.complete');;
                       break;
                     default:
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.default');;
                   }
                   switch ($scope.finding.nivel_confianza) {
                     case "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.not_confirm');;
                       break;
                     case "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.not_corrob');;
                       break;
                     case "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.confirmed');;
                       break;
                     default:
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.default');;
                   }
                   switch ($scope.finding.nivel_resolucion) {
                     case "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.palliative');;
                       break;
                     case "0.870 | Oficial: Existe un parche disponible por el fabricante":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.official');;
                       break;
                     case "0.900 | Temporal: Existen soluciones temporales":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.temporal');;
                       break;
                     case "1.000 | Inexistente: No existe solución":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.non_existent');;
                       break;
                     default:
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.default');;
                   }
                   switch ($scope.finding.probabilidad) {
                     case "100% Vulnerado Anteriormente":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.prev_vuln');;
                       break;
                     case "75% Fácil de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.easy_vuln');;
                       break;
                     case "50% Posible de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.possible_vuln');;
                       break;
                     case "25% Difícil de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.diffic_vuln');;
                       break;
                     default:
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.default');;
                   }
                   switch ($scope.finding.tipo_hallazgo_cliente) {
                     case "Higiene":
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.hygiene');;
                       break;
                     case "Vulnerabilidad":
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.vuln');;
                       break;
                     default:
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.default');;
                   }
                   switch ($scope.finding.tipo_prueba) {
                     case "Análisis":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.analysis');;
                       break;
                     case "Aplicación":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.app');;
                       break;
                     case "Binario":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.binary');;
                       break;
                     case "Código":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.code');;
                       break;
                     case "Infraestructura":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.infras');;
                       break;
                     default:
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.default');;
                   }
                   switch ($scope.finding.vector_acceso) {
                     case "0.646 | Red adyacente: Explotable desde el mismo segmento de red":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.adjacent');;
                       break;
                     case "1.000 | Red: Explotable desde Internet":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.network');;
                       break;
                     case "0.395 | Local: Explotable con acceso local al objetivo":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.local');;
                       break;
                     default:
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.default');;
                   }
                   switch ($scope.finding.tratamiento) {
                     case "Asumido":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.asummed');;
                       break;
                     case "Pendiente":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.working');;
                       break;
                     case "Remediar":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.remediated');;
                       break;
                     default:
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.default');;
                   }
                $scope.findingHeaderBuilding();
                $scope.view.project = false;
                $scope.view.finding = true;
                $scope.findingInformationTab();
                $scope.findingEvidenceTab();
                $scope.findingExploitTab();
                $scope.findingCommentTab();
                //Control de campos para tipos de hallazgo
                $scope.esDetallado = false;
                if($scope.finding.nivel == "Detallado"){
                  $scope.esDetallado = true;
                }
                //Control de campos editables
                $scope.onlyReadableTab1 = true;
                $scope.onlyReadableTab2 = true;
                //Inicializar galeria de evidencias
                $('.popup-gallery').magnificPopup({
                  delegate: 'a',
                  type: 'image',
                  tLoading: 'Loading image #%curr%...',
                  mainClass: 'mfp-img-mobile',
                  gallery: {
                      enabled: true,
                      navigateByImgClick: true,
                      preload: [0,1]
                    },
                    image: {
                      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
                      titleSrc: function(item) {
                          return item.el.attr('title');
                    }
                }
            });
            //Init auto height in textarea
            if($("#infoItem").hasClass("active")){
              $timeout(function() {
                $scope.$broadcast("elastic:adjust");
              });
            }
            $("#trackingItem").on("click", function(){
              $timeout(function() {
                $scope.$broadcast("elastic:adjust");
              });
            });
            $("#infoItem").on("click", function(){
              $timeout(function() {
                $scope.$broadcast("elastic:adjust");
              });
            });
            $("#edit").on("click", function(){
              $timeout(function() {
                $scope.$broadcast("elastic:adjust");
              });
            });
            //Init auto height in panels
            $("#evidenceItem").on("click", function(){
              $('.equalHeight').matchHeight();
            });
            $timeout($scope.goUp, 200);
        } else {
          $msg.error($translate.instant('proj_alerts.no_finding'));
          Rollbar.error("Error: Finding not found");
          return false;
        }
      });
    };
    $scope.configColorPalette = function(){
        $scope.colors = {};
        $scope.colors.critical = "background-color: #f12;";  //red
        $scope.colors.moderate = "background-color: #f72;";  //orange
        $scope.colors.tolerable = "background-color: #ffbf00;"; //yellow
        $scope.colors.ok = "background-color: #008000;"; //green
    };
    $scope.configKeyboardView = function(){
        document.onkeypress = function(ev){
            //Buscar un proyecto
            if(ev.keyCode === 13){
                if($('#project').is(':focus')){
                    $scope.search();
                }
            }
        };
    };
    $scope.findingCalculateCSSv2 = function(){
        var ImpCon = parseFloat($scope.finding.impacto_confidencialidad.split(" | ")[0]);
        var ImpInt = parseFloat($scope.finding.impacto_integridad.split(" | ")[0]);
        var ImpDis = parseFloat($scope.finding.impacto_disponibilidad.split(" | ")[0]);
        var AccCom = parseFloat($scope.finding.complejidad_acceso.split(" | ")[0]);
        var AccVec = parseFloat($scope.finding.vector_acceso.split(" | ")[0]);
        var Auth = parseFloat($scope.finding.autenticacion.split(" | ")[0]);
        var Explo = parseFloat($scope.finding.explotabilidad.split(" | ")[0]);
        var Resol = parseFloat($scope.finding.nivel_resolucion.split(" | ")[0]);
        var Confi = parseFloat($scope.finding.nivel_confianza.split(" | ")[0]);
        var BaseScore = (((0.6*(10.41*(1-(1-ImpCon)*(1-ImpInt)*(1-ImpDis))))+(0.4*(20*AccCom*Auth*AccVec))-1.5)*1.176);
        Temporal = BaseScore * Explo * Resol * Confi;
        CVSSGeneral = Temporal;
        $scope.finding.cssv2base = BaseScore.toFixed(1);
        $scope.finding.criticidad = Temporal.toFixed(1);
    };
    $scope.findingDropDownList = function(){
        $scope.list = {};
        $scope.list.finding_type = finding_type;
        $scope.list.categories = categories;
        $scope.list.probability = probabilities;
        $scope.list.actor = actor;
        $scope.list.scenario = scenario;
        $scope.list.accessVector = accessVector;
        $scope.list.accessComplexity = accessComplexity;
        $scope.list.authentication = authentication;
        $scope.list.confidenciality = confidenciality;
        $scope.list.integrity = integrity;
        $scope.list.availability = availability;
        $scope.list.explotability = explotability;
        $scope.list.resolutionLevel = resolutionLevel;
        $scope.list.realiabilityLevel = realiabilityLevel;
        $scope.list.treatment = tratamiento;
    };
    $scope.findingInformationTab = function(){
        $scope.findingDropDownList();
        $scope.finding.cardinalidad = parseInt($scope.finding.cardinalidad);
        $scope.finding.criticidad = parseFloat($scope.finding.criticidad);
        $scope.findingCalculateCSSv2();
        if($scope.finding.nivel == "Detallado"){
            $scope.esDetallado = "show-detallado";
            $scope.esGeneral = "hide-detallado";
            $scope.findingCalculateSeveridad();
        }else{
            $scope.esDetallado = "hide-detallado";
            $scope.esGeneral = "show-detallado";
        }
    };
    $scope.capitalizeFirstLetter = function(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    };
    $scope.findingEvidenceTab = function(){
        $scope.tabEvidences = [];
        var evidenceList = [];
        var url_pre = window.location.href.split('dashboard#!/')[0] + window.location.href.split('dashboard#!/')[1] + '/';
        if($scope.finding.animacion !== undefined){
            var url = url_pre + $scope.finding.animacion;
            evidenceList.push({
                "url": url,
                "desc": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                "ref": 0
            });
        }
        if($scope.finding.explotacion !== undefined){
            var url = url_pre + $scope.finding.explotacion;
            evidenceList.push({
                "url": url,
                "desc": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                "ref": 1
            });
        }
        if($scope.finding.desc_evidencia_1 !== undefined
            && $scope.finding.ruta_evidencia_1 !== undefined){
            var url = url_pre + $scope.finding.ruta_evidencia_1;
            evidenceList.push({
                "url": url,
                "desc": $scope.capitalizeFirstLetter(
                    $scope.finding.desc_evidencia_1
                ),
                "ref": 2
            });
        }
        if($scope.finding.desc_evidencia_2 !== undefined
            && $scope.finding.ruta_evidencia_2 !== undefined){
            var url = url_pre + $scope.finding.ruta_evidencia_2;
            evidenceList.push({
                "url": url,
                "desc": $scope.capitalizeFirstLetter(
                    $scope.finding.desc_evidencia_2
                ),
                "ref": 3
            });
        }
        if($scope.finding.desc_evidencia_3 !== undefined
            && $scope.finding.ruta_evidencia_3 !== undefined){
            var url = url_pre + $scope.finding.ruta_evidencia_3;
            evidenceList.push({
                "url": url,
                "desc": $scope.capitalizeFirstLetter(
                    $scope.finding.desc_evidencia_3
                ),
                "ref": 4
            });
        }
        if($scope.finding.desc_evidencia_4 !== undefined
            && $scope.finding.ruta_evidencia_4 !== undefined){
            var url = url_pre + $scope.finding.ruta_evidencia_4;
            evidenceList.push({
                "url": url,
                "desc": $scope.capitalizeFirstLetter(
                    $scope.finding.desc_evidencia_4
                ),
                "ref": 5
            });
        }
        if($scope.finding.desc_evidencia_5 !== undefined
            && $scope.finding.ruta_evidencia_5 !== undefined){
            var url = url_pre + $scope.finding.ruta_evidencia_5;
            evidenceList.push({
                "url": url,
                "desc": $scope.capitalizeFirstLetter(
                    $scope.finding.desc_evidencia_5
                ),
                "ref": 6
            });
        }
        $scope.tabEvidences = evidenceList;
    };
    $scope.findingCommentTab = function(){
        if($scope.finding.id !== undefined){
            var comments = projectFtry.getComments($scope.finding.id);
            comments.then(function(response){
                if(!response.error){                   
                    var usersArray = []
                    for (var i = 0; i < response.data.length; i++) {
                      var user = {fullname: "", email: ""};
                      user["fullname"] = response.data[i].fullname;
                      user["email"] = response.data[i].email;
                      usersArray.push(user);
                    }                   
                    var saveComment = function(data) {
                      // Convert pings to human readable format
                      $(data.pings).each(function(index, id) {
                        var user = usersArray.filter(function(user){return user.id == id})[0];
                        data.content = data.content.replace('@' + id, '@' + user.fullname);
                      });
                      return data;
                    }
                    $('#comments-container').comments({
                      roundProfilePictures: true,
                      textareaRows: 2,
                      enableAttachments: false,
                      enableHashtags: true,
                      enablePinging: false,
                      enableUpvoting: false,
                      enableEditing: false,
                      getUsers: function(success, error) {
                        setTimeout(function() {
                          success(usersArray);
                        }, 500);
                      },
                      getComments: function(success, error) {
                        setTimeout(function() {
                          success(response.data);
                        }, 500);
                      },
                      postComment: function(data, success, error) {
                        data["id"] = parseInt(Math.round(new Date()/1000).toString() + (Math.random() * 10000).toString(9));
                        data["finding_name"] = $scope.finding.hallazgo;
                        data["project"] = $scope.finding.proyecto_fluid;
                        data["finding_url"] = window.location.href;
                        var comment = projectFtry.addComment($scope.finding.id, data);
                        comment.then(function(response){
                          if(!response.error){
                            //Tracking mixpanel
                            var org = Organization.toUpperCase();
                            var projt = $stateParams.project.toUpperCase();
                            mixPanelDashboard.trackFindingDetailed("FindingNewComment", userName, userEmail, org, projt, $scope.finding.id);
                            setTimeout(function() {
                              success(data);
                            }, 500);
                          } else {
                            Rollbar.error("Error: An error occurred adding comment");
                          }
                        });
                      }
                    });                                   
                }
            });
        }
    };
    $scope.findingCalculateSeveridad = function(){
        if(!isNaN($scope.finding.severidad)){
            var severidad = parseFloat($scope.finding.severidad);
            if (severidad < 0 || severidad > 5){
                Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
                $msg.error($translate.instant('proj_alerts.error_severity'), "error");
                return false;
            }
            try{
                var prob = $scope.finding.probabilidad;
                var severidad = $scope.finding.severidad;
                prob = prob.split("%")[0];
                prob = parseFloat(prob)/100.0;
                severidad = parseFloat(severidad);
                var vRiesgo = prob*severidad;
                if(vRiesgo >= 3){
                    $scope.finding.valor_riesgo = "(:r) Critico".replace(":r", vRiesgo.toFixed(1));
                }else if(vRiesgo >= 2 && vRiesgo < 3){
                    $scope.finding.valor_riesgo = "(:r) Moderado".replace(":r", vRiesgo.toFixed(1));
                }else{
                    $scope.finding.valor_riesgo = "(:r) Tolerable".replace(":r", vRiesgo.toFixed(1));
                }
                return true;
            }catch(e){
                    $scope.finding.valor_riesgo = "";
                    return false;
            }
        }else{
            Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
            $msg.error($translate.instant('proj_alerts.error_severity'), "error");
            return false;
        }
    };
    $scope.updateDescription = function(){
         //Obtener datos
         descData = {
             id: $scope.finding.id,
             nivel: $scope.finding.nivel,
             hallazgo: $scope.finding.hallazgo,
             cardinalidad: $scope.finding.cardinalidad,
             escenario: $scope.finding.escenario,
             actor: $scope.finding.actor,
             categoria: $scope.finding.categoria,
             valor_riesgo: $scope.finding.valor_riesgo,
             probabilidad: $scope.finding.probabilidad,
             severidad: $scope.finding.severidad,
             vulnerabilidad: $scope.finding.vulnerabilidad,
             requisitos: $scope.finding.requisitos,
             donde: $scope.finding.donde,
             vector_ataque: $scope.finding.vector_ataque,
             amenaza: $scope.finding.amenaza,
             solucion_efecto: $scope.finding.solucion_efecto,
             sistema_comprometido: $scope.finding.sistema_comprometido,
             cwe: $scope.finding.cwe,
         };
         if(descData.nivel == "Detallado"){
             //Recalcular Severidad
             var choose = $scope.findingCalculateSeveridad();
             if(!choose){
                 Rollbar.error("Error: An error occurred calculating severity");
                 $msg.error( $translate.instant('proj_alerts.wrong_severity'));
                 return false;
             }
         }
         var modalInstance = $uibModal.open({
             templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
             animation: true,
             backdrop: 'static',
             resolve: { updateData: descData },
             controller: function($scope, $uibModalInstance, updateData){
                 $scope.modalTitle = $translate.instant('confirmmodal.title_description');
                 $scope.ok = function(){
                     //Consumir el servicio
                     var req = projectFtry.UpdateDescription(updateData);
                     //Capturar la Promisse
                     req.then(function(response){
                         if(!response.error){
                             var updated_at = $translate.instant('proj_alerts.updated_title');
                             var updated_ac = $translate.instant('proj_alerts.updated_cont');
                             $msg.success(updated_ac,updated_at);
                             $uibModalInstance.close();
                             location.reload();
                             //Tracking mixpanel
                             mixPanelDashboard.trackFinding("UpdateFinding", userEmail, descData.id);
                         }else{
                           Rollbar.error("Error: An error occurred updating description");
                           var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                           $msg.error(error_ac1);
                         }
                     });
                 };
                 $scope.close = function(){
                     $uibModalInstance.close();
                 };
             }
         });
     };
     $scope.validateTreatment = function(){
       if ($scope.aux.tratamiento !== $scope.finding.tratamiento){
          $scope.finding.razon_tratamiento = '';
       }
     };
     $scope.updateTreatment = function(){
          //Obtener datos
          if ($scope.aux.razon === $scope.finding.razon_tratamiento){
            $msg.error($translate.instant('proj_alerts.differ_comment'));
          } else if ($scope.finding.razon_tratamiento === '') {
            $msg.error($translate.instant('proj_alerts.empty_comment'))
          } else if ($scope.finding.razon_tratamiento.length < 50 || $scope.finding.razon_tratamiento.length > 80) {
            $msg.error($translate.instant('proj_alerts.short_comment'))
          } else {
          $scope.finding.responsable_tratamiento = userEmail;
          newData = {
              id: $scope.finding.id,
              tratamiento: $scope.finding.tratamiento,
              razon_tratamiento: $scope.finding.razon_tratamiento,
              responsable_tratamiento: $scope.finding.responsable_tratamiento,
          };
          var modalInstance = $uibModal.open({
              templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
              animation: true,
              backdrop: 'static',
              resolve: { updateData: newData },
              controller: function($scope, $uibModalInstance, updateData){
                  $scope.modalTitle = $translate.instant('search_findings.tab_description.update_treatmodal');
                  $scope.ok = function(){
                      //Consumir el servicio
                      var req = projectFtry.UpdateTreatment(updateData);
                      //Capturar la Promisse
                      req.then(function(response){
                          if(!response.error){
                              var org = Organization.toUpperCase();
                              var projt = $stateParams.project.toUpperCase();
                              mixPanelDashboard.trackFindingDetailed("FindingUpdateTreatment", userName, userEmail, org, projt, newData.id);
                              $msg.success($translate.instant('proj_alerts.updated_treat'),$translate.instant('proj_alerts.congratulation'));
                              $uibModalInstance.close();
                              location.reload();
                          }else{
                            Rollbar.error("Error: An error occurred updating treatment");
                            var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                            $msg.error(error_ac1);
                          }
                      });
                  };
                  $scope.close = function(){
                      $uibModalInstance.close();
                  };
              }
          });
        }
    };
    $scope.findingSolved = function(){
        //Obtener datos
        descData = {
            user_mail: userEmail,
            finding_name: $scope.finding.hallazgo,
            project: $scope.finding.proyecto_fluid,
            finding_url: window.location.href,
            finding_id: $scope.finding.id,
            finding_vulns: $scope.finding.cardinalidad,
         };
         var modalInstance = $uibModal.open({
             templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
             animation: true,
             backdrop: 'static',
             resolve: { mailData: descData },
             controller: function($scope, $uibModalInstance, mailData){
                 $scope.modalTitle = $translate.instant('search_findings.tab_description.remediated_finding');
                 $scope.ok = function(){
                     //Consumir el servicio
                     var req = projectFtry.FindingSolved(mailData);
                     //Capturar la Promisse
                     req.then(function(response){
                         if(!response.error){
                             //Tracking mixpanel
                             var org = Organization.toUpperCase();
                             var projt = descData.project.toUpperCase();
                             mixPanelDashboard.trackFindingDetailed("FindingRemediated", userName, userEmail, org, projt, descData.finding_id);
                             $msg.success($translate.instant('proj_alerts.remediated_success'));
                             $uibModalInstance.close();
                         }else{
                           Rollbar.error("Error: An error occurred when remediating the finding");
                           $msg.error($translate.instant('proj_alerts.error_textsad'));
                         }
                     });
                 };
                 $scope.close = function(){
                     $uibModalInstance.close();
                 };
             }
         });
       };
    $scope.goBack = function(){
       $scope.view.project = true;
       $scope.view.finding = false;
       $state.go("ProjectNamed", {project: $scope.project});
       $('html, body').animate({ scrollTop: $scope.currentScrollPosition }, 'fast');
     };
    $scope.urlDescription = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/description")
     };
    $scope.urlSeverity = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/severity")
     };
    $scope.urlTracking = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/tracking")
     };
    $scope.urlEvidence = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/evidence")
     };
    $scope.urlExploit = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/exploit")
     };
     $scope.urlComments = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/comments")
     };
    $scope.init = function(){
        var project = $stateParams.project;
        var findingId = $stateParams.finding;
        $scope.userRole = userRole;
        //Control para alternar los campos editables
        $scope.onlyReadableTab1 = true;
        $scope.onlyReadableTab2 = true;
        $scope.onlyReadableTab3 = true;
        $scope.onlyReadableTab4 = true;
        $scope.isManager = userRole != "customer";
        //Defaults para cambiar vistas
        $scope.view = {};
        $scope.view.project = false;
        $scope.view.finding = false;
        //Parametros de ruta
        if(findingId !== undefined) $scope.findingId = findingId;
        if(project != undefined
            && project != "") {
            $scope.project = project;
        }
        //Inicializacion para consulta de hallazgos
        $scope.configColorPalette();
        //Asigna el evento buscar al textbox search y tecla enter
        $scope.configKeyboardView();
        $scope.finding = {};
        $scope.finding = {};
        $scope.finding.id = $stateParams.id;
        $scope.loadFindingByID($stateParams.id);
        $scope.goUp();
        var org = Organization.toUpperCase();
        var projt = project.toUpperCase();
        if (window.location.hash.indexOf('description') !== -1){
          $("#infoItem").addClass("active");
          $("#info").addClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingDescription", userName, userEmail, org, projt, $scope.finding.id);      
        }
        if (window.location.hash.indexOf('severity') !== -1){
          $("#infoItem").removeClass("active");
          $("#info").removeClass("active");
          $("#cssv2Item").addClass("active");
          $("#cssv2").addClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingSeverity", userName, userEmail, org, projt, $scope.finding.id);
        }
        if (window.location.hash.indexOf('tracking') !== -1){
          $("#infoItem").removeClass("active");
          $("#info").removeClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").addClass("active");
          $("#tracking").addClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingTracking", userName, userEmail, org, projt, $scope.finding.id);
        }
        if (window.location.hash.indexOf('evidence') !== -1){
          $("#infoItem").removeClass("active");
          $("#info").removeClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").addClass("active");
          $("#evidence").addClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingEvidence", userName, userEmail, org, projt, $scope.finding.id);
        }
        if (window.location.hash.indexOf('exploit') !== -1){
          $("#infoItem").removeClass("active");
          $("#info").removeClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          $("#exploitItem").addClass("active");
          $("#exploit").addClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingExploit", userName, userEmail, org, projt, $scope.finding.id);
        }
        if (window.location.hash.indexOf('comments') !== -1){
          $("#infoItem").removeClass("active");
          $("#info").removeClass("active");
          $("#cssv2Item").removeClass("active");
          $("#cssv2").removeClass("active");
          $("#trackingItem").removeClass("active");
          $("#tracking").removeClass("active");
          $("#evidenceItem").removeClass("active");
          $("#evidence").removeClass("active");
          $("#exploitItem").removeClass("active");
          $("#exploit").removeClass("active");
          $("#commentItem").addClass("active");
          $("#comment").addClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingComments", userName, userEmail, org, projt, $scope.finding.id);
        }
    };
    $scope.init();
});
