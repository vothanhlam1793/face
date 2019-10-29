const MongoClient = require('mongodb').MongoClient;
const uri = "mongodb+srv://face:asrkpvg7@cluster0-ogucd.mongodb.net/test?retryWrites=true&w=majority";

function find(dbs, collect, conn, cb){
    var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
    client.connect(function(e){
        var db = client.db(dbs);
        db.collection(collect).find(conn).toArray(function(e,r){
            if(e){
                return e;
            }
            if(cb){
                cb(r);
            } else {
                console.log(r);
            }
            client.close();  
        })
    })
}
function insert(dbs, collect, obj, cb){
    var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
    client.connect(function(e){
        var db = client.db(dbs);
        db.collection(collect).insertOne(obj, function(e,r){
            if(e){
                return e;
            }
            if(cb){
                cb(r);
            } else {
                console.log(r);
            }
            client.close();  
        })
    })    
}

function rowupdate(database, collection, code_mongo, condition){
    return new Promise((resolve, reject)=>{
        var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
        client.connect(function(err, r){
            if (err) throw err;
            var db = client.db(database);
            db.collection(collection).updateOne(condition, code_mongo,function(err,r){
                if (err) reject({
                    index: "",
                    error: err
                });
                // if(cb){
                resolve(r);
                // } else {
                    // console.log(r);
                // }
                client.close();  
            })
        })            
    })
}

function update(dbs, collect, obj, conn, cb){
    var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
    client.connect(function(err, r){
        if (err) throw err;
        // console.log("E", r);
        var db = client.db(dbs);
        db.collection(collect).updateOne(conn, {$set: obj},function(err,r){
            if (err) throw err;
            if(cb){
                cb(r);
            } else {
                console.log(r);
            }
            client.close();  
        })
    })    
}

function aupdate(dbs, collect, _field, obj, conn, cb){
    var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
    client.connect(function(e){
        console.log(e);
        var db = client.db(dbs);
        db.collection(collect).updateOne(conn, {$push: 
            {
                _field: {
                    $each: obj
                }
            }
        },function(e,r){
            console.log(r);
            if(e){
                // client.close();
                return e;
            }
            if(cb){
                cb(r);
            } else {
                console.log(r);
            }
            client.close();  
        })
    })    
}

function edelete(dbs, collect, conn, cb){
    var client = new MongoClient(uri, {useNewUrlParser: true, useUnifiedTopology: true});
    client.connect(function(e){
        console.log("E:", e);
        var db = client.db(dbs);
        db.collection(collect).deleteOne(conn, function(e,r){
            console.log(e, r);
            if(e){
                // client.close();
                return e;
            }
            if(cb){
                cb(r);
            } else {
                console.log(r);
            }
            client.close();  
        })
    })    
}

// aupdate("creta", "customers", "note", {"data": 1, "content": "HIHI"}, {id: 1569201755269}, function(r){
//     console.log(r);
// } );


rowupdate("creta", "customers", {
    $push: {
        "note": {
            "date": 124, 
            "note": "Khong co ghi chu"
        }
    }}, {id: 1569253283062}, function(a){
        console.log(a)
    });
module.exports.insert = insert;
module.exports.update = update;
module.exports.find = find;
module.exports.delete = edelete;
module.exports.rowupdate = rowupdate;