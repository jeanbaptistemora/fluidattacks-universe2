var remember = null;
$(document).ready(function(){
    remember = function(){
        try{
            alertify.log( '<div class="" style="padding: 8px;"><p class="text-center">Recordatorio</p><p class="text-left"> Recuerda personalizar los campos dependiendo de la situación que vas a reportar!</p> </div>');
        } catch(e){
            
        }
    }
    remember();
    setInterval('remember();',35000);
    document.getElementsByTagName("select")[5].onchange = function(){
    	v = document.getElementsByTagName("select")[5].value; 
    	if(v == "Verificación") alertify.success('<p class="text-center"> Información: </p> <p class="text-left"> Verificacion debe usarse para reportar hallazgos en chequeos cruzados </p>');
    }
});

function isUpperCase(str) {
    return str === str.toUpperCase();
}

String.prototype.capitalizeFirstLetter = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

var description = $("#field32202728");
var requirement = $("#field38254586");
var solution = $("#field38619077");
var threat = $("#field38193361");
var risk = $("#field38193362");
var donde = $("#field38193357");
var has_solution = $("#field38861717_1");
var has_no_solution = $("#field38861717_2");
var solution_kb = $("#field38861739");
var debilidad = $("#field38899046");
var solution_pdf = $("#field38307753");
var evidencia_hallazgo = $('#field32202896');
var exploit = $('#field38307199');
var evidencia_explotacion = $('#field38307222');
var animacion = $('#field38307272');
var si_evidente = $('#field49132420_1');
var no_evidente = $('#field49132420_2');

var public_spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1L37WnF6enoC8Ws8vs9sr0G29qBLwbe-3ztbuopu1nvc/pubhtml';

Tabletop.init( { key: public_spreadsheet_url, callback: showInfo, simpleSheet: true , prettyColumnNames: true} );

function showInfo(data,tabletop) {
	obj = $.parseJSON(JSON.stringify(data));
	$("#field32201810").change(function() {
		var title = $("#field32201810").val();
		for(var i = 0; i < obj.length; i++) {

			if(obj[i].Titulo == title) {

				description.val(obj[i].Descripcion);
				requirement.val(obj[i].Requisito);
				solution.val(obj[i].Recomendacion);
				donde.attr("placeholder", obj[i].Donde);
				debilidad.val(obj[i].CWE.split("/")[5].split(".")[0]);
        
		        if(obj[i].Evidente == "Sí"){
		        	si_evidente.attr('checked', true);
		        }else{
		        	no_evidente.attr('checked', true);
		        }
        
				if(obj[i].Solucion_KB != "-"){
					has_solution.attr('checked', true);
					$("#fsCell38861739").removeClass("fsHidden");
					$("#fsCell38307753").removeClass("fsHidden");
					solution_pdf.removeAttr("disabled");
					solution_kb.val(obj[i].Solucion_KB);
				}else{
					has_no_solution.attr('checked', true);
					$("#fsCell38861739").addClass("fsHidden");
					$("#fsCell38307753").addClass("fsHidden");
					solution_pdf.attr("disabled");
				}

				if ($("#field38392454").val() == "Detallado"){
					threat.val(obj[i].Amenaza);
					risk.val(obj[i].Riesgo);
				}
	
				//if(obj[i].Exploit == "Sí"){
				if($("#field38529253").val() == 0.950){
					exploit.prop("required", true);
					exploit.addClass("fsRequired");
					exploit.attr("aria-required", true);
					exploit.attr("fsRequired");

					evidencia_explotacion.prop("required", true);
					evidencia_explotacion.addClass("fsRequired");
					evidencia_explotacion.attr("aria-required", true);
					evidencia_explotacion.attr("fsRequired");
			
				}else{
					exploit.prop("required",false);
					exploit.removeClass("fsRequired");
					exploit.attr("aria-required", false);

					evidencia_explotacion.prop("required", false);
					evidencia_explotacion.removeClass("fsRequired");
					evidencia_explotacion.attr("aria-required", false);
        
        			animacion.prop("required", false);
					animacion.removeClass("fsRequired");
					animacion.attr("aria-required", false);
				}
								
				break;
			}
			if(i == obj.length - 1) {
				description.val(""); 
				requirement.val("");
				solution.val("");
				threat.val("");
				risk.val("");
				debilidad.val(0);
				donde.attr("placeholder", "Formato DONDE dependiendo de la vulnerabilidad.");
				$("#fsCell38861739").addClass("fsHidden");
				$("#fsCell38307753").addClass("fsHidden");
				$("#field38307753").attr("disabled");
			}
		}
	});
}

$(donde).focusout(function() {
  	donde.val($.trim(donde.val()));
});

$(requirement).focusout(function() {
  	requirement.val($.trim(requirement.val()));
  	if(requirement.val()[requirement.val().length - 1] != "."){
  		requirement.val(requirement.val() + ".");
  	}
  	if(isUpperCase(requirement.val()[0]) == false){
  		requirement.val(requirement.val().capitalizeFirstLetter());
  	}
});

$(description).focusout(function() {
  	description.val($.trim(description.val()));
  	if(description.val()[description.val().length - 1] != "."){
  		description.val(description.val() + ".");
  	}
  	if(isUpperCase(description.val()[0]) == false){
  		description.val(description.val().capitalizeFirstLetter());
  	}

  	description.val(description.val());
});

$(solution).focusout(function() {
  	solution.val($.trim(solution.val()));
  	if(solution.val()[solution.val().length - 1] != "."){
  		solution.val(solution.val() + ".");
  	}
  	if(isUpperCase(solution.val()[0]) == false){
  		solution.val(solution.val().capitalizeFirstLetter());
  	}
});

$(risk).focusout(function() {
  	risk.val($.trim(risk.val()));
  	if(risk.val()[risk.val().length - 1] != "."){
  		risk.val(risk.val() + ".");
  	}
  	if(isUpperCase(risk.val()[0]) == false){
  		risk.val(risk.val().capitalizeFirstLetter());
  	}
});

$(threat).focusout(function() {
  	threat.val($.trim(threat.val()));
  	if(threat.val()[threat.val().length - 1] != "."){
  		threat.val(threat.val() + ".");
  	}
  	if(isUpperCase(threat.val()[0]) == false){
  		threat.val(threat.val().capitalizeFirstLetter());
  	}
});

$(evidencia_hallazgo).change(function() {
	var hallazgo_upload = $(evidencia_hallazgo).val().split("\\")[2].split(".")[0];
    var substring = "evidencia";
	if(hallazgo_upload.indexOf(substring) === -1){
		alert('El archivo se debe contener la palabra evidencia');
		evidencia_hallazgo.val("");
	}
	
});

$(exploit).change(function() {
	var exploit_upload = $(exploit).val().split("\\")[2].split(".")[0];
	if(exploit_upload != "exploit"){
		alert("El archivo se debe llamar: exploit")
		exploit.val("");
	}
	else{
		exploit.attr("aria-invalid",false);
	}
});

$(evidencia_explotacion).change(function() {
	var explotacion_upload = $(evidencia_explotacion).val().split("\\")[2].split(".")[0];
	if(explotacion_upload != "evidencia-de-explotacion"){
		alert("El archivo se debe llamar: evidencia-de-explotacion")
		evidencia_explotacion.val("");
	}else{
		evidencia_explotacion.attr("aria-invalid", false);
	}
});

$(animacion).change(function() {
	var animacion_upload = $(animacion).val().split("\\")[2].split(".")[0];
	if(animacion_upload != "animacion-de-explotacion"){
		alert("El archivo se debe llamar: animacion-de-explotacion")
		animacion.val("");
	}else{
		animacion.attr("aria-invalid", false);
	}
});

$(solution_pdf).change(function() {
	var sol_upload = $(solution_pdf).val().split("\\")[2].split(".")[0];
	if(sol_upload != "solucion"){
		alert("El archivo se debe llamar: solucion")
		solution_pdf.val("");
	}
});