var scenario = [
{
    name: "Anónimo desde Internet",
},
{
    name: "Anónimo desde Intranet"
},
{
    name: "Escaneo de Infraestructura"
},
{
    name: "Extranet usuario no autorizado"
},
{
    name: "Internet usuario autorizado"
},
{
    name: "Internet usuario no autorizado"
},
{
    name: "Intranet usuario autorizado"
},
{
    name: "Intranet usuario no autorizado"
}
];

var categories = [
{
    name: "Actualizar y configurar las líneas base de seguridad de los componentes"
},
{
    name: "Definir el modelo de autorización considerando el principio de mínimo privilegio",
},
{
    name: "Desempeño",
},
{
    name: "Eventualidad",
},
{
    name: "Evitar exponer la información técnica de la aplicación, servidores y plataformas"
},
{
    name: "Excluir datos sensibles del código fuente y del registro de eventos"
},
{
    name: "Fortalecer controles en autenticación y manejo de sesión"
},
{
    name: "Fortalecer controles en el procesamiento de archivos"
},
{
    name: "Fortalecer la protección de datos almacenados relacionados con contraseñas o llaves criptográficas"
},
{
    name: "Implementar controles para validar datos de entrada"
},
{
    name: "Mantenibilidad"
},
{
    name: "Registrar eventos para trazabilidad y auditoría"
},
{
    name: "Utilizar protocolos de comunicación seguros"
},
{
    name: "Validar la integridad de las transacciones en peticiones HTTP"
}
];

var probabilities = [
{
    name: "100% Vulnerado Anteriormente",
    value: 100
},
{
    name:"75% Fácil de vulnerar",
    value: 75
},
{
    name:"50% Posible de vulnerar",
    value: 50
},
{
    name:"25% Difícil de vulnerar",
    value: 25
}
];

var actor = [
{
    name: "​Cualquier persona en Internet",
},
{
    name: "Cualquier cliente de la organización"
},
{
    name: "Solo algunos clientes de la organización"
},
{
    name: "Cualquier persona con acceso a la estación"
},
{
    name: "Cualquier empleado de la organización"
},
{
    name: "Solo algunos empleados"
},
{
    name: "Solo un empleado"
}
];

var accessVector = [
{
    value: "0.646",
    name: "Red adyacente: Explotable desde el mismo segmento de red"
},
{
    value: "1.000",
    name: "Red: Explotable desde Internet"
},
{
    value: "0.395",
    name: "Local: Explotable con acceso local al objetivo"
}
];

var accessComplexity = [
{
    value: "0.350",
    name: "Alto: Se requieren condiciones especiales como acceso administrativo"
},
{
    value: "0.610",
    name: "Medio: Se requieren algunas condiciones como acceso al sistema"
},
{
    value: "0.710",
    name: "Bajo: No se requiere ninguna condición especial"
}
];

var authentication = [
{
    name: "Ninguna: No se requiere autenticación",
    value: "0.704"
},
{
    name: "Única: Único punto de autenticación",
    value: "0.560"
},
{
    name: "Multiple: Multiples puntos de autenticación",
    value: "0.450"
}
];

var confidenciality = [
{
    name: "Ninguno: No se presenta ningún impacto",
    value: "0"
},
{
    name: "Parcial: Se obtiene acceso a la información pero no control sobre ella",
    value: "0.275"
},
{
    name: "Completo: Se controla toda la información relacionada con el objetivo",
    value: "0.660"
}
];

var integrity = [
{
    name: "Ninguno: No se presenta ningún impacto",
    value: "0"
},
{
    name: "Parcial: Es posible modificar cierta información del objetivo",
    value: "0.275"
},
{
    name: "Completo: Es posible modificar toda la información del objetivo",
    value: "0.660"
}
];

var availability = [
{
    name: "Ninguno: No se presenta ningún impacto",
    value: "0"
},
{
    name: "Parcial: Se presenta intermitencia en el acceso al objetivo",
    value: "0.275"
},
{
    name: "Completo: Hay una caída total del objetivo",
    value: "0.660"
}
];

var explotability = [
{
    name: "Improbable: No existe un exploit",
    value: "0.850"
},
{
    name: "Conceptual: Existen pruebas de laboratorio",
    value: "0.900"
},
{
    name: "Funcional: Existe exploit",
    value: "0.950"
},
{
    name: "Alta: No se requiere exploit o se puede automatizar",
    value: "1.000"
}
];

var resolutionLevel = [
{
    name: "Paliativa: Existe un parche que no fue publicado por el fabricante",
    value: "0.950"
},
{
    name: "Oficial: Existe un parche disponible por el fabricante",
    value: "0.870"
},
{
    name: "Temporal: Existen soluciones temporales",
    value: "0.900"
},
{
    name: "Inexistente: No existe solución",
    value: "1.000"
}
];

var realiabilityLevel = [
{
    name: "No confirmado: Existen pocas fuentes que reconocen la vulnerabilidad",
    value: "0.900"
},
{
    name: "No corroborado: La vulnerabilidad es reconocida por fuentes no oficiales",
    value: "0.950"
},
{
    name: "Confirmado: La vulnerabilidad es reconocida por el fabricante",
    value: "1.000"
}
];

var finding_type = [
{
    name: "Seguridad"
},
{
    name: "Higiene"
}
];

var tratamiento = [
{
    name: "Asumido"
},
{
    name: "Pendiente"
},
{
    name: "Remediar"
}
];
