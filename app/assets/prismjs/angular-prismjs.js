angular.module('prismjsHighlight', [])
.directive('highlight', ['$timeout', function($timeout) {
    return {
        scope: true,
        link: function(scope, elm, attrs) {

            function escapeHtml(s) {
                return s
                    .replace(/&/g, "&amp;")
                    .replace(/</g, "&lt;")
                    .replace(/>/g, "&gt;")
                    .replace(/"/g, "&quot;")
                    .replace(/'/g, "&#039;")
            }
            var source = elm.find('figure').html()
            var escaped = escapeHtml(source)
            scope.code = escaped
        }
    }
}])
.directive('prismHighlight', ['$compile', function($compile) {
    return {
        restrict: 'A',
        transclude: true,
        scope: {
            source: '@'
        },
        link: function(scope, element, attrs, controller, transclude) {
            scope.$watch('source', function(v) {
                element.find("code").html(v)
                Prism.highlightElement(element.find("code")[0])
            })

            transclude(function(clone) {
                if (clone.html() !== undefined) {
                    element.find("code").html(clone.html())
                    $compile(element.contents())(scope.$parent)
                }
            })
        },
        template: "<code></code>"
    }
}])