var app = angular.module("api", []);
function arrayToObject(array, mainkey){
    var obj = {};
    for(i in array){
        obj[array[i][mainkey]] = {};
        for(j in array[i]){
            if(j == mainkey){
                continue;
            }
            obj[array[i][mainkey]][j] = array[i][j];
        }
    }
    return obj;
}
app.controller("application", function($scope, $http, $interval, $timeout) {
    $scope.products;
    $scope.o_products;
    $scope.order_product = [];
    $scope.total_order = 0;
    getProduct($http).then((a)=>{
        $scope.products = a.data.data;
        $scope.o_products = arrayToObject($scope.products, "idproduct")
        console.log($scope.o_products);
    }).catch((e)=>{
        console.log(e);
    })
    $scope.productId = function(id, key){
        return $scope.o_products[id][key];
    }
    $scope.productIdToName = function(id){
        return $scope.o_products[id].name;
    };
    $scope.productIdToPrice = function(id){
        return $scope.o_products[id].price;
    };
    $scope.addProduct = function(){
        console.log("SELECT:", $scope.selectProduct);
        if($scope.selectProduct == undefined){
            return;
        }
        $scope.order_product.push({
            idorder_buss: 0,
            idproduct: $scope.selectProduct,
            favor: '',
            favor_support: '',
            amount: 1
        })
        $scope.total();
    }
    $scope.deleteProduct = function(id){
        console.log("DELETE:", id)
        for(i in $scope.order_product){
            if($scope.order_product[i].idproduct == id){
                $scope.order_product.slice(i, 1);
                return;
            }
        }
    }
    $scope.createOrder = function(){
        if($scope.order_product.length == 0){
            alert("Không thể tạo với đơn hàng rỗng!. Ooop -");
            return;
        }
        var or_buss = new Order();
        or_buss.setCustomer(0);
        or_buss.setTotalPrice($scope.total_order);
        or_buss.create($http).then((a)=>{
            console.log("ORDER_BUSS:", a.data.data.id);
            for(i in $scope.order_product){
                console.log($scope.order_product[i]);
                var or_pro = new OrderProduct();
                or_pro.setOrderBuss(a.data.data.id);
                or_pro.setAmount($scope.order_product[i].amount);
                or_pro.setProduct($scope.order_product[i].idproduct);
                or_pro.create($http).then(print).catch(print);
            }
        }).catch(print);
    }

    $scope.total = function(){
        $scope.total_order = 0;
        for(i in $scope.order_product){
            $scope.total_order += $scope.productId($scope.order_product[i].idproduct, "price")*$scope.order_product[i].amount;
        }

    }
});