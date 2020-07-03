// materialize css settings
document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.tooltipped');
    var instances = M.Tooltip.init(elems);
  });

// Инициализация выпадающего списка
document.addEventListener('DOMContentLoaded', function() {
   var elems = document.querySelectorAll('select');
   var instances = M.FormSelect.init(elems, '');
});


// controllers

var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope, $http, $timeout) {
  $scope.connected = {}
  $scope.device_info = {}
  $scope.selected = 0
  $scope.link = false
  $scope.types = {}

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
                    $scope.connected = answ.data.connected;
                });
            $scope.getData();
         }, 100 );

    };

    $scope.getTypes = function() {
        $timeout(function() {
            $http({
                url: 'types.json?r=' + Math.random(),
                method: 'GET'
            }).then(function(answ) {
                $scope.types = answ.data.types;
            });
        }, 100);
    };

    $scope.selectAddress = function(addr) {
        if($scope.selected == addr) {
            $scope.selected = 0
        } else {
            $scope.selected = addr
            device = $scope.connected[addr].device
            $scope.device_info = device
        }
    }

    $scope.deleteDevice = function(addr) {
        var cmd =
             {
                 "cmd": "del",
                 "param": {
                     "addr": addr
                     }
             };
			$http({ url: "/actionAddr",
					method: 'POST',
					params: { data:cmd }
				  }).then(function (answ) {
                    console.log(cmd)
				  })
    }

    $scope.addDevice = function(addr, type) {
        var cmd =
             {
                 "cmd": "add",
                 "param": {
                     "addr": addr,
                     "type": type
                     }
             };
			$http({ url: "/actionAddr",
					method: 'POST',
					params: { data:cmd }
				  }).then(function (answ) {
                    console.log(cmd)
				  })
    }

    $scope.getTypes();
	$scope.getData();	// запускаем опрос json
});