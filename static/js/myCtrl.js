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
  $scope.selected_addr = -1

  $scope.hex = function(dec) {
    var str = 'x'+Number(dec).toString(16)
    return str
  };

  $scope.getData = function () {
        $timeout(function () {
            $http({
                url: 'data.json?r=' + Math.random(),
                method: 'GET'
            }).then(function (answ) {
                $scope.network = answ.data.network;
            });
            $scope.getData();
        }, 100 );
  };

  $scope.selectAddress = function(addr) {
    console.log(addr)
    if($scope.selected_addr == addr) {
        $scope.selected_addr = -1
    } else {
        $scope.selected_addr = addr
    }
    $scope.selected_device = addr
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
        // $scope.getData();
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
        // $scope.getData();
    }

    $scope.setValue = function(addr, reg, value){
        var cmd =
            {
            "cmd": "setValue",
            "param":{
                "addr": addr,
                "reg": reg,
                "value": value
            }
            };
        $http({
            url: "/actionAddr",
            method: 'POST',
            params: {data: cmd}
        }).then(function (answ) {
            console.log(cmd)
        })
    }
    // $scope.getValues = function() {
    // $timeout(function () {
    //     $http({
    //         url: 'data.json?r=' + Math.random(),
    //         method: 'GET'
    //     }).then(function (answ) {
    //         $scope.network = answ.data.network;
    //         // console.log($scope.setupData)
    //     });
    //    $scope.getValues();
    // }, 100 );
    // }
    // $scope.getValues();
    $scope.getTypes();
    $scope.getData();
});

app.controller('setupCtrl', function($scope, $http, $timeout) {
    $scope.setupData = {}

    $scope.setPort = function(port) {
        var cmd = {
            "cmd": "port",
            "param": {
                "port": port
            }
        };
        if(port != undefined) {
            $http({
                url: "/actionAddr",
                method: 'POST',
                params: {data: cmd}
            }).then(function (answ) {
                console.log(cmd)
            })
        }
    }

    $scope.getSetup = function() {
        $timeout(function () {
            $http({
                url: 'setup.json?r=' + Math.random(),
                method: 'GET'
            }).then(function (answ) {
                $scope.setupData = answ.data.setup;
                // console.log($scope.setupData)
            });
           $scope.getSetup();
        }, 2000 );
    }


    $scope.getSetup();
});