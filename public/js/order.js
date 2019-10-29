class Order {
    constructor(){
        this.type = "order_buss";
        this.obj = {
            idcustomer: "",
            total_price: "",
            note: "",
            create_at: new Date().toMysqlFormat()
        }
    }
    setCustomer(p){
        this.obj.idcustomer = p;
    }
    setTotalPrice(n){
        this.obj.total_price = n;
    }
    setNote(d){
        this.obj.note = d;
    }
    setCreateAt(d){
        this.obj.create_at = d;
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
            angGet(support, "/table?table=order_buss&c1="+condition+"&v1="+value).then(resolve).catch(reject);
        })
    } else {
        return new Promise((resolve, reject)=>{
            angGet(support, "/table?table=order_buss").then(resolve).catch(reject);
        })
    }
}