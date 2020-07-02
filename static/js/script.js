var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http, $timeout) {
  $scope.data = {}
  $scope.names = {}
  $scope.link = false

  $scope.setValue = function(reg, value) {
    var cmd =
             {
                 "cmd": "set",
                 "param": {
                     "reg": reg,
                     "value": value
                     }
             };
			$http({ url: "/setChannel",
					method: 'POST',
					params: { data:cmd }
				  }).then(function (answ) {
                    console.log(cmd)
				  })
  }

  $scope.getData = function () {
		$timeout(function () {
            $http({
                    url: 'data.json?r=' + Math.random(),
                    method: 'GET'
                }).then(function (answ) {
                    $scope.data = answ.data.regs;
                    $scope.link = answ.data.link;
                    $scope.names = answ.data.names;
//                    $scope.data["names"] = answ.data.names;
                });
            $scope.getData();
         }, 100 );

    };


	$scope.getData();	// запускаем опрос json
});