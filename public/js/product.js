class Product {
    constructor(id){
        this.type = "product";
        this.obj = {
            code: "",
            price: "",
            name: "",
            detail: ""
        }
        if(id != undefined){
            jQuery.get("/table?table=" + this.type + "&c1=id" + this.type + "&v1=" + id, function(data){
                this.obj = data.data[0];
                console.log(this.obj)
            })
        }
        
    }
    setPrice(p){
        this.obj.price = p;
    }
    setName(n){
        this.obj.name = n;
    }
    setDetail(d){
        this.obj.detail = d;
    }
    setCode(d){
        this.obj.code = d;
    }
    create(support){
        if(support == undefined){
            return new Promise((resolve, reject)=>{

            })
        } else {
            return new Promise((resolve, reject)=>{
                angCreateElement(this.obj, this.type, support).then(resolve).catch(reject);
            })
        }
    }
}

function getProduct(support, condition, value){
    if((condition != undefined) && (value != undefined)){
        return new Promise((resolve, reject)=>{
            angGet(support, "/table?table=product&c1="+condition+"&v1="+value).then(resolve).catch(reject);
        })
    } else {
        return new Promise((resolve, reject)=>{
            angGet(support, "/table?table=product").then(resolve).catch(reject);
        })
    }
}


function productIdToPrice(array, id){
    var o = searchArray("idproduct", id, array);
    return o.price;
}

function productIdToName(array, id){
    console.log("Hello");
    var o = searchArray("idproduct", id, array);
    return o.name;
}