/**
 * @file findingcontentCtrl.js
 * @author engineering@fluid.la
 */
/**
 * Funciones para administrar el UI del resumen de un hallazgo
 * @name findingcontentCtrl.js
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
    $scope.findingExploitTab = function(){
        var url_pre = BASE.url + "get_exploit?id=";
        $scope.hasExploit = false;
        if($scope.finding.exploit !== undefined && $scope.finding.cierres.length == 0){
            var url = url_pre + $scope.finding.exploit;
            var exploit = projectFtry.getExploit(url);
            $scope.hasExploit = true;
            exploit.then(function(response){
                if(!response.error){
                    $scope.exploitURL = response;
                }
            });
        } else {
            $scope.hasExploit = false;
        }
    };
    $scope.loadFindingByID = function(id){
        var findingObj = undefined;
        var req = findingFactory.getVulnById(id);
        req.then(function(response){
            if(!response.error && $stateParams.project == response.data.proyecto_fluid.toLowerCase()){
                $scope.finding = response.data;
                $scope.findingHeaderBuilding();
                $scope.view.project = false;
                $scope.view.finding = true;
                $scope.findingInformationTab();
                $scope.findingEvidenceTab();
                $scope.findingExploitTab();
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
            //Tracking mixpanel
            mixPanelDashboard.trackReadFinding(userEmail, $scope.finding.id);
            $timeout($scope.goUp, 200);
        } else {
          $msg.error("No encontramos el hallazgo!");
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
    $scope.descriptionEditable = function(){
        if($scope.onlyReadableTab1 == false){
            $scope.onlyReadableTab1 = true;
        }else{
            $scope.onlyReadableTab1 = false;
        }
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
        var url_pre = BASE.url + "get_evidence?id=";
        if($scope.finding.animacion !== undefined){
            var url = url_pre + $scope.finding.animacion;
            evidenceList.push({
                "url": url,
                "desc": 'Animación de explotación',
                "ref": 0
            });
        }
        if($scope.finding.explotacion !== undefined){
            var url = url_pre + $scope.finding.explotacion;
            evidenceList.push({
                "url": url,
                "desc": 'Evidencia de explotación',
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
        if($scope.desc_evidencia_3 !== undefined
            && $scope.ruta_evidencia_3 !== undefined){
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
            && $scope.ruta_evidencia_5 !== undefined){
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
    $scope.findingCalculateSeveridad = function(){
        if(!isNaN($scope.finding.severidad)){
            var severidad = parseFloat($scope.finding.severidad);
            if (severidad < 0 || severidad > 5){
                $msg.error("La severidad debe ser un numero de 0 a 5", "error");
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
            $msg.error("La severidad debe ser un numero de 0 a 5", "error");
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
                 $msg.error("Debes calcular correctamente la severidad");
                 return false;
             }
         }
         var modalInstance = $uibModal.open({
             templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
             animation: true,
             backdrop: 'static',
             resolve: { updateData: descData },
             controller: function($scope, $uibModalInstance, updateData){
                 $scope.modalTitle = "Actualizar Descripción";
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
                         }else{
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
    $scope.goBack = function(){
       $scope.view.project = true;
       $scope.view.finding = false;
       $state.go("ProjectNamed", {project: $scope.project});
       $('html, body').animate({ scrollTop: $scope.currentScrollPosition }, 'fast');
     };
    $scope.init = function(){
        var project = $stateParams.project;
        var findingId = $stateParams.finding;
        $scope.userRole = userRole;
        //Control para alternar los campos editables
        $scope.onlyReadableTab1 = true;
        $scope.onlyReadableTab2 = true;
        $scope.onlyReadableTab3 = true;
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
    };
    $scope.init();
});
