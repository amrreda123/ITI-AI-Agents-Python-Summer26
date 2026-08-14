// console.log(window);
// alert("test");
// window.alert("test");

// Timer
// setTimeout(fun ,time);
const testFun=()=>{
    console.log("hello from timer method..");
}
// testFun();

// setTimeout(testFun,1000);
// setTimeout(()=>console.log("hello from timer method.."),1000);

// let id=setInterval(testFun,2000);

// clearInterval(id);
let newWindow,id;
const openChild=()=>{
    newWindow= open("selectors.html",'','width=200,height=200');
}
const closeChild=()=>{
    newWindow.close();
    stopInt();
}
const scrollChild =()=>{
    // newWindow.scrollTo(0,20);
    newWindow.scrollBy(0,20);
    console.log("test...");
    // newWindow.moveTo(0,20);
    // newWindow.moveBy(0,20);
}

const start=()=>{
   id= setInterval(scrollChild,2000);
}
const stopInt=()=>{
    clearInterval(id);
}