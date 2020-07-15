// materialize css settings
// document.addEventListener('DOMContentLoaded', function() {
//     var elems = document.querySelectorAll('.tooltipped');
//     var instances = M.Tooltip.init(elems);
//   });
//
 // Инициализация выпадающего списка
// $(document).ready(function(){
//     $('select').formSelect();
//     $('.dropdown-trigger').dropdown();
//   });
// controllers

var app = angular.module("myApp", ["ngRoute"]);
app.config(function($routeProvider) {
  $routeProvider
  .when("/", {
    templateUrl : "network.html",
    controller: 'networkCtrl'
  })
  .when("/manage", {
    templateUrl : "manage.html",
    controller: 'manageCtrl'
  })
});

app.controller('networkCtrl', function($scope, $http, $timeout) {
    $scope.page = 'network'

  $scope.network = {}
  $scope.device_info = {}

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
                $scope.network = answ.data.network;
                console.log("getData " + answ.data)
            });
            $scope.getData();
        }, 100 );
  };


	$scope.getData();	// запускаем опрос json
});

app.controller('manageCtrl', function($scope, $http, $timeout) {
    $scope.page = 'manage'
    $scope.network = {}
    $scope.types = {}
    $scope.device_info = {}
    $scope.selected_addr = 0
    $scope.selected_device = 0

    $scope.getData = function () {
        $timeout(function () {
            $http({
                url: 'data.json?r=' + Math.random(),
                method: 'GET'
            }).then(function (answ) {
                $scope.network = answ.data.network;
            });
//            $scope.getData();
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
        if($scope.selected_addr == addr) {
            $scope.selected_addr = 0
            $scope.device_info = {}
        } else {
            $scope.selected_addr = addr
            device = $scope.network[addr].device
            $scope.device_info = device
        }
        $scope.selected_device = 0
    }

    $scope.selectDeviceType = function(id) {
        $scope.selected_device = id
        $scope.device_info = $scope.types[id]
        console.log($scope.device_info)
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
				  $scope.getData();
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
		$scope.getData();
    }

    $scope.getTypes();
    $scope.getData();
});