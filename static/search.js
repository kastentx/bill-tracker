var billTracker = angular.module("bill-tracker", []);

    billTracker.controller("BillsListController", function($scope, $http) {

        // Retrieve bills data from database
        $http.get("/get_bill_list").success(function(data) {

            var bills_list = [];
            for (index = 0; index < data.length; index++) {
                bills_list.push(data[index]["fields"]);
                bills_list[index]["id"] = data[index]["pk"];
            }
            console.log(bills_list);
            $scope.bills = bills_list;
        });
});