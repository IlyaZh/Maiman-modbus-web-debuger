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

  $scope.connected = {}
  $scope.device_info = {}
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
                $scope.connected = answ.data.connected;
            });
            $scope.getData();
        }, 100 );
  };


	$scope.getData();	// запускаем опрос json
});

app.controller('manageCtrl', function($scope, $http, $timeout) {
    $scope.page = 'manage'
    $scope.connected = {}
    $scope.types = {}
    $scope.device_info = {}
    $scope.selected_addr = 0
    $scope.selected_device = 0
    $scope.current_info = {}

    $scope.getData = function () {
        $timeout(function () {
            $http({
                url: 'data.json?r=' + Math.random(),
                method: 'GET'
            }).then(function (answ) {
                $scope.connected = answ.data.connected;
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

    $scope.getInfo = function(id) {
        $timeout(function() {
            $http({
                url: 'info.json?id='+ id +'&r=' + Math.random(),
                method: 'GET'
            }).then(function(answ) {
                $scope.device_info = answ.data;
            });
        }, 100);
    };

    $scope.selectAddress = function(addr) {
        if($scope.selected_addr == addr) {
            $scope.selected_addr = 0
            $scope.current_info = {}
        } else {
            $scope.selected_addr = addr
            device = $scope.connected[addr].device
            $scope.current_info = device
            if (device != null) {
                $scope.device_info
                console.log(device.id)
                console.log($scope.device_info)
            }
        }
    }

    $scope.selectDeviceType = function(id) {
        $scope.selected_device = id
        $scope.current_info = $scope.types[id]
        console.log($scope.current_info)
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
    $scope.getInfo(0);
});