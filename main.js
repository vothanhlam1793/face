var fs = require('fs');
var express = require('express');
var bodyParser = require('body-parser');
var mysql = require("./classMysql-v2");

var config = JSON.parse(fs.readFileSync('config.json', 'utf8'));
var object_define = JSON.parse(fs.readFileSync('element.json', 'utf8'));
var mongo = require("./mongodb")

var mqtt = require('mqtt')
// var clientMqtt  = mqtt.connect('mqtt://11.12.13.147')
var clientMqtt  = mqtt.connect('mqtt://localhost')
// var clientMqtt = mqtt.connect('mqtt://broker.hivemq.com');
clientMqtt.on('connect', function () {
  clientMqtt.subscribe('MainApp', function (err) {
    if (!err) {
        clientMqtt.publish('/face/hello', 'Hello mqtt');
        
    }
  });
  clientMqtt.subscribe('/strigger/+', function (err) {
    if (!err) {
        clientMqtt.publish('/face/hello', 'Hello mqtt');
        
    }
  });
  clientMqtt.subscribe('tele/strigger/rf/RESULT', function (err) {
    if (!err) {
        clientMqtt.publish('/face/hello', 'Hello mqtt');
        
    }
  });
})

clientMqtt.on('message', function (topic, message) {
    console.log(message.toString())
})

var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
const fileUpload = require('express-fileupload');
 
app.use(fileUpload());

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ // to support URL-encoded bodies
    extended: true
}));

app.use(express.static('public'));
app.set('view engine', 'ejs');
app.set('views', './views');

app.get("/", function(req, res) {
    res.render("index", {
        mainPage: "index",

    });
});

app.get("/testcam", function(req, res){
    res.render("testcam")
})
app.get("/camera", function(req, res){
    res.render("camera");
})

app.get("/record", function(req, res){
    res.render("record")
})

app.get("/object", function(req, res){
    res.send({
        status: "ERROR",
        data: "CANNOT FOUND OBJECT, YOU CAN DEFINE BEFORE USING",
    })
})
app.get("/object/:obj", function(req, res) {
    if((object_define.object[req.params.obj] == undefined)||(req.params.obj == undefined)) {
        res.send({
            status: "ERROR",
            data: "CANNOT FOUND OBJECT, YOU CAN DEFINE BEFORE USING",
        });
    } else {
        res.render("element", {
            mainPage: req.params.obj,
            form: object_define.object[req.params.obj].element,
            title: object_define.object[req.params.obj].element
        });
    }
});

app.post("/insert/:table", function(req, res){
    var a = req.body;
    mysql.connect2query(object_define.database[object_define.object[req.params.table].database], mysql.object2query(a, a, req.params.table)).then((a)=>{
        res.render("back")
    }).catch((e)=>{
        res.send({
            status: "ERROR",
            data: e
        })
    })
});

app.post("/insertid/:table", function(req, res){
    var a = req.body;
    mysql.connect2query(object_define.database[object_define.object[req.params.table].database], mysql.object2query(a, a, req.params.table)).then((a)=>{
        res.send({
            status: "OK",
            data: {
                id: a.insertId
            }
        })
    }).catch((e)=>{
        console.log(e)
        res.send({
            status: "ERROR",
            data: e
        })
    })
});

app.get("/table", function(req, res){
    var a = req.query;
    console.log(a.table);
    if(a.c1 == undefined){
        mysql.connect2query(object_define.database[object_define.object[a.table].database], "select * from " + a.table).then((a)=>{
            res.send({
                status: "OK", 
                data: a
            });
        }).catch((e)=>{
            console.log(e);
            res.send({
                status: "ERROR",
                error: e.code
            })
        })
    } else {
        mysql.connect2query(object_define.database[object_define.object[a.table].database], "select * from " + a.table + " where " + a.c1 + "='" + a.v1 + "'").then((a)=>{
            res.send({
                status: "OK", 
                data: a
            });
        }).catch((e)=>{
            console.log(e);
            res.send({
                status: "ERROR",
                error: e.code
            })
        })
    }
    
})

app.put("/update", function(req, res) {
    var a = req.body;
    console.log("HERE ==> ", a);
    mysql.connect2query(object_define.database[object_define.object[a.table].database], mysql.update2query("id" + a.table, a.data["id" + a.table], a.table, a.data)).then((a)=>{
        console.log(a);
        res.send({
            status: "OK",
            data: ""
        })
    }).catch((e)=>{
        console.log(e)
        res.send({
            status: "ERROR",
            data: ""
        })
    })
})

app.get("/delete", function(req, res) {
    var a = req.query;
    console.log(a);
    mysql.connect2query(object_define.database[object_define.object[a.table].database], mysql.delete2query("id" + a.table, a.id, a.table)).then((a)=>{
        res.send({
            status: "OK",
            data: ""
        })
    }).catch((e)=>{
        res.send({
            status: "ERROR",
            data: "e"
        })
    })
});

app.post('/upload/:type', function(req, res) {
    console.log("TYPE:", req.params.type);
    let type = {};
    if(req.params.type == "record"){
        type.type = ".webm";
        type.link = "record/"
    } else if (req.params.type == "image"){
        type.type = ".png";
        type.link = "img/"
    } else {
        res.send({
            status: "ERROR",
            data: "CANNOT FIND TYPE"
        });
        return;
    }
    if (Object.keys(req.files).length == 0) {
      return res.status(400).send('No files were uploaded.');
    }
  //    console.log(req.files);
      console.log(req.body);
    // The name of the input field (i.e. "sampleFile") is used to retrieve the uploaded file
    let sampleFile = req.files.data;
  
    // Use the mv() method to place the file somewhere on your server
    sampleFile.mv("public/" + type.link + req.body.fname + type.type, function(err) {
        if (err){
            console.log(err)
            return res.status(500).send(err);
        }
        res.send({
            status: "OK",
            data: "/" + type.link + req.body.fname + type.type
        });
        // clientMqtt.publish('APIGetPost', JSON.stringify({
        //     "source":"MainApp",
        //     "func":"capture",
        //     "data":{
        //         "ID":"",
        //         "base64image":__dirname + "/public/img/" + req.body.fname + ".png",
        //     }
        // }));
    });
});

var topic_main_face = "APIGetPost"
function sendMqttInforCamera(link){
    clientMqtt.publish(topic_main_face, JSON.stringify(link))
}

io.on('connection', function(socket) {
   socket.on('disconnect', function () {
      console.log('A user disconnected');
   });
   console.log("Connection on");
   clientMqtt.on("message", function(topic, message){
       console.log("ABC:", topic, message);
       socket.emit("message", {topic: topic, message: message.toString()});
   })
    socket.on("image", function(data){
        sendMqttInforCamera(data);
    });
    socket.on("record", function(data){
        sendMqttInforCamera(data);
    })
    socket.on("save_data", function(da){
        console.log("242", da);
        // let str = {};
        let t = new Date();
        // str["note-" + t.getTime().toString()] = da.note;
        if(da.staff == undefined)
            da.staff = 0;
        mongo.rowupdate("face", "customers", {
            $push:{
                note:{
                    date: t,
                    content: da.note,
                    staff: da.staff,
                    price: da.price
                }
            }
        }, {id: da.id}, function(r){
            console.log(r);
        })
    })
    socket.on("check_info", function(da){
        console.log();
        mongo.find("face", "customers", da, function(r){
            if(r.length == 0){
                /* DANG KI MOI */
                // let t = new Date();
                // insert("creta", "customer", {id: t.getTime()}, function(r){
                    // console.log(r.ops[0].id);
                //     socket.emit("infor_customer", r.ops[0]);
                // })
                console.log(r);
                socket.emit("infor_customer", r)
            } else if (r.length == 1){
                /* TRUONG HOP DUNG NE */
                socket.emit("infor_customer", r)
            } else {
                /* LOI HE THONG */
            }
        })
    })
    socket.on("create_customer", function(da){
        console.log(da);
        let str = {};
        let t = new Date();
        str["note-" + t.getTime().toString()] = da.note;
        mongo.insert("face", "customers", da, function(r){
            console.log(r);
        })
    })
});

http.listen(config.port);
