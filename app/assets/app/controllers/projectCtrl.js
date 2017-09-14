/**
 * @file ProjectCtrl.js
 * @author engineering@fluid.la
 */
/**
 * Controlador de vista de proyectos
 * @name ProjectCtrl 
 * @param {Object} $scope 
 * @param {Object} $uibModal
 * @param {Object} $stateParams
 * @param {Object} $state
 * @param {Object} $timeout
 * @return {undefined}
 */
integrates.controller(
    "projectCtrl",
    function(
        $scope, $location,
        $uibModal, $timeout,
        $state, $stateParams,
        $translate, projectFtry) {

        $scope.init = function(){
            var project = $stateParams.project;
            var findingId = $stateParams.finding;
            $scope.userRole = userRole;
            //Defaults para cambiar vistas
            $scope.view = {};
            $scope.view.project = false;
            $scope.view.finding = false;
            //Parametros de ruta
            if(findingId !== undefined) $scope.findingId = findingId;
            if(project != undefined
                && project != "") {
                $scope.project = project;
                $scope.search();
            }
            //Inicializacion para consulta de hallazgos
            $scope.configColorPalette();
            //Asigna el evento buscar al textbox search y tecla enter
            $scope.configKeyboardView();
            $scope.goUp();
            $scope.finding = {};
        };
        $scope.goUp = function(){
            $('html, body').animate({ scrollTop: 0 }, 'fast');
        };
        $scope.goBack = function(){
            $scope.view.project = true;
            $scope.view.finding = false;
            $scope.mainGraphcriticalityPieChart;
            $scope.mainGraphamountPieChart;
            $scope.mainGraphstatusPieChart;
            $('html, body').animate({ scrollTop: $scope.currentScrollPosition }, 'fast');
        };
        $scope.testFinding = function(){
            $scope.finding = {
                proyecto_fluid: "Integrates",
                proyecto_cliente: "Integrates",
                tipo_prueba: "Aplicación",
                escenario: "Nunc ut nibh non neque semper ornare id sit amet ipsum.",
                actor: "Praesent pharetra metus eget diam dignissim facilisis",
                hallazgo: "FIN. 0001 Ejecución Remota de Comandos",
                categoria: "Fusce iaculis, dolor nec maximus molestie, nisi leo malesuada libero",
                valor_riesgo: "(3.0) Crítico",
                probabilidad: "75% Fácil de vulnerar",
                severidad: "5",
                vulnerabilidad: "Pellentesque quis sapien luctus, fermentum mauris ac, tincidunt urna. Praesent pharetra metus eget diam dignissim facilisis. Phasellus in dictum dolor, elementum pharetra neque. Duis molestie, dui sit amet dictum efficitur, dolor arcu cursus metus, tempor bibendum justo sem quis velit. Nam sed sem id libero scelerisque pretium sit amet rhoncus diam. In eleifend diam felis, eget rutrum mi tempus a. In ex neque, vehicula vitae congue in, sodales non massa.",
                requisitos: "REQ000X. Maecenas vitae molestie arcu. Sed ut enim eu mauris fermentum malesuada sed non magna.",
                cardinalidad: "1023",
                amenaza: "Maecenas eget metus nec nibh blandit sollicitudin vel convallis diam. Maecenas vestibulum augue vitae risus tincidunt",
                donde: "Pellentesque quis sapien luctus, fermentum mauris ac, tincidunt urna. Praesent pharetra metus eget diam dignissim facilisis. Phasellus in dictum dolor, elementum pharetra neque. Duis molestie, dui sit amet dictum efficitur, dolor arcu cursus metus, tempor bibendum justo sem quis velit. Nam sed sem id libero scelerisque pretium sit amet rhoncus diam. In eleifend diam felis, eget rutrum mi tempus a. In ex neque, vehicula vitae congue in, sodales non massa",
                vector_ataque: "Praesent porta congue lorem sit amet rhoncus. ",
                solucion_efecto: "Etiam dapibus ultrices ligula a convallis. Vivamus ultricies convallis magna. Praesent metus sem, porttitor sed risus quis, fringilla rutrum arcu.",
                debilidad: "Fusce iaculis, dolor nec maximus molestie, nisi leo malesuada libero",
                cwe: "https://fluid.la",
                vector_acceso: "0343 | Red Adyacente",
                autenticacion: "0324 | Ninguna",
                explotabilidad: "0435 | Conceptual",
                nivel_confianza: "4543 | Confirmado",
                complejidad_acceso: "4542 | Facil",
                impacto_confidencialidad: "0324 | Alto: Aqui va un texto 1",
                impacto_integridad: "0324 | Alto: Aqui va un texto 2",
                impacto_disponibilidad: "0324 | Alto: Aqui va un texto 3",
                nivel_resolucion: "0233 | Existe porque va un texto 4",
                sistema_comprometido: "Stiam dapibus ultrices ligula a convallis.",
                cssv2base: "4.3",
                criticidad: "5.1",
                timestamp: "04/06/2017 12:40:24"
            };
            //Begin current Date
            var today = new Date();
            var dd = today.getDate();
            var mm = today.getMonth()+1; //January is 0!
            var yyyy = today.getFullYear();
            if(dd<10){ dd='0'+dd; } 
            if(mm<10){ mm='0'+mm; } 
            var today = dd+'/'+mm+'/'+yyyy;
            $scope.header = {
                findingTitle: $scope.finding.hallazgo,
                findingID: "323932433",
                findingType: $scope.finding.tipo_prueba,
                findingValueColor: $scope.colors.critical,
                findingValue: "8.0",
                findingValueDescription: "(Alto)",
                findingCount: $scope.finding.cardinalidad,
                findingStateColor: $scope.colors.critical,
                findingState: "Abierto",
                finding: today
            };
        };
        $scope.calculateCardinality = function(data){
            var cardinalidad = 0;
            data.data.forEach(function(i){
                cardinalidad += parseInt(i.cardinalidad);
            });
            $("#total_cardinalidad").html(cardinalidad);
            $("#total_hallazgos").html(data.data.length);
            var total_criticidad = 0;
            data.data.forEach(function(i){    
                try{
                    if(i.tipo_hallazgo == "Seguridad"){
                        var ImpCon = parseFloat(i.impacto_confidencialidad.split(" | ")[0]);
                        var ImpInt = parseFloat(i.impacto_integridad.split(" | ")[0]);
                        var ImpDis = parseFloat(i.impacto_disponibilidad.split(" | ")[0]);
                        var AccCom = parseFloat(i.complejidad_acceso.split(" | ")[0]);
                        var AccVec = parseFloat(i.vector_acceso.split(" | ")[0]);
                        var Auth = parseFloat(i.autenticacion.split(" | ")[0]);
                        var Explo = parseFloat(i.explotabilidad.split(" | ")[0]);
                        var Resol = parseFloat(i.nivel_resolucion.split(" | ")[0]);
                        var Confi = parseFloat(i.nivel_confianza.split(" | ")[0]);
                        var BaseScore = (((0.6*(10.41*(1-(1-ImpCon)*(1-ImpInt)*(1-ImpDis))))+(0.4*(20*AccCom*Auth*AccVec))-1.5)*1.176);
                        total_criticidad += BaseScore * parseFloat(i.cardinalidad);
                    }
                }catch(e){
            
                }
            });
            $("#total_criticidad").html(total_criticidad.toFixed(0));
        };
        $scope.capitalizeFirstLetter = function(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
        $scope.configColorPalette = function(){
            $scope.colors = {};
            $scope.colors.critical = "background-color: #f12;";  //red
            $scope.colors.moderate = "background-color: #f72;";  //orange
            $scope.colors.tolerable = "background-color: #fd2;"; //yellow
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
            $scope.list.finding_test_type = finging_test_type;
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
        $scope.findingHeaderBuilding = function(){
            //console.log($scope.finding);
            $scope.header = {};
            try{
                var cierres = $scope.finding.cierres;
                var cierresTmp = [];
                for(var i = 0; i < cierres.length ; i++){
                    cierre = cierres[i];
                    cierre.position = i+1;
                    cierresTmp.push(cierre);
                }
                $scope.finding.cierres = cierresTmp;
            }catch(e){
                console.log($scope.finding.id + "No tiene cierres");
            }
            $scope.header.findingTitle = $scope.finding.hallazgo;
            $scope.header.findingType = $scope.finding.tipo_prueba;
            $scope.header.findingRisk = "";
            $scope.header.findingState = $scope.finding.estado;
            $scope.header.findingID = $scope.finding.id;
            $scope.header.findingValue = $scope.finding.criticidad;
            var findingValue = parseFloat($scope.finding.criticidad);
            if(findingValue >= 7){
                $scope.header.findingValueDescription = " Alto";
                $scope.header.findingValueColor = $scope.colors.critical;
            }else if(findingValue >= 4 && findingValue <= 6.9){
                $scope.header.findingValueDescription = " Moderado";
                $scope.header.findingValueColor = $scope.colors.moderate;
            }else{
                $scope.header.findingValueDescription = " Tolerable";
                $scope.header.findingValueColor = $scope.colors.tolerable;
            }
    
            if($scope.header.findingState == "Abierto"){
                $scope.header.findingStateColor = $scope.colors.critical;
            }else if($scope.header.findingState == "Parcialmente cerrado"){
                $scope.header.findingStateColor = $scope.colors.moderate;
            }else{
                $scope.header.findingStateColor = $scope.colors.ok;
            }
    
            $scope.header.findingCount = $scope.finding.cardinalidad;
        };
        $scope.findingCalculateSeveridad = function(){
            if(!isNaN($scope.finding.severidad)){
                var severidad = parseFloat($scope.finding.severidad);
                if (severidad < 0 || severidad > 5){
                    ngNotify.set("La severidad debe ser un numero de 0 a 5", "error");
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
                }catch(e){
                        $scope.finding.valor_riesgo = "";
                }
            }else{
                ngNotify.set("La severidad debe ser un numero de 0 a 5", "error");
            }
        };
        $scope.findingEvidenceTab = function(){
            $scope.tabEvidences = [];
            var evidenceList = [];
            var url_pre = BASE.url + "get_evidence?id=";
            if($scope.finding.animacion !== undefined){
                var url = url_pre + $scope.finding.animacion;
                evidenceList.push({
                    "url": url,
                    "desc": 'Animación de explotación'
                });
            }
            if($scope.finding.desc_evidencia_1 !== undefined
                && $scope.finding.ruta_evidencia_1 !== undefined){
                var url = url_pre + $scope.finding.ruta_evidencia_1;
                evidenceList.push({
                    "url": url,
                    "desc": $scope.capitalizeFirstLetter(
                        $scope.finding.desc_evidencia_1
                    )
                });
            }
            if($scope.finding.desc_evidencia_2 !== undefined
                && $scope.finding.ruta_evidencia_2 !== undefined){
                var url = url_pre + $scope.finding.ruta_evidencia_2;
                evidenceList.push({
                    "url": url,
                    "desc": $scope.capitalizeFirstLetter(
                        $scope.finding.desc_evidencia_2
                    )
                });
            }
            if($scope.desc_evidencia_3 !== undefined
                && $scope.ruta_evidencia_3 !== undefined){
                var url = url_pre + $scope.finding.ruta_evidencia_3;
                evidenceList.push({
                    "url": url,
                    "desc": $scope.capitalizeFirstLetter(
                        $scope.finding.desc_evidencia_3
                    )
                });
            }
            if($scope.finding.desc_evidencia_4 !== undefined
                && $scope.finding.ruta_evidencia_4 !== undefined){
                var url = url_pre + $scope.finding.ruta_evidencia_4;
                evidenceList.push({
                    "url": url,
                    "desc": $scope.capitalizeFirstLetter(
                        $scope.finding.desc_evidencia_4
                    )
                });
            }
            if($scope.finding.desc_evidencia_5 !== undefined
                && $scope.ruta_evidencia_5 !== undefined){
                var url = url_pre + $scope.finding.ruta_evidencia_5;
                evidenceList.push({
                    "url": url,
                    "desc": $scope.capitalizeFirstLetter(
                        $scope.finding.desc_evidencia_5
                    )
                });
            }
            $scope.tabEvidences = evidenceList;
        }
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
        $scope.loadFindingByID = function(id){
            $scope.$apply();
            var findingObj = undefined;
            for(var i=0; i<$scope.data.length; i++){
                var attach = $scope.data[i];
                if(attach.id == id){
                    findingObj = attach;
                    break;
                }
            }
            console.log(findingObj);
            console.log($scope.data);
            if(findingObj.length != undefined){
                $msg.error("No encontramos el hallazgo!");
                return false;
            }else{
                $scope.finding = findingObj;
                $scope.findingHeaderBuilding();
                $scope.view.project = false;
                $scope.view.finding = true;
                $scope.findingInformationTab();
                $scope.findingEvidenceTab();
                //Tracking mixpanel
                mixPanelDashboard.trackReadFinding(userEmail, $scope.finding.id);
                $timeout($scope.goUp, 200);
            }
        };
        $scope.mainGraphamountPieChart = function(){
            var currData = $scope.data;
            var total = 0;
            var high = 0;
            var moderate = 0;
            var low = 0;
            currData.forEach(function(val, i){
                cardinalidad = parseFloat(val.cardinalidad);
                total += cardinalidad;
                criticity = parseFloat(val.criticidad);
                if(criticity >= 7){
                    high += cardinalidad;
                }else if(criticity >= 4 & criticity <= 6.9){
                    moderate += cardinalidad;
                }else{
                    low += cardinalidad;
                }
            });
            total = parseFloat(total);
            highLabel = "Altos :n%".replace(":n", (high*100/total).toFixed(2).toString());
            moderateLabel = "Moderados :n%".replace(":n", (moderate*100/total).toFixed(2).toString());
            lowLabel = "Bajos :n%".replace(":n", (low*100/total).toFixed(2).toString());
            $("#grapAmount").empty();
            Morris.Donut({
                element: 'grapAmount',
                resize: true,
                data: [
                  {label: highLabel, value: high, color: "#ff1a1a"},
                  {label: moderateLabel, value: moderate, color: "#ffbf00"},
                  {label: lowLabel, value: low, color: "#FFFF37"}
                ]
            });
        };
        $scope.mainGraphcriticalityPieChart = function(){
            var currData = $scope.data;
            var total = 0;
            var high = 0;
            var moderate = 0;
            var low = 0;
            currData.forEach(function(val, i){
                cardinalidad = parseFloat(val.cardinalidad);
                total += cardinalidad;
                criticity = parseFloat(val.criticidad);
                if(criticity >= 7){
                    high ++;
                }else if(criticity >= 4 & criticity <= 6.9){
                    moderate ++;
                }else{
                    low ++;
                }
            });
            total = parseFloat(total);
            highLabel = "Altos :n%".replace(":n", (high*100/total).toFixed(2).toString());
            moderateLabel = "Moderados :n%".replace(":n", (moderate*100/total).toFixed(2).toString());
            lowLabel = "Bajos :n%".replace(":n", (low*100/total).toFixed(2).toString());
            $("#grapCriticality").empty();
            Morris.Donut({
                element: 'grapCriticality',
                resize: true,
                data: [
                  {label: highLabel, value: high, color: "#ff1a1a"},
                  {label: moderateLabel, value: moderate, color: "#ffbf00"},
                  {label: lowLabel, value: low, color: "#FFFF37"}
                ]
            });
        };
        $scope.mainGraphstatusPieChart = function(){
            var currData = $scope.data;
            var total = 0;
            var open = 0;
            var partial = 0;
            var close = 0;
            currData.forEach(function(val, i){
                estado = val.estado;
                total ++;
                if(estado == "Abierto"){
                    open++;
                }else if(estado == "Cerrado"){
                    close++;
                }else{
                    partial++;
                }
            });
            total = parseFloat(total);
            openLabel = "Abiertos :n%".replace(":n", (open*100/total).toFixed(2).toString());
            partialLabel = "Parciales :n%".replace(":n", (partial*100/total).toFixed(2).toString());
            closeLabel = "Cerrados :n%".replace(":n", (close*100/total).toFixed(2).toString());
            $("#grapStatus").empty();
            Morris.Donut({
                element: 'grapStatus',
                resize: true,
                data: [
                  {label: openLabel, value: open, color: "#ff1a1a"},
                  {label: partialLabel, value: partial, color: "#ffbf00"},
                  {label: closeLabel, value: close, color: "#31c0be"}
                ]
            });
        };
        $scope.search = function(){
            var project = $scope.project;
            var filter = $scope.filter;
            var finding = $scope.findingId;
            if(project === undefined
                || project === ""){
                $msg.warning("Busqueda vacia");
                return false;
            }
            $scope.view.project = false;
            $scope.view.finding = false;
            $msg.info("Buscando Proyecto :)");
            var reqProject = projectFtry.projectByName(project, filter);
            var reqEventualities = projectFtry.EventualityByName(project, "Name");
            reqProject.then(function(response){
                $scope.view.project = true;
                if(!response.error){
                    //Tracking Mixpanel
                    $scope.data = response.data;
                    mixPanelDashboard.trackSearchFinding(userEmail, project);
                    $timeout($scope.mainGraphcriticalityPieChart, 200);
                    $timeout($scope.mainGraphamountPieChart, 200);
                    $timeout($scope.mainGraphstatusPieChart, 200);
                    //CONFIGURACION DE TABLA
                    $("#vulnerabilities").bootstrapTable('destroy');
                    $("#vulnerabilities").bootstrapTable({
                        data: $scope.data,
                        onClickRow: function(row, elem){
                            $scope.loadFindingByID(row.id);
                            $scope.currentScrollPosition =  $(document).scrollTop();
                        }
                    });
                    $("#vulnerabilities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip();
                    $scope.calculateCardinality({data: $scope.data});
                   
                    if(finding !== undefined){
                        $scope.finding.id = finding;
                        $scope.loadFindingByID($scope.finding.id);
                        $scope.view.project = false;
                        $scope.view.finding = false;
                    }
                }else{
                    $msg.error("No pudimos encontrarlo :(");
                }
            });
            reqEventualities.then(function(response){
                if(!response.error){
                    mixPanelDashboard.trackSearchEventuality (userEmail, project);
                    //CONFIGURACION DE TABLA
                    $("#tblEventualities").bootstrapTable('destroy');
                    $("#tblEventualities").bootstrapTable({
                        data: response.data,
                        onClickRow: function(row){
                            var modalInstance = $uibModal.open({
                                templateUrl: BASE.url + 'assets/views/project/eventualityMdl.html',
                                animation: true, 
                                resolve: { evt: row }, backdrop: false,
                                controller: function($scope, $uibModalInstance, evt){
                                    $scope.evt = evt;
                                    $scope.close = function(){
                                        $uibModalInstance.close();
                                    }
                                }
                            });
                        }
                    });
                    $("#tblEventualities").bootstrapTable('refresh');
                    //MANEJO DEL UI
                    $("#search_section").show();
                    $('[data-toggle="tooltip"]').tooltip();
                }else{

                }
            });
        }
        $scope.showProjectView = function(){
            $("#findingView").fadeOut(300);
            $("#projectView").fadeIn(300);
            $(".loader").hide();
        };
        $scope.showFindingView = function(){
            $("#projectView").fadeOut(300);
            $("#findingView").fadeIn(300);
            $(".loader").hide();
        };
        $scope.init();
    }
);