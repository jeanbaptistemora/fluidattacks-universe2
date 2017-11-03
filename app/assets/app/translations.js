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
                'cardinalities': 'Vulnerabilities',
                'criticity': 'Total Criticity Found',
                'closure': 'Closure Effectiveness'
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
            },
            'descriptions':{
              'description1': '',
              'description2': 'Click',
              'description3': 'to see more details of the find'
            },
            'eventualities':{
              'description': 'Click to see the detail'
            }
        },
        'main_content':{
          'projects':{
            'title': 'My Projects',
            'description1': 'You can see details of a project by ',
            'description2': 'clicking',
            'description3': ' on it'
          },
          'eventualities':{
                'title': 'My Eventualities',
                'description_1': 'You can see details of a eventuality by',
                'description_2': 'clicking',
                'description_3': 'on it'
              }
        },
        'grapExploit':{
          'title': 'Distribution by Exploitability'
        },
        'grapType':{
          'title': 'Distribution by Type Find'
        },
        'grapStatus':{
          'title': 'Findings by Status'
        },
        'tab_container':{
          'findings': 'Findings',
          'eventualities': 'Eventualities'
        },
        'event_by_name':{
          'page_head':{
            'search': 'Search',
            'vuln_by_proj': 'Eventualities by project '
          },
          'modal_edit':{
            'type': 'Type',
            'analyst': 'Analyst',
            'f_proj': 'Fluid Project',
            'c_proj': 'Client Project',
            'client': 'Client',
            'detail': 'Description',
            'date': 'Date',
            'affec': 'Affection',
            'close': 'Close',
            'refresh': 'Update'
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
                'cardinalities': 'Vulnerabilidades',
                'criticity': 'Criticidad Total Encontrada',
                'closure': 'Efectividad de Cierre'
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
            },
            'descriptions':{
              'description1': 'Haz',
              'description2': 'click',
              'description3': 'para ver mas detalles del hallazgo'
            },
            'eventualities':{
              'description': 'Haz click para ver el detalle'
            }
        },
        'main_content':{
          'projects':{
            'title': 'Mis Proyectos',
            'description1': 'Para ver el detalle del proyecto debes hacer ',
            'description2': 'click',
            'description3': ' sobre el proyecto'
          },
          'eventualities':{
                 'title': 'Mis Eventualidades',
                 'description_1': 'Para ver el detalle de la eventualidad debes hacer',
                 'description_2': 'click',
                 'description_3': 'sobre la eventualidad'
           }
        },
        'grapExploit':{
          'title': 'Distribucion por Explotabilidad'
        },
        'grapType':{
          'title': 'Distribucion por Tipo Hallazgo'
        },
        'grapStatus':{
          'title': 'Hallazgos por Estado'
        },
        'tab_container':{
          'findings': 'Hallazgos',
          'eventualities': 'Eventualidades'
        },
        'event_by_name':{
          'page_head':{
            'search': 'Busqueda',
            'vuln_by_proj': 'Eventualidades por proyecto'
          },
          'modal_edit':{
            'type': 'Tipo',
            'analyst': 'Analista',
            'f_proj': 'Proyecto Fluid',
            'c_proj': 'Proyecto Cliente',
            'client': 'Cliente',
            'detail': 'Detalle',
            'date': 'Fecha',
            'affec': 'Afectacion',
            'close': 'Cerrar',
            'refresh': 'Actualizar'
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
