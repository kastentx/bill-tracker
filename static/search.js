var billTracker = angular.module("bill-tracker", []).config(function($httpProvider) {
    // http://django-angular.readthedocs.org/en/latest/csrf-protection.html
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

    billTracker.controller("BillsListController", function($scope, $http) {

        // Retrieve bills data from database
        $http.get("/get_bill_list").success(function (data) {

            var bills_list = [];
            for (index = 0; index < data.length; index++) {
                bills_list.push(data[index]["fields"]);
                bills_list[index]["id"] = data[index]["pk"];
            }
            console.log(bills_list);
            $scope.bills = bills_list;
        });
    });

    billTracker.controller("AuthorListController", function($scope, $http) {

        // Retrieve authors (senators) data from database
        $http.get("/get_author_list").success(function(data) {

            var author_list = [];
            for (index = 0; index < data.length; index++) {
                author_list.push(data[index]["fields"]);
                author_list[index]["id"] = data[index]["pk"];
            }
            console.log(author_list);
            $scope.authors = author_list;
        });
    });

    billTracker.controller("SubjectListController", function($scope, $http) {

        // Retrieve subjects data from database
        $http.get("/get_subject_list").success(function(data) {

            var subject_list = [];
            for (index = 0; index < data.length; index++) {
                subject_list.push(data[index]["fields"]);
                subject_list[index]["id"] = data[index]["pk"];
            }
            console.log(subject_list);
            $scope.subjects = subject_list;
        });
    });

    billTracker.controller("BillsByAuthorController", function($scope, $window, $http) {

        // Retrieve bills authored by author with specified id
        $http.get("/get_author_bills", {params: {id: $window.author_id}}).success(function(data) {

            var bills_list = [];
            for (index = 0; index < data.length; index++) {
                bills_list.push(data[index]["fields"]);
                bills_list[index]["id"] = data[index]["pk"];
            }
            console.log(bills_list);
            $scope.bills = bills_list;
        });
    });

    billTracker.controller("BillsBySubjectController", function($scope, $window, $http) {

        // Retrieve bills about specified subject
        $http.get("/get_subject_bills", {params: {id: $window.subject_id}}).success(function(data) {

            var bills_list = [];
            for (index = 0; index < data.length; index++) {
                bills_list.push(data[index]["fields"]);
                bills_list[index]["id"] = data[index]["pk"];
            }
            console.log(bills_list);
            $scope.bills = bills_list;
        });
    });