/**
 * @file findingcontentCtrl.js
 * @author engineering@fluidattacks.com
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
    $scope.alertHeader = function(company, project){
      var req = projectFtry.getAlerts(company, project);
      req.then(function(response){
          if(!response.error && response.data.length > 0){
            if (response.data[0].status_act=='1'){
               var html = '<div class="alert alert-danger-2">';
               html += '<strong>Atención! </strong>' + response.data[0].message + '</div>';
               document.getElementById('header_alert').innerHTML = html;
             }
           }
         });
       };
    $scope.findingExploitTab = function(){
        $scope.hasExploit = false;
        var exploit;
        var req = projectFtry.getEvidences($scope.finding.id);
        req.then(function(response){
            if(!response.error){
                if(response.data.length > 0){
                    for (var i = 0; i < response.data.length; i++) {
                        if(response.data[i].exploit !== undefined
                            && response.data[i].es_exploit == true
                              && $scope.finding.cierres.length == 0){
                          exploit = projectFtry.getExploit($scope.finding.id, response.data[i].exploit);
                          $scope.hasExploit = true;
                          exploit.then(function(response){
                              if(!response.error){
                                  response = response.replaceAll("<", "&lt;");
                                  response = response.replaceAll(">", "&gt;");
                                  $scope.exploitURL = response;
                              } else {
                                Rollbar.error("Error: An error occurred loading exploit from S3");
                              }
                          });
                        } else if($scope.finding.exploit !== undefined && $scope.finding.cierres.length == 0){
                            exploit = projectFtry.getExploit($scope.finding.id, $scope.finding.exploit);
                            $scope.hasExploit = true;
                            exploit.then(function(response){
                                if(!response.error){
                                    response = response.replaceAll("<", "&lt;");
                                    response = response.replaceAll(">", "&gt;");
                                    $scope.exploitURL = response;
                                } else {
                                  Rollbar.error("Error: An error occurred loading exploit");
                                }
                            });
                        } else {
                            $scope.hasExploit = false;
                        }
                    }
                } else if($scope.finding.exploit !== undefined && $scope.finding.cierres.length == 0){
                            exploit = projectFtry.getExploit($scope.finding.id, $scope.finding.exploit);
                            $scope.hasExploit = true;
                            exploit.then(function(response){
                                if(!response.error){
                                    response = response.replaceAll("<", "&lt;");
                                    response = response.replaceAll(">", "&gt;");
                                    $scope.exploitURL = response;
                                } else {
                                  Rollbar.error("Error: An error occurred loading exploit");
                                }
                            });
                        } else {
                            $scope.hasExploit = false;
                }

            }
        });
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
        var inputs = document.querySelectorAll( '.inputfile' );
        Array.prototype.forEach.call( inputs, function( input )
        {
          var label  = input.nextElementSibling,
            labelVal = label.innerHTML;

          input.addEventListener( 'change', function( e )
          {
            var fileName = '';
            if( this.files && this.files.length > 1 )
              {fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );}
            else
              {fileName = e.target.value.split( '\\' ).pop();}

            if( fileName )
              {label.querySelector( 'span' ).innerHTML = fileName;}
            else
              {label.innerHTML = labelVal;}
          });

          // Firefox bug fix
          input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
          input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
        });
        $scope.evidenceDescription = [$('#evidenceText0').val(), $('#evidenceText1').val(), $('#evidenceText2').val(),
                                      $('#evidenceText3').val(), $('#evidenceText4').val(), $('#evidenceText5').val(),
                                      $('#evidenceText6').val()];
        var refList = []
        for(var i = 0; i < $scope.tabEvidences.length; i++) {
            refList.push($scope.tabEvidences[i].ref);
        }
        var evidencesList = []
        if(refList.indexOf(0) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                "desc": "",
                "ref": 0
            });
        }
        if(refList.indexOf(1) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                "desc": "",
                "ref": 1
            });
        }
        if(refList.indexOf(2) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 1',
                "desc": "",
                "ref": 2
            });
        }
        if(refList.indexOf(3) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 2',
                "desc": "",
                "ref": 3
            });
        }
        if(refList.indexOf(4) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 3',
                "desc": "",
                "ref": 4
            });
        }
        if(refList.indexOf(5) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 4',
                "desc": "",
                "ref": 5
            });
        }
        if(refList.indexOf(6) == -1) {
            $scope.tabEvidences.push({
                "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 5',
                "desc": "",
                "ref": 6
            });
        }
        $scope.tabEvidences.sort(function (a, b) {
          return a.ref - b.ref;
        });
    };
    $scope.treatmentEditable = function(){
      $scope.goDown()
      if($scope.onlyReadableTab4 == false){
          $scope.finding.responsable_tratamiento = userEmail;
          $scope.onlyReadableTab4 = true;
          $scope.finding.tratamiento = $scope.aux.tratamiento
          $scope.finding.razon_tratamiento = $scope.aux.razon
          $scope.finding.bts_externo = $scope.aux.bts
      }else if($scope.onlyReadableTab4 == true){
          $scope.finding.tratamiento = $scope.aux.tratamiento
          $scope.finding.razon_tratamiento = $scope.aux.razon
          $scope.finding.responsable_tratamiento = $scope.aux.responsable
          $scope.finding.bts_externo = $scope.aux.bts
          $scope.onlyReadableTab4 = false;
      }
    };
    $scope.exploitEditable = function(){
        if($scope.onlyReadableTab5 == false){
            $scope.onlyReadableTab5 = true;
        }else{
            $scope.onlyReadableTab5 = false;
        }
        var inputs = document.querySelectorAll( '.inputfile' );
        Array.prototype.forEach.call( inputs, function( input )
        {
          var label  = input.nextElementSibling,
            labelVal = label.innerHTML;

          input.addEventListener( 'change', function( e )
          {
            var fileName = '';
            if( this.files && this.files.length > 1 )
              {fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );}
            else
              {fileName = e.target.value.split( '\\' ).pop();}

            if( fileName )
              {label.querySelector( 'span' ).innerHTML = fileName;}
            else
              {label.innerHTML = labelVal;}
          });

          // Firefox bug fix
          input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
          input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
        });
    };
    $scope.recordsEditable = function(){
        if($scope.onlyReadableTab6 == false){
            $scope.onlyReadableTab6 = true;
        }else{
            $scope.onlyReadableTab6 = false;
        }
        var inputs = document.querySelectorAll( '.inputfile' );
        Array.prototype.forEach.call( inputs, function( input )
        {
          var label  = input.nextElementSibling,
            labelVal = label.innerHTML;

          input.addEventListener( 'change', function( e )
          {
            var fileName = '';
            if( this.files && this.files.length > 1 )
              {fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );}
            else
              {fileName = e.target.value.split( '\\' ).pop();}

            if( fileName )
              {label.querySelector( 'span' ).innerHTML = fileName;}
            else
              {label.innerHTML = labelVal;}
          });

          // Firefox bug fix
          input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
          input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
        });
    };
    $scope.detectNivel = function (){
        $timeout(function(){
            $scope.$apply();
            if($scope.finding.nivel == "Detallado"){
                $scope.esDetallado = true;
            }else{
                $scope.esDetallado = false;
            }
        },200);
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
    updateEvidencesFiles = function(element){
        var error_ac1;
        var evImage = $(element).attr('target');
        var data = {};
        data.document = $('#evidence'+ evImage).val();
        if(data.document == ""){
            error_ac1 = $translate.instant('proj_alerts.error_textsad');
            $msg.error(error_ac1);
            return false;
        }
        var data = new FormData();
        var fileInput = $('#evidence'+ evImage)[0];
        data.append("id", evImage);
        data.append("url", $stateParams.project.toLowerCase() + "-" + $scope.finding.id);
        data.append("findingId", $scope.finding.id);
        data.append("document", fileInput.files[0]);
        fileName = fileInput.files[0].name;
        dots = fileName.split(".");
        fileType = "." + dots[dots.length-1];
        if((fileType == ".png" || fileType == ".PNG") && fileInput.files[0].size > 2097152){
            error_ac1 = $translate.instant('proj_alerts.file_size_png');
            $msg.error(error_ac1);
            return false;
        }
        if((fileType == ".gif" || fileType == ".GIF") && fileInput.files[0].size > 10485760){
            error_ac1 = $translate.instant('proj_alerts.file_size');
            $msg.error(error_ac1);
            return false;
        }
        if((fileType == ".py" || fileType == ".PY") && fileInput.files[0].size > 1048576){
            error_ac1 = $translate.instant('proj_alerts.file_size_py');
            $msg.error(error_ac1);
            return false;
        }
        if((fileType == ".csv" || fileType == ".CSV") && fileInput.files[0].size > 1048576){
            error_ac1 = $translate.instant('proj_alerts.file_size_py');
            $msg.error(error_ac1);
            return false;
        }
        evImages = ['1', '2', '3', '4', '5', '6'];
        if(evImage == '0' && (fileType != ".gif" && fileType != ".GIF")){
            error_ac1 = $translate.instant('proj_alerts.file_type_gif');
            $msg.error(error_ac1);
            return false;
        } else if (evImage == '7' && (fileType != ".py"  && fileType != ".PY")){
            error_ac1 = $translate.instant('proj_alerts.file_type_py');
            $msg.error(error_ac1);
            return false;
        } else if (evImage == '8' && (fileType != ".csv"  && fileType != ".CSV")){
            error_ac1 = $translate.instant('proj_alerts.file_type_csv');
            $msg.error(error_ac1);
            return false;
        } else if(evImages.indexOf(evImage) != -1 && (fileType != ".png" && fileType != ".PNG")){
            error_ac1 = $translate.instant('proj_alerts.file_type_png');
            $msg.error(error_ac1);
            return false;
        }
        var responseFunction = function(response){
          if(!response.error){
              var updated_at = $translate.instant('proj_alerts.updated_title');
              var updated_ac = $translate.instant('proj_alerts.updated_cont_file');
              $msg.success(updated_ac,updated_at);
              location.reload();
              return true;
          } else {
              error_ac1 = $translate.instant('proj_alerts.no_file_update');
              Rollbar.error("Error: An error occurred updating evidences");
              $msg.error(error_ac1);
              return false;
          }
        };
        var errorFunction = function(response){
          if(!response.error){
              error_ac1 = $translate.instant('proj_alerts.no_file_update');
              Rollbar.error("Error: An error occurred updating evidences");
              $msg.error(error_ac1);
              return false;
          }
        };
        projectFtry.UpdateEvidenceFiles(data, responseFunction, errorFunction);
    };
    updateEvidenceText = function(element){
        var evImage = $(element).attr('target');
        var data = {}
        data.id = $scope.finding.id;
        var description = $('#evidenceText' + evImage).val();
        var file = $('#evidence'+ evImage).val();
        if(description == '' || $scope.evidenceDescription[evImage] == description){
            if(file != ''){
                updateEvidencesFiles(element);
            } else {
                return false;
            }
        } else {
            if(evImage == '2'){
              data.desc_evidencia_1 = description;
              data.field = "desc_evidencia_1";
            }
            if(evImage == '3'){
                data.desc_evidencia_2 = description;
                data.field = "desc_evidencia_2";
            }
            if(evImage == '4'){
                data.desc_evidencia_3 = description;
                data.field = "desc_evidencia_3";
            }
            if(evImage == '5'){
                data.desc_evidencia_4 = description;
                data.field = "desc_evidencia_4";
            }
            if(evImage == '6'){
                data.desc_evidencia_5 = description;
                data.field = "desc_evidencia_5";
            }
            var req = projectFtry.UpdateEvidenceText(data);
            //Capturar la Promisse
            req.then(function(response){
                if(!response.error){
                    var updated_at = $translate.instant('proj_alerts.updated_title');
                    var updated_ac = $translate.instant('proj_alerts.updated_cont_description');
                    $msg.success(updated_ac,updated_at);
                    if(file != ''){
                        updateEvidencesFiles(element);
                    } else {
                        location.reload();
                    }
                    return true;
                } else {
                    var error_ac1 = $translate.instant('proj_alerts.no_text_update');
                    Rollbar.error("Error: An error occurred updating evidences description");
                    $msg.error(error_ac1);
                    return false;
                }
            });
        }
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
    $scope.goDown = function(){
         window.scrollTo(0,document.body.scrollHeight);
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
                if($scope.finding.tratamiento == "Asumido"){
                  $scope.isAssumed = true;
                } else {
                  $scope.isAssumed = false;
                }
                if($scope.finding.estado == "Cerrado"){
                  $scope.isClosed = true;
                } else {
                  $scope.isClosed = false;
                }
                if($scope.finding.suscripcion == "Continua" || $scope.finding.suscripcion == "Concurrente" || $scope.finding.suscripcion == "Si"){
                  $scope.isContinuous = true;
                } else {
                  $scope.isContinuous = false;
                }
                if($scope.finding.suscripcion != 'Concurrente' && $scope.finding.suscripcion != 'Puntual' && $scope.finding.suscripcion != 'Continua'){
                  Rollbar.warning("Warning: Finding " + id + " without type");
                }
                $scope.aux.responsable = $scope.finding.responsable_tratamiento;
                $scope.aux.bts = $scope.finding.bts_externo;
                   switch ($scope.finding.actor) {
                     case "​Cualquier persona en Internet":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_internet');
                       break;
                     case "Cualquier cliente de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_costumer');
                       break;
                     case "Solo algunos clientes de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.some_costumer');
                       break;
                     case "Cualquier persona con acceso a la estación":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_access');
                       break;
                     case "Cualquier empleado de la organización":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.any_employee');
                       break;
                     case "Solo algunos empleados":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.some_employee');
                       break;
                     case "Solo un empleado":
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.one_employee');
                       break;
                     default:
                       $scope.finding.actor = $translate.instant('finding_formstack.actor.default');
                   }
                   switch ($scope.finding.autenticacion) {
                     case "0.704 | Ninguna: No se requiere autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.any_authen');
                       break;
                     case "0.560 | Única: Único punto de autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.single_authen');
                       break;
                     case "0.450 | Multiple: Multiples puntos de autenticación":
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.multiple_authen');
                       break;
                     default:
                       $scope.finding.autenticacion = $translate.instant('finding_formstack.authentication.default');
                   }
                   switch ($scope.finding.categoria) {
                     case "Actualizar y configurar las líneas base de seguridad de los componentes":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.update_base');
                       break;
                     case "Definir el modelo de autorización considerando el principio de mínimo privilegio":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.define_model');
                       break;
                     case "Desempeño":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.performance');
                       break;
                     case "Eventualidad":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.event');
                       break;
                     case "Evitar exponer la información técnica de la aplicación, servidores y plataformas":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.avoid_technical');
                       break;
                     case "Excluir datos sensibles del código fuente y del registro de eventos":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.exclude_finding');
                       break;
                     case "Fortalecer controles en autenticación y manejo de sesión":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_authen');
                       break;
                     case "Fortalecer controles en el procesamiento de archivos":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_process');
                       break;
                     case "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.strengt_protect');
                       break;
                     case "Implementar controles para validar datos de entrada":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.validate_input');
                       break;
                     case "Mantenibilidad":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.maintain');
                       break;
                     case "Registrar eventos para trazabilidad y auditoría":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.record_event');
                       break;
                     case "Utilizar protocolos de comunicación seguros":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.secure_protoc');
                       break;
                     case "Validar la integridad de las transacciones en peticiones HTTP":
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.validate_http');
                       break;
                     default:
                       $scope.finding.categoria = $translate.instant('finding_formstack.category.default');
                   }
                   switch ($scope.finding.complejidad_acceso) {
                     case "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.high_complex');
                       break;
                     case "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.medium_complex');
                       break;
                     case "0.710 | Bajo: No se requiere ninguna condición especial":
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.low_complex');
                       break;
                     default:
                       $scope.finding.complejidad_acceso = $translate.instant('finding_formstack.complexity.default');
                   }
                   switch ($scope.finding.escenario) {
                     case "Anónimo desde Internet":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.anon_inter');
                       break;
                     case "Anónimo desde Intranet":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.anon_intra');
                       break;
                     case "Escaneo de Infraestructura":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.infra_scan');
                       break;
                     case "Extranet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_extra');
                       break;
                     case "Internet usuario autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.auth_inter');
                       break;
                     case "Internet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_inter');
                       break;
                     case "Intranet usuario autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.auth_intra');
                       break;
                     case "Intranet usuario no autorizado":
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.unauth_inter');
                        break;
                     default:
                       $scope.finding.escenario = $translate.instant('finding_formstack.scenario.default');
                   }
                   switch ($scope.finding.estado) {
                     case "Abierto":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.open');
                       break;
                     case "Cerrado":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.close');
                       break;
                     case "Parcialmente cerrado":
                       $scope.finding.estado = $translate.instant('finding_formstack.status.part_close');
                       break;
                     default:
                       $scope.finding.estado = $translate.instant('finding_formstack.status.default');
                   }
                   switch ($scope.finding.explotabilidad) {
                     case "0.850 | Improbable: No existe un exploit":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.improbable');
                       break;
                     case "0.900 | Conceptual: Existen pruebas de laboratorio":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.conceptual');
                       break;
                     case "0.950 | Funcional: Existe exploit":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.functional');
                       break;
                     case "1.000 | Alta: No se requiere exploit o se puede automatizar":
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.high');
                       break;
                     default:
                       $scope.finding.explotabilidad = $translate.instant('finding_formstack.exploitability.default');
                   }
                   switch ($scope.finding.explotable) {
                     case "Si":
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.yes');
                       break;
                     case "No":
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.no');
                       break;
                     default:
                       $scope.finding.explotable = $translate.instant('finding_formstack.exploitable.default');
                   }
                   switch ($scope.finding.impacto_confidencialidad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.none');
                       break;
                     case "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.partial');
                       break;
                     case "0.660 | Completo: Se controla toda la información relacionada con el objetivo":
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.complete');
                       break;
                     default:
                       $scope.finding.impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.default');
                   }
                   switch ($scope.finding.impacto_disponibilidad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.none');
                       break;
                     case "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.partial');
                       break;
                     case "0.660 | Completo: Hay una caída total del objetivo":
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.complete');
                       break;
                     default:
                       $scope.finding.impacto_disponibilidad = $translate.instant('finding_formstack.availability.default');
                   }
                   switch ($scope.finding.impacto_integridad) {
                     case "0 | Ninguno: No se presenta ningún impacto":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.none');
                       break;
                     case "0.275 | Parcial: Es posible modificar cierta información del objetivo":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.partial');
                       break;
                     case "0.660 | Completo: Es posible modificar toda la información del objetivo":
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.complete');
                       break;
                     default:
                       $scope.finding.impacto_integridad = $translate.instant('finding_formstack.integrity.default');
                   }
                   switch ($scope.finding.nivel_confianza) {
                     case "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.not_confirm');
                       break;
                     case "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.not_corrob');
                       break;
                     case "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante":
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.confirmed');
                       break;
                     default:
                       $scope.finding.nivel_confianza = $translate.instant('finding_formstack.confidence.default');
                   }
                   switch ($scope.finding.nivel_resolucion) {
                     case "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.palliative');
                       break;
                     case "0.870 | Oficial: Existe un parche disponible por el fabricante":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.official');
                       break;
                     case "0.900 | Temporal: Existen soluciones temporales":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.temporal');
                       break;
                     case "1.000 | Inexistente: No existe solución":
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.non_existent');
                       break;
                     default:
                       $scope.finding.nivel_resolucion = $translate.instant('finding_formstack.resolution.default');
                   }
                   switch ($scope.finding.probabilidad) {
                     case "100% Vulnerado Anteriormente":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.prev_vuln');
                       break;
                     case "75% Fácil de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.easy_vuln');
                       break;
                     case "50% Posible de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.possible_vuln');
                       break;
                     case "25% Difícil de vulnerar":
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.diffic_vuln');
                       break;
                     default:
                       $scope.finding.probabilidad = $translate.instant('finding_formstack.probability.default');
                   }
                   switch ($scope.finding.tipo_hallazgo_cliente) {
                     case "Higiene":
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.hygiene');
                       break;
                     case "Vulnerabilidad":
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.vuln');
                       break;
                     default:
                       $scope.finding.tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.default');
                   }
                   switch ($scope.finding.tipo_prueba) {
                     case "Análisis":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.analysis');
                       break;
                     case "Aplicación":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.app');
                       break;
                     case "Binario":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.binary');
                       break;
                     case "Código":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.code');
                       break;
                     case "Infraestructura":
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.infras');
                       break;
                     default:
                       $scope.finding.tipo_prueba = $translate.instant('finding_formstack.test_method.default');
                   }
                   switch ($scope.finding.vector_acceso) {
                     case "0.646 | Red adyacente: Explotable desde el mismo segmento de red":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.adjacent');
                       break;
                     case "1.000 | Red: Explotable desde Internet":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.network');
                       break;
                     case "0.395 | Local: Explotable con acceso local al objetivo":
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.local');
                       break;
                     default:
                       $scope.finding.vector_acceso = $translate.instant('finding_formstack.access_vector.default');
                   }
                   switch ($scope.finding.tratamiento) {
                     case "Asumido":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.asummed');
                       break;
                     case "Pendiente":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.working');
                       break;
                     case "Remediar":
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.remediated');
                       break;
                     default:
                       $scope.finding.tratamiento = $translate.instant('finding_formstack.treatment_header.default');
                   }
                $scope.findingHeaderBuilding();
                $scope.remediatedView();
                $scope.view.project = false;
                $scope.view.finding = true;
                $scope.findingInformationTab();
                $scope.findingEvidenceTab();
                $scope.findingExploitTab();
                $scope.findingRecordsTab();
                $scope.findingCommentTab();
                //Control de campos para tipos de hallazgo
                $scope.esDetallado = false;
                if($scope.finding.nivel == "Detallado"){
                  $scope.esDetallado = true;
                }
                //Control de campos editables
                $scope.onlyReadableTab1 = true;
                $scope.onlyReadableTab2 = true;
                $scope.isManager = userRole != "customer";
                if(!$scope.isManager && !$scope.isAssumed && !$scope.isClosed && $scope.isContinuous){
                  $('.finding-treatment').show();
                } else {
                  $('.finding-treatment').hide();
                }
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
        var BaseScore = (0.6*(10.41*(1-(1-ImpCon)*(1-ImpInt)*(1-ImpDis)))+0.4*(20*AccCom*Auth*AccVec)-1.5)*1.176;
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
        var url;
        var evidenceList = [];
        var url_pre = window.location.href.split('dashboard#!/')[0] + window.location.href.split('dashboard#!/')[1] + '/';
        var req = projectFtry.getEvidences($scope.finding.id);
        req.then(function(response){
            if(!response.error){
              if(response.data.length > 0){
                  for (var i = 0; i < response.data.length; i++) {
                      if(response.data[i].animacion !== undefined && response.data[i].es_animacion == true){
                          url = url_pre + response.data[i].animacion;
                          evidenceList.push({
                              "url": url,
                              "name": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                              "desc": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                              "ref": 0
                          });
                      } else if($scope.finding.animacion !== undefined){
                          url = url_pre + $scope.finding.animacion;
                          evidenceList.push({
                              "url": url,
                              "name": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                              "desc": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                              "ref": 0
                          });
                      }
                      if(response.data[i].explotacion !== undefined && response.data[i].es_explotacion == true){
                          url = url_pre + response.data[i].explotacion;
                          evidenceList.push({
                              "url": url,
                              "name": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                              "desc": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                              "ref": 1
                          });
                      } else if($scope.finding.explotacion !== undefined){
                          url = url_pre + $scope.finding.explotacion;
                          evidenceList.push({
                              "url": url,
                              "name": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                              "desc": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                              "ref": 1
                          });
                      }
                      if($scope.finding.desc_evidencia_1 !== undefined
                          && response.data[i].ruta_evidencia_1 !== undefined
                            && response.data[i].es_ruta_evidencia_1 == true){
                          url = url_pre + response.data[i].ruta_evidencia_1;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 1',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_1
                              ),
                              "ref": 2
                          });
                      } else if($scope.finding.desc_evidencia_1 !== undefined
                          && $scope.finding.ruta_evidencia_1 !== undefined){
                          url = url_pre + $scope.finding.ruta_evidencia_1;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 1',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_1
                              ),
                              "ref": 2
                          });
                      }
                      if($scope.finding.desc_evidencia_2 !== undefined
                          && response.data[i].ruta_evidencia_2 !== undefined
                            && response.data[i].es_ruta_evidencia_2 == true){
                          url = url_pre + response.data[i].ruta_evidencia_2;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 2',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_2
                              ),
                              "ref": 3
                          });
                      } else if($scope.finding.desc_evidencia_2 !== undefined
                          && $scope.finding.ruta_evidencia_2 !== undefined){
                          url = url_pre + $scope.finding.ruta_evidencia_2;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 2',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_2
                              ),
                              "ref": 3
                          });
                      }
                      if($scope.finding.desc_evidencia_3 !== undefined
                          && response.data[i].ruta_evidencia_3 !== undefined
                            && response.data[i].es_ruta_evidencia_3 == true){
                          url = url_pre + response.data[i].ruta_evidencia_3;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 3',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_3
                              ),
                              "ref": 4
                          });
                      } else if($scope.finding.desc_evidencia_3 !== undefined
                          && $scope.finding.ruta_evidencia_3 !== undefined){
                          url = url_pre + $scope.finding.ruta_evidencia_3;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 3',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_3
                              ),
                              "ref": 4
                          });
                      }
                      if($scope.finding.desc_evidencia_4 !== undefined
                          && response.data[i].ruta_evidencia_4 !== undefined
                            && response.data[i].es_ruta_evidencia_4 == true){
                          url = url_pre + response.data[i].ruta_evidencia_4;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 4',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_4
                              ),
                              "ref": 5
                          });
                      } else if($scope.finding.desc_evidencia_4 !== undefined
                          && $scope.finding.ruta_evidencia_4 !== undefined){
                          url = url_pre + $scope.finding.ruta_evidencia_4;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 4',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_4
                              ),
                              "ref": 5
                          });
                      }
                      if($scope.finding.desc_evidencia_5 !== undefined
                          && response.data[i].ruta_evidencia_5 !== undefined
                            && response.data[i].es_ruta_evidencia_5 == true){
                          url = url_pre + response.data[i].ruta_evidencia_5;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 5',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_5
                              ),
                              "ref": 6
                          });
                      } else if($scope.finding.desc_evidencia_5 !== undefined
                          && $scope.finding.ruta_evidencia_5 !== undefined){
                          url = url_pre + $scope.finding.ruta_evidencia_5;
                          evidenceList.push({
                              "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 5',
                              "url": url,
                              "desc": $scope.capitalizeFirstLetter(
                                  $scope.finding.desc_evidencia_5
                              ),
                              "ref": 6
                          });
                      }
                      $scope.tabEvidences = evidenceList;
                  }
              } else {
                  if($scope.finding.animacion !== undefined){
                        url = url_pre + $scope.finding.animacion;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                            "desc": $translate.instant('search_findings.tab_evidence.animation_exploit'),
                            "ref": 0
                        });
                    }
                    if($scope.finding.explotacion !== undefined){
                        url = url_pre + $scope.finding.explotacion;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                            "desc": $translate.instant('search_findings.tab_evidence.evidence_exploit'),
                            "ref": 1
                        });
                    }
                    if($scope.finding.desc_evidencia_1 !== undefined
                        && $scope.finding.ruta_evidencia_1 !== undefined){
                        url = url_pre + $scope.finding.ruta_evidencia_1;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 1',
                            "desc": $scope.capitalizeFirstLetter(
                                $scope.finding.desc_evidencia_1
                            ),
                            "ref": 2
                        });
                    }
                    if($scope.finding.desc_evidencia_2 !== undefined
                        && $scope.finding.ruta_evidencia_2 !== undefined){
                        url = url_pre + $scope.finding.ruta_evidencia_2;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 2',
                            "desc": $scope.capitalizeFirstLetter(
                                $scope.finding.desc_evidencia_2
                            ),
                            "ref": 3
                        });
                    }
                    if($scope.finding.desc_evidencia_3 !== undefined
                        && $scope.finding.ruta_evidencia_3 !== undefined){
                        url = url_pre + $scope.finding.ruta_evidencia_3;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 3',
                            "desc": $scope.capitalizeFirstLetter(
                                $scope.finding.desc_evidencia_3
                            ),
                            "ref": 4
                        });
                    }
                    if($scope.finding.desc_evidencia_4 !== undefined
                        && $scope.finding.ruta_evidencia_4 !== undefined){
                        url = url_pre + $scope.finding.ruta_evidencia_4;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 4',
                            "desc": $scope.capitalizeFirstLetter(
                                $scope.finding.desc_evidencia_4
                            ),
                            "ref": 5
                        });
                    }
                    if($scope.finding.desc_evidencia_5 !== undefined
                        && $scope.finding.ruta_evidencia_5 !== undefined){
                        url = url_pre + $scope.finding.ruta_evidencia_5;
                        evidenceList.push({
                            "url": url,
                            "name": $translate.instant('search_findings.tab_evidence.evidence_name') + ' 5',
                            "desc": $scope.capitalizeFirstLetter(
                                $scope.finding.desc_evidencia_5
                            ),
                            "ref": 6
                        });
                    }
                    $scope.tabEvidences = evidenceList;
              }
            } else {
               Rollbar.error("Error: An error occurred loading evidences");
            }
        });

    };
    $scope.findingCommentTab = function(){
        if($scope.finding.id !== undefined){
            var comments = projectFtry.getComments($scope.finding.id);
            comments.then(function(response){
                if(!response.error){
                    var usersArray = []
                    for (var i = 0; i < response.data.length; i++) {
                      var user = {fullname: "", email: ""};
                      user.fullname = response.data[i].fullname;
                      user.email = response.data[i].email;
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
                        data.id = parseInt(Math.round(new Date()/1000).toString() + (Math.random() * 10000).toString(9));
                        data.finding_name = $scope.finding.hallazgo;
                        data.project = $scope.finding.proyecto_fluid;
                        data.finding_url = window.location.href;
                        data.remediated = false;
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
    $scope.findingRecordsTab = function(){
        $scope.hasRecords = false;
        var vlang;
        var record;
        var req = projectFtry.getEvidences($scope.finding.id);
        req.then(function(response){
            if(!response.error){
                if(localStorage.lang === "en"){
                  vlang = 'en-US';
                } else {
                  vlang = 'es-CO';
                }
                if(response.data.length > 0){
                    for (var i = 0; i < response.data.length; i++) {
                        if(response.data[i].registros_archivo !== undefined
                            && response.data[i].es_registros_archivo == true){
                            record = projectFtry.getRecords($scope.finding.id, response.data[i].registros_archivo);
                            $scope.hasRecords = true;
                            record.then(function(response){
                                if(!response.error){
                                    var dataCols = []
                                    for(var i in response.data[0]){
                                        dataCols.push({
                                            field: i,
                                            title: i
                                        });
                                    }
                                    $("#recordsTable").bootstrapTable('destroy');
                                    $("#recordsTable").bootstrapTable({
                                        locale: vlang,
                                        columns: dataCols,
                                        data: response.data,
                                        cookieIdTable: "recordsTableCookie",
                                        cookie: true
                                    });
                                    $("#recordsTable").bootstrapTable('refresh');
                                } else {
                                    Rollbar.error("Error: An error occurred loading record from S3");
                                    var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                                    $msg.error(error_ac1);
                                }
                            });
                        } else if($scope.finding.registros_archivo !== undefined){
                            record = projectFtry.getRecords($scope.finding.id, $scope.finding.registros_archivo);
                            $scope.hasRecords = true;
                            record.then(function(response){
                                if(!response.error){
                                    var dataCols = []
                                    for(var i in response.data[0]){
                                        dataCols.push({
                                            field: i,
                                            title: i
                                        });
                                    }
                                    $("#recordsTable").bootstrapTable('destroy');
                                    $("#recordsTable").bootstrapTable({
                                        locale: vlang,
                                        columns: dataCols,
                                        data: response.data,
                                        cookieIdTable: "recordsTableCookie",
                                        cookie: true
                                    });
                                    $("#recordsTable").bootstrapTable('refresh');
                                } else {
                                    Rollbar.error("Error: An error occurred loading record");
                                    var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                                    $msg.error(error_ac1);
                                }
                            });
                        } else {
                            $scope.hasRecords = false;
                        }
                    }
                } else if($scope.finding.registros_archivo !== undefined){
                        record = projectFtry.getRecords($scope.finding.id, $scope.finding.registros_archivo);
                        $scope.hasRecords = true;
                        record.then(function(response){
                            if(!response.error){
                                var dataCols = []
                                for(var i in response.data[0]){
                                    dataCols.push({
                                        field: i,
                                        title: i
                                    });
                                }
                                $("#recordsTable").bootstrapTable('destroy');
                                $("#recordsTable").bootstrapTable({
                                    locale: vlang,
                                    columns: dataCols,
                                    data: response.data,
                                    cookieIdTable: "recordsTableCookie",
                                    cookie: true
                                });
                                $("#recordsTable").bootstrapTable('refresh');
                            } else {
                                Rollbar.error("Error: An error occurred loading record");
                                var error_ac1 = $translate.instant('proj_alerts.error_textsad');
                                $msg.error(error_ac1);
                            }
                        });
                    } else {
                        $scope.hasRecords = false;
                }

            }
        });
    };
    $scope.findingCalculateSeveridad = function(){
        var severidad;
        if(!isNaN($scope.finding.severidad)){
            severidad = parseFloat($scope.finding.severidad);
            if (severidad < 0 || severidad > 5){
                Rollbar.error("Error: Severity must be an integer bewteen 0 and 5");
                $msg.error($translate.instant('proj_alerts.error_severity'), "error");
                return false;
            }
            try{
                var prob = $scope.finding.probabilidad;
                severidad = $scope.finding.severidad;
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
             registros: $scope.finding.registros,
             registros_num: $scope.finding.registros_num,
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
       if ($scope.aux.razon === $scope.finding.razon_tratamiento){
         $msg.error($translate.instant('proj_alerts.differ_comment'));
         return 'false'
       } else if ($scope.finding.razon_tratamiento === '') {
         $msg.error($translate.instant('proj_alerts.empty_comment'))
         return 'false'
       } else if ($scope.finding.razon_tratamiento.length < 50  || $scope.finding.razon_tratamiento.length > 80) {
         $msg.error($translate.instant('proj_alerts.short_comment'))
         return 'false'
       } else {
          $scope.finding.responsable_tratamiento = userEmail;
          return 'true' }
     };
     $scope.updateTreatment = function(){
          var flag = 'false';
          if ($scope.finding.tratamiento === 'Pendiente' && $scope.aux.razon !== $scope.finding.razon_tratamiento) {
            if ($scope.validateTreatment()==='true') {
              flag = 'true'
            } else { flag = 'false' }
        } else if ($scope.finding.tratamiento !== 'Pendiente' && $scope.aux.razon !== $scope.finding.razon_tratamiento ||
          $scope.finding.tratamiento !== 'Pendiente' && $scope.aux.razon === $scope.finding.razon_tratamiento) {
              if ($scope.validateTreatment()==='true') {
                flag = 'true'
              } else { flag = 'false' }
        } else if ($scope.finding.tratamiento === 'Pendiente' && $scope.aux.razon === $scope.finding.razon_tratamiento) {
              flag = 'true'
          }
          if (flag === 'true'){
            newData = {
              id: $scope.finding.id,
              tratamiento: $scope.finding.tratamiento,
              razon_tratamiento: $scope.finding.razon_tratamiento,
              responsable_tratamiento: $scope.finding.responsable_tratamiento,
              bts_externo: $scope.finding.bts_externo,
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
             templateUrl: BASE.url + 'assets/views/project/remediatedMdl.html',
             animation: true,
             backdrop: 'static',
             resolve: { mailData: descData },
             controller: function($scope, $uibModalInstance, mailData){
                $scope.remediatedData = {}
                 $scope.modalTitle = $translate.instant('search_findings.tab_description.remediated_finding');
                 $scope.ok = function(){
                    $scope.remediatedData.user_mail = mailData.user_mail;
                    $scope.remediatedData.finding_name = mailData.finding_name;
                    $scope.remediatedData.project = mailData.project;
                    $scope.remediatedData.finding_url = mailData.finding_url;
                    $scope.remediatedData.finding_id = mailData.finding_id;
                    $scope.remediatedData.finding_vulns = mailData.finding_vulns;
                    $scope.remediatedData.justification = $scope.remediatedData.justification.trim();
                    if($scope.remediatedData.justification.length < 100) {
                      $msg.error($translate.instant('proj_alerts.short_remediated_comment'));
                    } else {
                      //Consumir el servicio
                      var req = projectFtry.FindingSolved($scope.remediatedData);
                      //Capturar la Promisse
                      req.then(function(response){
                          if(!response.error){
                              //Tracking mixpanel
                              var org = Organization.toUpperCase();
                              var projt = descData.project.toUpperCase();
                              mixPanelDashboard.trackFindingDetailed("FindingRemediated", userName, userEmail, org, projt, descData.finding_id);
                              $scope.remediated = response.data.remediated;
                              $msg.success($translate.instant('proj_alerts.remediated_success'));
                              $uibModalInstance.close();
                              location.reload();
                              var data = {};
                              data.id = parseInt(Math.round(new Date()/1000).toString() + (Math.random() * 10000).toString(9));
                              data.content = $scope.remediatedData.justification;
                              data.parent = 0;
                              data.email = $scope.remediatedData.user_mail;
                              data.finding_name = $scope.remediatedData.finding_name;
                              data.project = $scope.remediatedData.project;
                              data.finding_url = $scope.remediatedData.finding_url;
                              data.remediated = true;
                              var comment = projectFtry.addComment($scope.remediatedData.finding_id, data);
                          }else{
                            Rollbar.error("Error: An error occurred when remediating the finding");
                            $msg.error($translate.instant('proj_alerts.error_textsad'));
                         }
                      });
                    }

                 };
                 $scope.close = function(){
                     $uibModalInstance.close();
                 };
             }
         });
       };
    $scope.remediatedView = function(){
        $scope.isManager = userRole != "customer";
        $scope.isRemediated = true;
        if($scope.finding.id !== undefined){
            var req = projectFtry.RemediatedView($scope.finding.id);
            req.then(function(response){
                if(!response.error){
                  $scope.isRemediated = response.data.remediated;
                  if($scope.isManager && $scope.isRemediated){
                    $('.finding-verified').show();
                  } else {
                    $('.finding-verified').hide();
                  }
                } else {
                  Rollbar.error("Error: An error occurred when remediating/verifying the finding");
                }
            });
        }
    };
    $scope.findingVerified = function(){
        //Obtener datos
        var currUrl = window.location.href;
        var trackingUrl = currUrl.replace("/description", "/tracking");
        descData = {
            user_mail: userEmail,
            finding_name: $scope.finding.hallazgo,
            project: $scope.finding.proyecto_fluid,
            finding_url: trackingUrl,
            finding_id: $scope.finding.id,
            finding_vulns: $scope.finding.cardinalidad,
        };
        var modalInstance = $uibModal.open({
            templateUrl: BASE.url + 'assets/views/project/confirmMdl.html',
            animation: true,
            backdrop: 'static',
            resolve: { mailData: descData },
            controller: function($scope, $uibModalInstance, mailData){
                $scope.modalTitle = $translate.instant('search_findings.tab_description.verified_finding');
                $scope.ok = function(){
                    //Consumir el servicio
                    var req = projectFtry.FindingVerified(mailData);
                    //Capturar la Promisse
                    req.then(function(response){
                        if(!response.error){
                            //Tracking mixpanel
                            var org = Organization.toUpperCase();
                            var projt = descData.project.toUpperCase();
                            mixPanelDashboard.trackFindingDetailed("FindingVerified", userName, userEmail, org, projt, descData.finding_id);
                            var updated_at = $translate.instant('proj_alerts.updated_title');
                            var updated_ac = $translate.instant('proj_alerts.verified_success');
                            $msg.success(updated_ac,updated_at);
                            $uibModalInstance.close();
                            location.reload();
                        }else{
                          Rollbar.error("Error: An error occurred when verifying the finding");
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
    $scope.urlRecords = function(){
        location.replace(window.location.href.split($stateParams.id)[0] + $stateParams.id + "/records")
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
        $scope.onlyReadableTab5 = true;
        $scope.onlyReadableTab6 = true;
        $scope.isManager = userRole != "customer";
        //Defaults para cambiar vistas
        $scope.view = {};
        $scope.view.project = false;
        $scope.view.finding = false;
        //Parametros de ruta
        if(findingId !== undefined) {$scope.findingId = findingId;}
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
        $scope.alertHeader(org, projt);
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
        if (window.location.hash.indexOf('records') !== -1){
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
          $("#commentItem").removeClass("active");
          $("#comment").removeClass("active");
          $("#recordsItem").addClass("active");
          $("#records").addClass("active");
          //Tracking mixpanel
          mixPanelDashboard.trackFindingDetailed("FindingRecords", userName, userEmail, org, projt, $scope.finding.id);
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
