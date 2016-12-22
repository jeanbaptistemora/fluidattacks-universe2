/**
 * @file app.js
 * @author engineering@fluid.la
 */
/**
 * Obtiene una cookie atraves de su nombre
 * @function getCookie
 * @param {String} name
 * @return {String}
 */
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
/**
 * Verifica el metodo por el cual se va a enviar una peticion de cookie
 * @function csrfSafeMethod
 * @param {String} method
 * @return {Boolean}
 */
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS)$/.test(method));
}
/**
 * Verifica si la url dada esta dentro del mismo dominio
 * @function sameOrigin
 * @param {String} url
 * @return {Boolean}
 */
function sameOrigin(url) {
    var host = document.location.host;
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        !(/^(\/\/|http:|https:).*/.test(url));
}
/**
 * Agrega la cookie de CSRF a todas las peticiones ajax de la aplicacion
 * @function ajaxConfig
 * @return {undefined}
 */
function ajaxConfig(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                var csrftoken = getCookie('csrftoken');
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
/*
 * Establece la ruta principal para las peticiones ajax
 */
var BASE = { production: "/integrates/",
             development: "/" };
BASE.url = BASE.production;
if(location.pathname.indexOf("/integrates") == -1)
    BASE.url = BASE.development;

/**
 * Crea integrates como una aplicacion de angular
 * @module {AngularJS} FluidIntegrates
 */
var integrates = angular.module("FluidIntegrates", ['ui.router','ui.bootstrap']); 
/**
 * Establece la configuracion de las rutas para integrates
 * @config {AngularJS} 
 * @param {Object} $stateProvider
 * @param {Object} $urlRouterProvider
 * @return {undefined}
 */
integrates.config(function($stateProvider, $urlRouterProvider) {
    $urlRouterProvider.otherwise('home');
    $stateProvider
        .state('home', {
            url: '/home',
            templateUrl: 'assets/views/dashboard.html'
        })
        .state('VulnerabilitiesByName', {
            url: '/VulnerabilitiesByName',
            templateUrl: 'assets/views/search/vulns_by_name.html',
            controller: 'findingController'  
        })
            .state('UpdateVuln', {
                url: '/vuln/update/?id',
                templateUrl: 'assets/views/search/vulns_update.html',
                controller: 'findingUpdateController'  
            })
            .state('DeleteVuln', {
                url: '/vuln/delete/?id',
                templateUrl: 'assets/views/search/vulns_delete.html',
                controller: 'findingDeleteController'  
            })
            .state('ReadVuln', {
                url: '/vuln/read/?id',
                templateUrl: 'assets/views/search/vulns_read.html',
                controller: 'findingReadController'  
            })
        .state('EventualitiesByName', {
            url: '/EventualitiesByName',
            templateUrl: 'assets/views/search/event_by_name.html',
            controller: 'eventualityController'        
        })
});