// Hoisting:
//  var userName,degree,courseName,isActive,testScope;


// console.log("hello from External file .js ....");


// variable : name . value , type    --- address
// declare => var => var name =value;
//  string ,boolean , Number , undefined 

// console.log("before declare rana= ",rana);
// console.log("before declare username= ",userName);
// var userName ='e'; // declare + assign
// console.log(userName);
// console.log(typeof userName);


// var userName="khaled ";// redeclare


// var degree=100.59;    // IEEE 754 => Double 8B
// console.log(degree ,typeof degree);
// degree="test case "; 
// console.log(degree ,typeof degree);

// var isActive = true;
// console.log(isActive, typeof isActive);

// var courseName;

// console.log(courseName, typeof courseName);

// console.log("before if *** testScope= ",testScope);
// if(2<5){
//     var testScope=" global";
//     courseName='Js';
//     console.log("****** in if ****************");
//     console.log(testScope);
// }
// console.log("****** after if ****************");
//     console.log(testScope);
// console.log(courseName, typeof courseName);

//  console.log("before for i= ",i); //
// for(var i=0;i<10;i++){
//     console.log("i= ",i); //0-9
// }

//     console.log("after i= ",i); // 10 global



// function testScopeVar(){ // var test;
//     console.log("*******before declare*********",test);
//     var test="hello from fun"; //local
//     console.log(test);
// }
// testScopeVar();
// console.log(test); error: not defined
// **********************************************************


//   loosley type 
// scope 
// not def
// hoisting

/* 
Ecma5:ES5 var problems:
1- hoisting
2- redeclare 
3- var local only in function , otherwise global

*/
// solutions: let , const

// console.log("before declare username= ",userName);
 let userName='dr.ayman lotfy';// ='e'; // declare + assign
// console.log(userName);
// console.log(typeof userName);
// // userName=100;
// // console.log(userName);


// //  var userName="khaled ";// redeclare

// // console.log(degree ,typeof degree);

// console.log(PI);
const PI=3.14;
console.log(PI);
// PI=5.5;

 let degree=100.59;    // IEEE 754 => Double 8B
// console.log(degree ,typeof degree);
// degree="test case "; 
// console.log(degree ,typeof degree);


    //   console.log(testScope);// error not defined

// if(2<5){
//     //  console.log(testScope);

//     let testScope=" global";
   
//     console.log("****** in if ****************");
//     console.log(testScope);
// }
// console.log("****** after if ****************");
//     // console.log(testScope);

// //  console.log("before for i= ",i); //
// for(let i=0;i<10;i++){
//     console.log("i= ",i); //0-9
// }

    // console.log("after i= ",i); // 10 global



let track='AI-Agent';
// let str= "data info: 'user name' :"+userName +"tracks :"+ track +"degree : "+degree;
let str= `"data info":  
 'user name' : ${userName} 
  tracks : ${track}
  degree : ${degree *10}`;

console.log(str);

