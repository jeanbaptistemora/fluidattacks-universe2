/**
 * @file translations.js
 * @author engineering@fluid.la
 */
 /**
 * Establece la configuracion de las traducciones de integrates
 * @config {AngularJS}
 * @param {Object} $translateProvider
 * @return {undefined}
 */
integrates.config(['$translateProvider', function($translateProvider) {
    $translateProvider.useSanitizeValueStrategy('sanitize');
    var translations = {
        'logout': {
            'message': 'Are you sure?',
            'title': 'Close Session',
            'ok': 'Logout',
            'cancel': 'Cancel'
        },
        'left_menu': {
            'first': 'Findings',
            'second': 'Eventualities'
        },
        'breadcumbs': {
            'findings': {
                'page': 'Findings',
                'function': 'Findings by project'
            },
            'eventualities':{
                'page': 'Eventualities',
                'function': 'Eventualities by project'
            }
        },
        'search_findings': {
            'filter_menu':{
                'filter_select':{
                    'any': 'All',
                    'analysis': 'Analysis',
                    'application': 'Application',
                    'binary': 'Binary',
                    'code': 'Code',
                    'infrastructure': 'Infrastructure'
                },
                'search':{
                    'placeholder': 'Fluid project name'
                }
            },
            'filter_labels':{
                'findings': 'Findings',
                'cardinalities': 'Vulnerabilities'
            },
            'filter_buttons':{
                'advance': 'Progress',
                'documentation': 'Documentation'
            },
            'table':{
                'headings':{
                    'action': 'Action',
                    'age': 'Age',
                    'timestamp': 'Date',
                    'type': 'Type',
                    'finding': 'Title',
                    'vulnerability': 'Description',
                    'criticity': 'CVSSv2 Score',
                    'cardinality': '# Vuln.',
                    'state': 'State',
                    'exploit': 'Exploit'
                }
            }
        }
    };
    var traducciones = {
        'logout': {
            'message': 'Esta seguro de que desea salir?',
            'title':'Cerrar Sesion',
            'ok': 'Salir',
            'cancel': 'Cancelar'
        },
        'left_menu': {
            'first': 'Hallazgos',
            'second': 'Eventualidades'
        },
        'breadcumbs': {
            'findings': {
                'page': 'Hallazgos',
                'function': 'Hallazgos por proyecto'
            },
            'eventualities':{
                'page': 'Eventualidades',
                'function': 'Eventualidades por proyecto'
            }
        },
        'search_findings': {
            'filter_menu':{
                'filter_select':{
                    'any': 'Todos',
                    'analysis': 'Analisis',
                    'application': 'Aplicacion',
                    'binary': 'Binario',
                    'code': 'Codigo',
                    'infrastructure': 'Infraestructura'
                },
                'search':{
                    'placeholder': 'Nombre del proyecto en Fluid'
                }
            },
            'filter_labels':{
                'findings': 'Hallazgos',
                'cardinalities': 'Vulnerabilidades'
            },
            'filter_buttons':{
                'advance': 'Avance',
                'documentation': 'Documentacion'
            },
            'table':{
                'headings':{
                    'age': 'Edad',
                    'action': 'Accion',
                    'timestamp': 'Fecha',
                    'type': 'Tipo',
                    'finding': 'Titulo',
                    'vulnerability': 'Descripcion',
                    'criticity': 'CVSSv2',
                    'cardinality': '# Vuln.',
                    'state': 'Estado',
                    'exploit': 'Explotable'
                }
            }
        }
    };
    if(localStorage['lang'] === undefined){
        localStorage['lang'] = 'es';
    }
    $translateProvider
        .translations('en', translations)
        .translations('es', traducciones)
        .preferredLanguage(localStorage['lang']);

}]);
