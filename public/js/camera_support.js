var ID_TEMP = "1569136449056";
var socket = io();
var TIME_RECORD = 10;
const TIME_TO_RECORD = 10000;
const TIME_SLEEP_NOTIFY = 3000;
var READY_UPLOAD_RECORD = false;
var rts;
var data_recog;
var data_customer;
jQuery("canvas").hide();
function showImage(){
    jQuery("video").hide();    
    jQuery("canvas").show();
}

function showCamera(){
    jQuery("video").show();    
    jQuery("canvas").hide();
}

function recordTimeSecond(nsecond){
    startRecording();
    READY_UPLOAD_RECORD = false;
    rts = setTimeout(function(){
        READY_UPLOAD_RECORD = true;
        stopRecording();
    }, nsecond*1000);
}
const STATE_APP = ["PAGE_1", "PAGE_2", "PAGE_3", "PAGE_4"];
const NEX_PAGE = 13;
const NE_PAGE = 43;
const PRE_PAGE = 45;
const OUT_PAGE = 97;
const CAN_     = 97;
var PAGE_INDEX = 0;
var PAGE_PREV  = 0;
var STRIGGER    = 254;
var time_strigger = 0;
function hideModal(id){
    var modal = jQuery("#" + id);
    modal.hide();
}

function showModal(id){
    var modal = jQuery("#" + id);
    modal.show();
}

function createCustomer(obj){
    socket.emit("create_customer", obj, function(){
        console.log("OK");
    });
}

function saveCustomer(obj){
    socket.emit("save_data", obj, function(){
        console.log("OK");
    });
}

function capture_send_video(name){
    uploadRecord(name);
    showCamera();
}
var app = angular.module("camera", []);
app.controller("counter", function($scope, $http, $interval, $timeout) {
    $scope.updateResult = function(obj){
        $scope.results = obj.content;
    }
    $scope.updateStatus = function(obj){
        console.log(obj)
        var d = jQuery("#field-status");
        var color = ["w3-green", "w3-blue", "w3-yellow", "w3-red", "w3-gray"];
        for(i in color){
            if(d.hasClass(color[i])){
                d.removeClass(color[i]);
            }
        }
        d.addClass(obj.color);
        $scope.status = obj.content;
    }
    $scope.data_recog = [];
    $scope.data_customer = [];
    $scope.note = {};
    $scope.customers = {};
    $scope.results = "Nhấn ENTER để bắt đầu";
    $scope.state_note = [{
        key: 1,
        note: "Thân thiện",
        chose: false
    }, {
        key: 2,
        note: "Thích uống cafe",
        chose: false
    }, {
        key: 3,
        note: "Mua thêm món bánh",
        chose: false
    }, {
        key: 4,
        note: "Hay chào hỏi",
        chose: false
    }, {
        key: 5,
        note: "Trà sữa",
        chose: false
    }, {
        key: 6,
        note: "Đi một nhóm",
        chose: false
    }]
    $scope.page = function (index){
        switch(index){
            case 0:{
                hideModal("page-2");
                hideModal("page-3");
                showCamera();
                // $scope.updateStatus({
                //     content: "Nhấn ENTER để chụp ảnh",
                //     color: "w3-green"
                
                // });

                if(PAGE_PREV == 3) {
                    let t = [];
                    for(i in $scope.state_note){
                        if($scope.state_note[i].chose == true){
                            t.push($scope.state_note[i].note);
                            console.log("122: ", i)
                        }
                    }
                    let s = (new Date());
                    var obj = {};

                    console.log($scope.data_recog);
                    if($scope.data_recog.length == 0){
                        obj["note"] = [{
                            content: t,
                            date: s,
                            price: $scope.price
                        }];
                        // obj["price"] = $scope.price;
                        id_ = (new Date()).getTime().toString();
                        obj.id = id_;
                        obj.name = "CUS-" + id_;
                        createCustomer(obj);
                        capture_send_video(obj.name);
                    } else {
                        obj["note"] = t;
                        obj["price"] = $scope.price;
                        console.log("SAVE DATA TO DATABASE");
                        obj.id = data_customer[0].id;
                        console.log(obj);
                        console.log(data_customer);
                        saveCustomer(obj);
                    }
                    $scope.data_customer = [];
                    $scope.data_recog = [];
                    // let j = 1;
                    for(i in $scope.state_note){
                        if($scope.state_note[i].chose == true){
                            jQuery("#tr-" + $scope.state_note[i].key).removeClass("w3-red");
                            $scope.state_note[i].chose = false;
                            console.log($scope.state_note[i]);
                        }
                    }
                    $scope.price = "";
                    $timeout(function(){
                        $scope.updateStatus({ content: "Nhấn ENTER để chụp ảnh", color: "w3-blue"});
                    }, 5000) 
                } else if (PAGE_PREV == 1){
                    if($scope.data_recog.length == 0){
                        $scope.updateStatus({ content: "Nhấn ENTER để chụp ảnh", color: "w3-blue"});
                    }
                } else {
                    /* NOTHING TO DO */
                    //$scope.updateStatus({ content: "Nhấn ENTER để chụp ảnh", color: "w3-blue"});
                    $scope.data_customer = [];
                    $scope.data_recog = [];
                    // let j = 1;
                    for(i in $scope.state_note){
                        if($scope.state_note[i].chose == true){
                            jQuery("#tr-" + $scope.state_note[i].key).removeClass("w3-red");
                            $scope.state_note[i].chose = false;
                            console.log($scope.state_note[i]);
                        }
                    }
                    $scope.price = "";
                    $scope.updateStatus({ content: "Nhấn ENTER để chụp ảnh", color: "w3-blue"});
                }

                /* XOA TOAN DU LIEU */
                /* TRO VE CAMERA */
            } break;
            case 1:{
                if(PAGE_PREV == 2){
                    showImage();
                    hideModal("page-2");
                } else {
                    $scope.updateStatus(
                        {
                            content: "Đang xác nhận dữ liệu",
                            color: "w3-green"
                        });
                    $scope.updateResult({
                        content: "Đang xác nhận dữ liệu",
                        color: "w3-green"
                    });
                    // showImage();
                    // uploadImage();
                    capture_send();
                }

                /* HIEN THI ANH */
                /* ACTION TIM KIEM VA HIEN THONG TIN */
                /* CHUYEN DOI DUOC THONG TIN GIUA CAC KHACH HANG */
            } break;
            case 2:{
                showModal("page-2");
                hideModal("page-3");
                /* THEM GHI CHU SO THICH DA THEM TRUOC DO */
                /* DAY LA GHI CHU KHACH HANG */
            } break;
            case 3:{
                hideModal("page-2");
                showModal("page-3");
                document.getElementById("price").focus();
                /* THEM GIA TIEN */
                /* NHUNG LUU Y KHAC */
                /* SAVE ==> 0*/
                


            } break;
            default:{
                console.log("NOT FOUND PAGE")
            }
        }
    }
    $scope.socket = socket;
    // $scope.updateStatus = function(cont){
    //     $scope.status = cont;
    // }
    $scope.updateStatus({ content: "Nhấn ENTER để chụp ảnh", color: "w3-blue"})
    $scope.updateImage = function(){
        $scope.updateStatus("ĐÃ CHỤP ẢNH - ENTER để quay lại")
        capture_send();
    }
    $scope.updateRecord = function(){
        capture_send_video("UNKNOWN");
    }
    $scope.strigger = function(){
        $scope.catchKey(STRIGGER);
    }
    $scope.catchKey = function(key){
        console.log(key);
        switch(key){
            case NE_PAGE:
            case NEX_PAGE:{
                if(time_strigger != 0){
                    clearTimeout(time_strigger);
                    time_strigger = 0;
                }
                PAGE_PREV = PAGE_INDEX;
                PAGE_INDEX = PAGE_INDEX + 1;
                console.log("NEXT-PAGE:", PAGE_INDEX);
                if(PAGE_INDEX < 2){

                } else {
                    /* SAVE DATE */

                    /* */
                    PAGE_INDEX = 0;
                    PAGE_PREV = 3;
                }
                $scope.page(PAGE_INDEX);
            } break;
            case PRE_PAGE:{
                if(PAGE_INDEX == 0){
                    console.log("CANNOT PREV WHEN PAGE_INDEX:", PAGE_INDEX);
                    return;
                }
                PAGE_PREV = PAGE_INDEX;
                PAGE_INDEX = PAGE_INDEX - 1;
                console.log("NEXT-PAGE:", PAGE_INDEX);
                console.log("PREV-PAGE");
                if(PAGE_INDEX < 1){
                    /* CLEAR ALL ACTION */

                    /* */
                    PAGE_INDEX = 0;
                } else {
                    $scope.page(PAGE_INDEX);
                }
                $scope.page(PAGE_INDEX);
            } break;
            case OUT_PAGE:{
                console.log("OUTLET-PAGE");
                if(time_strigger != 0){
                    time_strigger = 0;
                } else {
                    if(PAGE_INDEX != 0){
                        confirm("BẠN MUỐN HUỶ THAO TÁC? [Enter] để hoàn tất");
                    }
                }
                
                PAGE_INDEX = 0;
                $scope.page(PAGE_INDEX);
            } break;
            case STRIGGER:{
                if(PAGE_INDEX == 0){
                    $scope.catchKey(NEX_PAGE);
                    time_strigger = setTimeout(function(){
                        $scope.catchKey(OUT_PAGE);
                    }, 20000);
                }
            } break;
            default:{
                if((key > 48 && key < 59) && (PAGE_INDEX == 2)){
                    if($scope.state_note[key - 48 - 1] == undefined){
                        console.log(key - 48);
                        return;
                    } else {

                    }
                    if($scope.state_note[key - 48 - 1].chose == true){
                        $scope.state_note[key - 48 - 1].chose = false;
                        jQuery("#tr-" + (key - 48).toString()).removeClass("w3-red");
                    } else {
                        $scope.state_note[key - 48 - 1].chose = true;
                        jQuery("#tr-" + (key - 48).toString()).addClass("w3-red");
                    }                    
                } else if((key > 48 && key < 58) && (PAGE_INDEX == 3)){
                    	try{
    			    document.getElementsById("price").focus();
			} catch (e) {
			    console.log(e);
			}
                    // console.log("Hello");
                }
                /* NOTHING */
            }
        }
    }
    $scope.upDataRecog = function(){
        console.log("RECOG:", data_recog);
        if(data_recog.length == 0){
            id_ = (new Date()).getTime().toString();
            $scope.updateStatus({content: "Không tìm thấy", color: "w3-red"});
            // $scope.updateResult({content: "Không nhận ra!. Học mới!", color: "w3-red"});
            $scope.catchKey(NEX_PAGE);
        } else {
            $scope.data_recog = data_recog;
            $scope.updateStatus({
                content: "Đã tìm thấy. ENTER tiếp tục",
                color: "w3-yellow"
            })
            // $scope.updateStatus({content: c, color: "w3-red"});
        }
    }
    $scope.upDataCustomer = function(){
        console.log("CUSTOMER:", data_customer);
        if(data_customer.length == 0){
            $scope.data_recog = [];
        } else {
            for(i in data_customer){
                $scope.data_customer.push(data_customer[i]);
                $scope.customers = data_customer;
            }
        }
    }
});

function capture_send(){
    console.log("1234")
    uploadImage();
    showImage();
    recordTimeSecond(TIME_RECORD);
    // sendLinkImage();
    // setTimeout(function(){
    //     showCamera();
    // }, TIME_TO_RECORD);
}
jQuery("#btnRecog").hide();
jQuery("#btnCustomer").hide();
function strigger_active(t){
    jQuery("#btnStrigger").click();
}
socket.on("message", function(t, m){
    if(t.topic != 'MainApp'){
        strigger_active(t);
        return;
    }
    var to = JSON.parse(t.message);
    console.log(to);
        if((to.source == "KeyBoard")){
            capture_send();
        } else if (to.func == "recognize") {
            console.log("RECOGNIZE", to.data);
            var l = [];
            for(i in to.data){
                if((to.data[i].ID != "Unknown") && (to.data[i].ID != "")){
                    l.push(to.data[i]);
                    console.log("ID:", to.data[i].ID);
                    socket.emit("check_info", {id: to.data[i].ID});
                }
            }
            data_recog = l;
            jQuery("#btnRecog").click();
        } else if ((to.source == "APIGetPost") && (to.func == "register")) {
            let a = jQuery("#notify");
            jQuery("#labelNotify").text("STATUS: " + to.data.status + " - ID: " + to.data.ID);
            a.show();
            if(a.hasClass("w3-blue")){
                a.removeClass("w3-blue");
            } else if(a.hasClass("w3-red")){
                a.removeClass("w3-red");
            } else {
                //nothing in hewe
            }
            if(to.data.status == true){
                a.addClass("w3-blue");
            } else {
                a.addClass("w3-red");
            }
            setTimeout(function(){
                jQuery("#notify").hide();
            }, TIME_SLEEP_NOTIFY);
        }else {
            console.log("TEST", to.func);
        }
})

socket.on("infor_customer", function(data){
    console.log("INFOR-CUSTOMER:", data);
    data_customer = data;
    jQuery("#btnCustomer").click();
})
