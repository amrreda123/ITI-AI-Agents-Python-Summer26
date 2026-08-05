/** 
 *  Functions :
 *  1- Function Declaration (statement)
 *  2- Function Expression
 *  3- Anonymouse Function
 *  4- CallBack Function
 *  5- Arrow Fucntion (ES6)
 *  6- IIFE (IMMidialtely Invoked Fucntion Expression)
 *  7- Concise Method (memebre class function,obj)
 */
// hoisting : 
/*
  var sum2Num=function sum2Num(){
    let result=0;
    for(let i=0;i<arguments.length;i++){
        result+=arguments[i];
    }
    return result;
}
  

*/




//---- functions  not input and no return
// function name (){body}

// let username="yara ahmed"; //global
// function sayHello(username){ // local  let username;
//     // debugger;
//     console.log("hello...",username);
//     // return ;
//     return 5;
// }
// console.log("start..");
// // call
// let result=sayHello("gana"); //gana
// console.log(result);
// sayHello("ali");
// sayHello(10);
// sayHello(true);
// sayHello('');
// sayHello();
// // console.log(username);


// function sum2Num(num1,num2){
//     return num1+num2;
// }
// function sum2Num(num1,num2=0,num3=0){
//     // debugger;
//     console.log(arguments);
//     return num1+num2+num3;
// }

// console.log(sum2Num(10,20));
// console.log("******************************");
// // v0.2
// function sum2Num(){
//     // debugger;
//     // console.log(arguments); //array like
//     let result=0;
//     for(let i=0;i<arguments.length;i++){
//         result+=arguments[i];
//     }
//     return result;
// }
// console.log(arguments); Error

// console.log(sum2Num(10,20));
// console.log(sum2Num(10,true));
// console.log(sum2Num(10,'ali'));
// console.log(sum2Num("ali",'ahmed'));
// console.log(sum2Num("ali "));
// console.log(sum2Num(10));
// Numbers=[-10,...,0,... 10,NaN]

// parsInt ,parseFLoat
// let x="     55 8  ";
//  console.log("x= ",parseInt(x));
// alg: 1- trim  => "10" ,"eman" , '55 8'
// 2-digit => 10 number , char stop ,NAN

// console.log(Number(x));
// console.log(+(x));

// sum
// console.log(sum2Num("ali ","tamer"));
// console.log(sum2Num(10));
// console.log(sum2Num(10,20));
// console.log(sum2Num(10,20,5));
// console.log(sum2Num(10,20,5,6));
// console.log(sum2Num(10,20,5,6,89));
// console.log(sum2Num(10,20,5,6,89,9,7,8));

// arg
// type of


// console.log(typeof sum2Num);
// sum2Num=10;
// console.log(sum2Num,typeof sum2Num);



 /**********************
 * 2- Fucntion Expression (function is a varible)
 */
// console.log(sum2Num);
// sum2Num();
// const sum2Num=function sum2Num(){
//     let result=0;
//     for(let i=0;i<arguments.length;i++){
//         result+=arguments[i];
//     }
//     return result;
// }
// const sum2Num=function(){
//     let result=0;
//     for(let i=0;i<arguments.length;i++){
//         result+=arguments[i];
//     }
//     return result;
// }
// console.log(sum2Num());
// console.log(sum2Num(5,9));
// sum2Num=990000000000000;
// console.log(sum2Num);











 /**********************
 * ES6  :  Arrow Fucntion (function Expression + =>)
 * function Keyword ==== (=>)
 * 
 * input =>  output     
 */

// const sum2Num=function(num1,num2){
//     return num1+num2;
// }
// const sum2Num=(num1,num2)=>{
//     return num1+num2;
// }
// const sum2Num=(num1,num2)=> console.log(num1+num2);
// const sum2Num=(num1,num2)=> num1+num2;
// const sum2Num=a=> a*10;

// const sum2Num=()=>{
//     let result=0;
//     for(let i=0;i<arguments.length;i++){ // error
//         result+=arguments[i];
//     }
//     return result;
// }



// Dialogs
// display msg
// console.log(alert("hello ya AI Agent"));

// ask T|F
// let res=confirm("ARE u sure?");
// console.log(res);

// take i/p
// let res=prompt("enter your name plz.",'ex.ali');
// console.log(res);



// Q: take 2 numbers => alert sum?

// let num1,num2;
// do{
//      num1=prompt("enter num1:");

// }while(isNaN(num1));
// do{
//      num2=prompt("enter num2:");

// }while(isNaN(num2));

// alert(+num1+Number(num2));

// let num2=prompt("enter num2:");
// alert(+num1+Number(num2));


// document.writeln("hello ya python..");
// document.writeln("<h2>hello ya python..</h2>");


