/**
 * @file ProjectCtrl.js
 * @author engineering@fluid.la
 */
/* Table Formatter */
function removeHour(value, row, index){
    if(value.indexOf(":") != -1){
        return value.split(" ")[0];
    }
    return value;
}
function labelState(value, row, index){
    if(value == "Cerrado"){
        return "<label class='label label-success' style='background-color: #31c0be'>Cerrado</label>";
    }else if(value == "Closed"){
        return "<label class='label label-success' style='background-color: #31c0be'>Closed</label>";
    }else if(value == "Abierto"){
        return "<label class='label label-danger' style='background-color: #f22;'>Abierto</label>";
    }else if(value == "Open"){
        return "<label class='label label-danger' style='background-color: #f22;'>Open</label>";
    }else if(value == "Parcialmente cerrado"){
        return "<label class='label label-info' style='background-color: #ffbf00'>Parcialmente cerrado</label>";
    }else{
        return "<label class='label label-info' style='background-color: #ffbf00'>Partially closed</label>";
    }
}
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
                $scope.search();
            }
            //Inicializacion para consulta de hallazgos
            $scope.configColorPalette();
            //Asigna el evento buscar al textbox search y tecla enter
            $scope.configKeyboardView();
            $scope.goUp();
            $scope.finding = {};
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
        $scope.goUp = function(){
            $('html, body').animate({ scrollTop: 0 }, 'fast');
        };
        $scope.goBack = function(){
            $scope.view.project = true;
            $scope.view.finding = false;
            $scope.mainGraphexploitPieChart;
            $scope.mainGraphtypePieChart;
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
            var cardinalidad_total = 0;
            data.data.forEach(function(i){
                cardinalidad += parseInt(i.cardinalidad);
                cardinalidad_total += parseInt(i.cardinalidad_total);
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
                        total_criticidad += BaseScore * parseFloat(i.cardinalidad_total);
                    }
                }catch(e){
                }
            });
            $("#total_criticidad").html(total_criticidad.toFixed(0));
            $("#total_efectividad").html("n%".replace("n", (((1-(cardinalidad/cardinalidad_total))*100).toFixed(2).toString())));
        };
        $scope.capitalizeFirstLetter = function(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
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
        $scope.generateFullDoc = function(){
            var project = $scope.project;
            var data = $("#vulnerabilities").bootstrapTable('getData');
            for(i=0; i < data.length-1; i++){
                for(j=i+1; j < data.length; j++){
                    if(parseFloat(data[i].criticidad) < parseFloat(data[j].criticidad)){
                        aux = data[i];
                        data[i] = data[j];
                        data[j] = aux;
                    }
                }
            }
            var generateDoc = true;
            try{
                json = data;
                generateDoc = true;
                json = JSON.stringify(JSON.parse(JSON.stringify(json))); //remove indices
                if (json == undefined) throw "error";
                if (json == [] || json == {}) throw "error";
                if(project.trim() == "") throw "error";
            }catch(e){
                generateDoc = false;
            }
            if(generateDoc == false) return false;
            var req = projectFtry.ProjectDoc(project, json, "IT");
            req.then(function(response){
                if(!response.error){
                    var url = BASE.url + "export_autodoc?project=" + $scope.project;
                    url += "&format=IT";
                    if(navigator.userAgent.indexOf("Firefox") == -1){
                        $scope.downloadURL = url;
                    }else{
                        win = window.open(url, '__blank');
                    }
                }
            });
            $scope.downloadDoc();
        };
        $scope.generatePDF = function(){
            var project = $scope.project;
            var lang = localStorage['lang'];
            var prjpatt = new RegExp("^[a-zA-Z0-9_]+$");
            var langpatt = new RegExp("^en|es$");
            if(prjpatt.test(project)
                && langpatt.test(lang)){
                var url = BASE.url + "doc/" + lang + "/project/" + project;
                if(navigator.userAgent.indexOf("Firefox") == -1){
                    $scope.downloadURL = url;
                }else{
                     win = window.open(url, '__blank');
                }
            }
        };
        $scope.downloadDoc = function(){
            if($scope.downloadURL == undefined){
                $timeout($scope.downloadDoc, 3000);
            }else{
                downLink = document.createElement("a");
                downLink.target = "_blank";
                downLink.href = $scope.downloadURL;
                downLink.click();
            }
        }
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
            $scope.$apply();
            var findingObj = undefined;
            for(var i=0; i<$scope.data.length; i++){
                var attach = $scope.data[i];
                if(attach.id == id){
                    findingObj = attach;
                    break;
                }
            }
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
            }
        };
        $scope.mainGraphtypePieChart = function(){
            var currData = $scope.data;
            var total_seg = 0;
            var total_hig = 0;
            currData.forEach(function(val, i){
                tipo = val.tipo_hallazgo;
                if(val.estado != "Cerrado" && val.estado != "Closed"){
                    if(tipo == "Seguridad"){
                        total_seg += 1;
                    }else{
                        total_hig += 1;
                    }
                }
            });
            var seg_transl = $translate.instant('grapType.seg_label');
            var hig_transl = $translate.instant('grapType.hig_label');
            total_segLabel = seg_transl + " :n%".replace(":n", (total_seg*100/(total_seg+total_hig)).toFixed(2).toString());
            total_higLabel = hig_transl + " :n%".replace(":n", (total_hig*100/(total_seg+total_hig)).toFixed(2).toString());
            $("#grapType").empty();
            Morris.Donut({
                element: 'grapType',
                resize: true,
                data: [
                  {label: total_segLabel, value: total_seg, color: "#ff1a1a"},
                  {label: total_higLabel, value: total_hig, color: "#31c0be"},
                ]
            });
        };
        $scope.mainGraphexploitPieChart = function(){
            var currData = $scope.data;
            var exploit = 0;
            var nonexploit = 0;
            currData.forEach(function(val, i){
                explotable = val.explotabilidad;
                if(val.estado != "Cerrado" && val.estado != "Closed"){
                    if(explotable == "1.000 | Alta: No se requiere exploit o se puede automatizar" || explotable == "0.950 | Funcional: Existe exploit" || explotable == "1.000 | High: Exploit is not required or it can be automated" || explotable == "0.950 | Functional: There is an exploit" ){
                        exploit ++;
                    }else{
                        nonexploit ++;
                    }
                }
            });
            var exploit_transl = $translate.instant('grapExploit.exploit_label');
            var nonexploit_transl = $translate.instant('grapExploit.nonexploit_label');
            exploitLabel = exploit_transl + " :n%".replace(":n", (exploit*100/(exploit+nonexploit)).toFixed(2).toString());
            nonexploitLabel = nonexploit_transl + " :n%".replace(":n", (nonexploit*100/(exploit+nonexploit)).toFixed(2).toString());
            $("#grapExploit").empty();
            Morris.Donut({
                element: 'grapExploit',
                resize: true,
                data: [
                  {label: exploitLabel, value: exploit, color: "#ff1a1a"},
                  {label: nonexploitLabel, value: nonexploit, color: "#31c0be"},
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
                if(estado == "Abierto" || estado == "Open" ){
                    open++;
                }else if(estado == "Cerrado" || estado == "Closed"){
                    close++;
                }else{
                    partial++;
                }
            });
            total = parseFloat(total);
            var open_transl = $translate.instant('grapStatus.open_label');
            var partial_transl = $translate.instant('grapStatus.partial_label');
            var close_transl = $translate.instant('grapStatus.close_label');
            openLabel = open_transl + " :n%".replace(":n", (open*100/total).toFixed(2).toString());
            partialLabel = partial_transl + " :n%".replace(":n", (partial*100/total).toFixed(2).toString());
            closeLabel = close_transl + " :n%".replace(":n", (close*100/total).toFixed(2).toString());
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
            if(localStorage['lang'] === "en"){
              var vlang = 'en-US';
            } else {
              var vlang = 'es-CO';
            }
            var project = $scope.project;
            var filter = $scope.filter;
            var finding = $scope.findingId;
            if(project === undefined
                || project === ""){
                var attention_at = $translate.instant('proj_alerts.attent_title');
                var attention_ac = $translate.instant('proj_alerts.attent_cont');
                $msg.warning(attention_ac,attention_at);
                return false;
            }
            if($stateParams.project != $scope.project){
                $state.go("ProjectNamed", {project: $scope.project});
            }else{
                $scope.view.project = false;
                $scope.view.finding = false;
                var search_at = $translate.instant('proj_alerts.search_title');
                var search_ac = $translate.instant('proj_alerts.search_cont');
                $msg.info(search_ac, search_at);
                var reqProject = projectFtry.projectByName(project, filter);
                var reqEventualities = projectFtry.EventualityByName(project, "Name");
                reqProject.then(function(response){
                    $scope.view.project = true;
                    if(!response.error){
                        //Tracking Mixpanel
                        $scope.data = response.data;
                        for(var i = 0; i< $scope.data.length;i++){
                           switch ($scope.data[i].actor) {
                             case "​Cualquier persona en Internet":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.any_internet');;
                               break;
                             case "Cualquier cliente de la organización":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.any_costumer');;
                               break;
                             case "Solo algunos clientes de la organización":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.some_costumer');;
                               break;
                             case "Cualquier persona con acceso a la estación":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.any_access');;
                               break;
                             case "Cualquier empleado de la organización":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.any_employee');;
                               break;
                             case "Solo algunos empleados":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.some_employee');;
                               break;
                             case "Solo un empleado":
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.one_employee');;
                               break;
                             default:
                               $scope.data[i].actor = $translate.instant('finding_formstack.actor.default');;
                           }
                           switch ($scope.data[i].autenticacion) {
                             case "0.704 | Ninguna: No se requiere autenticación":
                               $scope.data[i].autenticacion = $translate.instant('finding_formstack.authentication.any_authen');;
                               break;
                             case "0.560 | Única: Único punto de autenticación":
                               $scope.data[i].autenticacion = $translate.instant('finding_formstack.authentication.single_authen');;
                               break;
                             case "0.450 | Multiple: Multiples puntos de autenticación":
                               $scope.data[i].autenticacion = $translate.instant('finding_formstack.authentication.multiple_authen');;
                               break;
                             default:
                               $scope.data[i].autenticacion = $translate.instant('finding_formstack.authentication.default');;
                           }
                           switch ($scope.data[i].categoria) {
                             case "Actualizar y configurar las líneas base de seguridad de los componentes":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.update_base');;
                               break;
                             case "Definir el modelo de autorización considerando el principio de mínimo privilegio":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.define_model');;
                               break;
                             case "Desempeño":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.performance');;
                               break;
                             case "Eventualidad":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.event');;
                               break;
                             case "Evitar exponer la información técnica de la aplicación, servidores y plataformas":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.avoid_technical');;
                               break;
                             case "Excluir datos sensibles del código fuente y del registro de eventos":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.exclude_data');;
                               break;
                             case "Fortalecer controles en autenticación y manejo de sesión":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.strengt_authen');;
                               break;
                             case "Fortalecer controles en el procesamiento de archivos":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.strengt_process');;
                               break;
                             case "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.strengt_protect');;
                               break;
                             case "Implementar controles para validar datos de entrada":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.validate_input');;
                               break;
                             case "Mantenibilidad":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.maintain');;
                               break;
                             case "Registrar eventos para trazabilidad y auditoría":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.record_event');;
                               break;
                             case "Utilizar protocolos de comunicación seguros":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.secure_protoc');;
                               break;
                             case "Validar la integridad de las transacciones en peticiones HTTP":
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.validate_http');;
                               break;
                             default:
                               $scope.data[i].categoria = $translate.instant('finding_formstack.category.default');;
                           }
                           switch ($scope.data[i].complejidad_acceso) {
                             case "0.350 | Alto: Se requieren condiciones especiales como acceso administrativo":
                               $scope.data[i].complejidad_acceso = $translate.instant('finding_formstack.complexity.high_complex');;
                               break;
                             case "0.610 | Medio: Se requieren algunas condiciones como acceso al sistema":
                               $scope.data[i].complejidad_acceso = $translate.instant('finding_formstack.complexity.medium_complex');;
                               break;
                             case "0.710 | Bajo: No se requiere ninguna condición especial":
                               $scope.data[i].complejidad_acceso = $translate.instant('finding_formstack.complexity.low_complex');;
                               break;
                             default:
                               $scope.data[i].complejidad_acceso = $translate.instant('finding_formstack.complexity.default');;
                           }
                           switch ($scope.data[i].escenario) {
                             case "Anónimo desde Internet":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.anon_inter');;
                               break;
                             case "Anónimo desde Intranet":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.anon_intra');;
                               break;
                             case "Escaneo de Infraestructura":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.infra_scan');;
                               break;
                             case "Extranet usuario no autorizado":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.unauth_extra');;
                               break;
                             case "Internet usuario autorizado":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.auth_inter');;
                               break;
                             case "Internet usuario no autorizado":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.unauth_inter');;
                               break;
                             case "Intranet usuario autorizado":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.auth_intra');;
                               break;
                             case "Intranet usuario no autorizado":
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.unauth_inter');;
                                break;
                             default:
                               $scope.data[i].escenario = $translate.instant('finding_formstack.scenario.default');;
                           }
                           switch ($scope.data[i].estado) {
                             case "Abierto":
                               $scope.data[i].estado = $translate.instant('finding_formstack.status.open');;
                               break;
                             case "Cerrado":
                               $scope.data[i].estado = $translate.instant('finding_formstack.status.close');;
                               break;
                             case "Parcialmente cerrado":
                               $scope.data[i].estado = $translate.instant('finding_formstack.status.part_close');;
                               break;
                             default:
                               $scope.data[i].estado = $translate.instant('finding_formstack.status.default');;
                           }
                           switch ($scope.data[i].explotabilidad) {
                             case "0.850 | Improbable: No existe un exploit":
                               $scope.data[i].explotabilidad = $translate.instant('finding_formstack.exploitability.improbable');;
                               break;
                             case "0.900 | Conceptual: Existen pruebas de laboratorio":
                               $scope.data[i].explotabilidad = $translate.instant('finding_formstack.exploitability.conceptual');;
                               break;
                             case "0.950 | Funcional: Existe exploit":
                               $scope.data[i].explotabilidad = $translate.instant('finding_formstack.exploitability.functional');;
                               break;
                             case "1.000 | Alta: No se requiere exploit o se puede automatizar":
                               $scope.data[i].explotabilidad = $translate.instant('finding_formstack.exploitability.high');;
                               break;
                             default:
                               $scope.data[i].explotabilidad = $translate.instant('finding_formstack.exploitability.default');;
                           }
                           switch ($scope.data[i].explotable) {
                             case "Si":
                               $scope.data[i].explotable = $translate.instant('finding_formstack.exploitable.yes');;
                               break;
                             case "No":
                               $scope.data[i].explotable = $translate.instant('finding_formstack.exploitable.no');;
                               break;
                             default:
                               $scope.data[i].explotable = $translate.instant('finding_formstack.exploitable.default');;
                           }
                           switch ($scope.data[i].impacto_confidencialidad) {
                             case "0 | Ninguno: No se presenta ningún impacto":
                               $scope.data[i].impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.none');;
                               break;
                             case "0.275 | Parcial: Se obtiene acceso a la información pero no control sobre ella":
                               $scope.data[i].impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.partial');
                               break;
                             case "0.660 | Completo: Se controla toda la información relacionada con el objetivo":
                               $scope.data[i].impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.complete');
                               break;
                             default:
                               $scope.data[i].impacto_confidencialidad = $translate.instant('finding_formstack.confidenciality.default');;
                           }
                           switch ($scope.data[i].impacto_disponibilidad) {
                             case "0 | Ninguno: No se presenta ningún impacto":
                               $scope.data[i].impacto_disponibilidad = $translate.instant('finding_formstack.availability.none');;
                               break;
                             case "0.275 | Parcial: Se presenta intermitencia en el acceso al objetivo":
                               $scope.data[i].impacto_disponibilidad = $translate.instant('finding_formstack.availability.partial');;
                               break;
                             case "0.660 | Completo: Hay una caída total del objetivo":
                               $scope.data[i].impacto_disponibilidad = $translate.instant('finding_formstack.availability.complete');;
                               break;
                             default:
                               $scope.data[i].impacto_disponibilidad = $translate.instant('finding_formstack.availability.default');;
                           }
                           switch ($scope.data[i].impacto_integridad) {
                             case "0 | Ninguno: No se presenta ningún impacto":
                               $scope.data[i].impacto_integridad = $translate.instant('finding_formstack.integrity.none');;
                               break;
                             case "0.275 | Parcial: Es posible modificar cierta información del objetivo":
                               $scope.data[i].impacto_integridad = $translate.instant('finding_formstack.integrity.partial');;
                               break;
                             case "0.660 | Completo: Es posible modificar toda la información del objetivo":
                               $scope.data[i].impacto_integridad = $translate.instant('finding_formstack.integrity.complete');;
                               break;
                             default:
                               $scope.data[i].impacto_integridad = $translate.instant('finding_formstack.integrity.default');;
                           }
                           switch ($scope.data[i].nivel_confianza) {
                             case "0.900 | No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad":
                               $scope.data[i].nivel_confianza = $translate.instant('finding_formstack.confidence.not_confirm');;
                               break;
                             case "0.950 | No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales":
                               $scope.data[i].nivel_confianza = $translate.instant('finding_formstack.confidence.not_corrob');;
                               break;
                             case "1.000 | Confirmado: La vulnerabilidad es reconocida por el fabricante":
                               $scope.data[i].nivel_confianza = $translate.instant('finding_formstack.confidence.confirmed');;
                               break;
                             default:
                               $scope.data[i].nivel_confianza = $translate.instant('finding_formstack.confidence.default');;
                           }
                           switch ($scope.data[i].nivel_resolucion) {
                             case "0.950 | Paliativa: Existe un parche que no fue publicado por el fabricante":
                               $scope.data[i].nivel_resolucion = $translate.instant('finding_formstack.resolution.palliative');;
                               break;
                             case "0.870 | Oficial: Existe un parche disponible por el fabricante":
                               $scope.data[i].nivel_resolucion = $translate.instant('finding_formstack.resolution.official');;
                               break;
                             case "0.900 | Temporal: Existen soluciones temporales":
                               $scope.data[i].nivel_resolucion = $translate.instant('finding_formstack.resolution.temporal');;
                               break;
                             case "1.000 | Inexistente: No existe solución":
                               $scope.data[i].nivel_resolucion = $translate.instant('finding_formstack.resolution.non_existent');;
                               break;
                             default:
                               $scope.data[i].nivel_resolucion = $translate.instant('finding_formstack.resolution.default');;
                           }
                           switch ($scope.data[i].probabilidad) {
                             case "100% Vulnerado Anteriormente":
                               $scope.data[i].probabilidad = $translate.instant('finding_formstack.probability.prev_vuln');;
                               break;
                             case "75% Fácil de vulnerar":
                               $scope.data[i].probabilidad = $translate.instant('finding_formstack.probability.easy_vuln');;
                               break;
                             case "50% Posible de vulnerar":
                               $scope.data[i].probabilidad = $translate.instant('finding_formstack.probability.possible_vuln');;
                               break;
                             case "25% Difícil de vulnerar":
                               $scope.data[i].probabilidad = $translate.instant('finding_formstack.probability.diffic_vuln');;
                               break;
                             default:
                               $scope.data[i].probabilidad = $translate.instant('finding_formstack.probability.default');;
                           }
                           switch ($scope.data[i].tipo_hallazgo_cliente) {
                             case "Higiene":
                               $scope.data[i].tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.hygiene');;
                               break;
                             case "Vulnerabilidad":
                               $scope.data[i].tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.vuln');;
                               break;
                             default:
                               $scope.data[i].tipo_hallazgo_cliente = $translate.instant('finding_formstack.finding_type.default');;
                           }
                           switch ($scope.data[i].tipo_prueba) {
                             case "Análisis":
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.analysis');;
                               break;
                             case "Aplicación":
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.app');;
                               break;
                             case "Binario":
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.binary');;
                               break;
                             case "Código":
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.code');;
                               break;
                             case "Infraestructura":
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.infras');;
                               break;
                             default:
                               $scope.data[i].tipo_prueba = $translate.instant('finding_formstack.test_method.default');;
                           }
                           switch ($scope.data[i].vector_acceso) {
                             case "0.646 | Red adyacente: Explotable desde el mismo segmento de red":
                               $scope.data[i].vector_acceso = $translate.instant('finding_formstack.access_vector.adjacent');;
                               break;
                             case "1.000 | Red: Explotable desde Internet":
                               $scope.data[i].vector_acceso = $translate.instant('finding_formstack.access_vector.network');;
                               break;
                             case "0.395 | Local: Explotable con acceso local al objetivo":
                               $scope.data[i].vector_acceso = $translate.instant('finding_formstack.access_vector.local');;
                               break;
                             default:
                               $scope.data[i].vector_acceso = $translate.instant('finding_formstack.access_vector.default');;
                           }
                           switch ($scope.data[i].tratamiento) {
                             case "Asumido":
                               $scope.data[i].tratamiento = $translate.instant('finding_formstack.treatment_header.asummed');;
                               break;
                             case "Pendiente":
                               $scope.data[i].tratamiento = $translate.instant('finding_formstack.treatment_header.working');;
                               break;
                             case "Remediar":
                               $scope.data[i].tratamiento = $translate.instant('finding_formstack.treatment_header.remediated');;
                               break;
                             default:
                               $scope.data[i].tratamiento = $translate.instant('finding_formstack.treatment_header.default');;
                           }
                        };
                        mixPanelDashboard.trackSearchFinding(userEmail, project);
                        $timeout($scope.mainGraphexploitPieChart, 200);
                        $timeout($scope.mainGraphtypePieChart, 200);
                        $timeout($scope.mainGraphstatusPieChart, 200);
                        //CONFIGURACION DE TABLA
                        $("#vulnerabilities").bootstrapTable('destroy');
                        $("#vulnerabilities").bootstrapTable({
                            locale: vlang,
                            data: $scope.data,
                            onClickRow: function(row, elem){
                                $state.go("FindingDescription", {project: row.proyecto_fluid.toLowerCase(), id: row.id});
                                $("#infoItem").addClass("active");
                                $("#info").addClass("active");
                                $("#cssv2Item").removeClass("active");
                                $("#cssv2").removeClass("active")
                                $("#trackingItem").removeClass("active");
                                $("#tracking").removeClass("active");
                                $("#evidenceItem").removeClass("active");
                                $("#evidence").removeClass("active");
                                $("#exploitItem").removeClass("active");
                                $("#exploit").removeClass("active");
                                $scope.currentScrollPosition =  $(document).scrollTop();
                            },
                            cookieIdTable: "saveId",
                            cookie: true,
                            exportDataType: "all"
                        });
                        $("#vulnerabilities").bootstrapTable('refresh');
                        //MANEJO DEL UI
                        $("#search_section").show();
                        $('[data-toggle="tooltip"]').tooltip();
                        $scope.calculateCardinality({data: $scope.data});

                        if($stateParams.finding !== undefined){
                            $scope.finding.id = $stateParams.finding;
                            $scope.loadFindingByID($scope.finding.id);
                            $scope.view.project = false;
                            $scope.view.finding = false;
                        }
                    }else{
                        $msg.error($translate.instant('proj_alerts.not_found'));
                    }
                });
                reqEventualities.then(function(response){
                    if(!response.error){
                      for(var i = 0; i< response.data.length;i++){
                         switch (response.data[i].tipo) {
                           case "Autorización para ataque especial":
                             response.data[i].tipo = $translate.instant('event_formstack.type.auth_attack');;
                             break;
                           case "Alcance difiere a lo aprobado":
                             response.data[i].tipo = $translate.instant('event_formstack.type.toe_differs');;
                             break;
                           case "Aprobación de alta disponibilidad":
                             response.data[i].tipo = $translate.instant('event_formstack.type.high_approval');;
                             break;
                           case "Insumos incorrectos o faltantes":
                             response.data[i].tipo = $translate.instant('event_formstack.type.incor_supplies');;
                             break;
                           case "Cliente suspende explicitamente":
                             response.data[i].tipo = $translate.instant('event_formstack.type.explic_suspend');;
                             break;
                           case "Cliente aprueba cambio de alcance":
                             response.data[i].tipo = $translate.instant('event_formstack.type.approv_change');;
                             break;
                           case "Cliente cancela el proyecto/hito":
                             response.data[i].tipo = $translate.instant('event_formstack.type.cancel_proj');;
                             break;
                           case "Cliente detecta ataque":
                             response.data[i].tipo = $translate.instant('event_formstack.type.det_attack');;
                             break;
                           case "Otro":
                             response.data[i].tipo = $translate.instant('event_formstack.type.other');;
                             break;
                           case "Ambiente no accesible":
                             response.data[i].tipo = $translate.instant('event_formstack.type.inacc_ambient');;
                             break;
                           case "Ambiente inestable":
                             response.data[i].tipo = $translate.instant('event_formstack.type.uns_ambient');;
                             break;
                           case "Insumos incorrectos o faltantes":
                             response.data[i].tipo = $translate.instant('event_formstack.type.incor_supplies');;
                             break;
                           default:
                             response.data[i].tipo = $translate.instant('event_formstack.type.unknown');;
                         }
                         switch (response.data[i].estado) {
                           case "Pendiente":
                             response.data[i].estado = $translate.instant('event_formstack.status.unsolve');;
                             break;
                           case "Tratada":
                             response.data[i].estado = $translate.instant('event_formstack.status.solve');;
                             break;
                           default:
                             response.data[i].estado = $translate.instant('event_formstack.status.unknown');;
                         }
                      };
                        mixPanelDashboard.trackSearchEventuality (userEmail, project);
                        //CONFIGURACION DE TABLA
                        $("#tblEventualities").bootstrapTable('destroy');
                        $("#tblEventualities").bootstrapTable({
                            locale: vlang,
                            data: response.data,
                            onClickRow: function(row){
                                var modalInstance = $uibModal.open({
                                    templateUrl: BASE.url + 'assets/views/project/eventualityMdl.html',
                                    animation: true,
                                    resolve: { evt: row },
                                    backdrop: 'static',
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
                    $scope.modalTitle = $translate.instant('confirmmodal.title_cssv2');;
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
        $scope.openModalAvance = function(){
            var modalInstance = $uibModal.open({
                animation: true,
                templateUrl: 'avance.html',
                windowClass: 'modal avance-modal',
                keyboard: false,
                controller: function($scope, $uibModalInstance){
                    var auxiliar = $("#vulnerabilities").bootstrapTable('getData');
                    var data = auxiliar;
                    for(i=0; i < data.length; i++){
                        data[i].atributos = 0;
                        data[i].link = window.location.href.split('project/')[0] + 'project/' + data[i].proyecto_fluid.toLowerCase() + '/' + data[i].id + '/description';
                        if (typeof data[i].registros !== 'undefined' && data[i].registros !== ''){
                          data[i].atributos = 1 + (data[i].registros.match(/\n/g)||[]).length;
                        }
                    }
                    for(i=0; i < data.length-1; i++){
                        for(j=i+1; j < data.length; j++){
                           if(parseFloat(data[i].criticidad) < parseFloat(data[j].criticidad)){
                                aux = data[i];
                                data[i] = data[j];
                                data[j] = aux;
                           }
                        }
                    }
                    $scope.rows = data;
                    $scope.closeModalAvance = function(){
                        $uibModalInstance.dismiss('cancel');
                        $timeout(function() {$("#vulnerabilities").bootstrapTable('load', auxiliar);},100);
                    }
                },
                resolve: {
                    ok: true
                }
            });
        };
        $scope.updateEvidenceText = function(target){
            console.log(target);
            $msg.info("En desarrollo ;)");
            return false;
        };
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
