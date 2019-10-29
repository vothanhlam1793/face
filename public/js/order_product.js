class OrderProduct {
    constructor(){
        this.type = "order_product";
        this.obj = {
            idorder_buss: 0,
            idproduct: 0,
            favor: 0,
            favor_support: 0,
            amount: 0
        }
    }
    setOrderBuss(p){
        this.obj.idorder_buss = p;
    }
    setProduct(n){
        this.obj.idproduct = n;
    }
    setAmount(d){
        this.obj.amount = d;
    }
    setFavor(d){
        this.obj.favor = d;
    }
    setFavorSupport(a){
        this.obj.favor_support = a;
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

function getOrder(support, condition, value){
    if((condition != undefined) && (value != undefined)){
        return new Promise((resolve, reject)=>{
            angGet(support, "/table?table=order_product&c1="+condition+"&v1="+value).then(resolve).catch(reject);
        })
    } else {
        return new Promise((resolve, reject)=>{
            angGet(support, "/table?table=order_buss").then(resolve).catch(reject);
        })
    }
}