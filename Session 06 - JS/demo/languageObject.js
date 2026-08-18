// Boolean , Number => toFixed(1),toString(2)=>base(2,16)

// let isActive =true;
// let isActive=new Boolean(''); // F: false,0,null,undefined,''

// let x=10;
// console.log(isActive.valueOf());
// // isActive.toString();
// if(isActive && (x=5) ){
//    // debugger; // true & true ,,, T|T
//     console.log("true -- hello from condition",x);
// }

// let num1=10;
// let num2=new Number(100.69);

// console.log(num1,num2);

// num1.toString();
// +num2.toFixed(2); 
// Number.isFinite(100)
// Number.isNaN('10');

//String   toUpperCase,indexOf,slice,split,replace

//  let str="hello python AI_AGENT _ ITI ZAG _SM 2026";
// 
// str[4]='8' => no 
// str.toLowerCase()
// str.includes('ZAG')
// str.indexOf('ZAG')
// str.indexOf('A',14)
// str.lastIndexOf('A')
// str.concat('sup: eng.Mona')
// str.replaceAll('A','$')
// console.log(str.slice(str.indexOf('python'),str.indexOf('T')+1));// start , end as index not count
// str.split(' ')






/*   Array(dynamic) :collection of arranged Data
 Declare:   literal & constructor
  */

// let arr=new Array(); //[]
// let arr=new Array(5); //length
// let arr=new Array(5,5,6); //values
// let arr=[10,5,6,true, "ali",{user:"ahmed"},10,5,5.6];

// console.log(arr);
// console.log(typeof arr);
// console.log(arr.constructor.name);





// Q1: type of ??

// array.constructor.name =>Array



// Q2: fixed size??  






// -------------------- Adding & Remove



//1-  push and pop



//2- shift , unshift

//3- splice

// arr.splice(6,0,800,700,400);

//----------------  loops types

// let arr=[10,5,6,true, "ali",{user:"ahmed"},10,5,5.6];

// for(let i=0;i<arr.length;i++){
//     console.log(i,arr[i]);
// }

// for(let item in arr){
//     console.log(item,arr[item]);
// }

// for(let item of arr){ // 0-len ,k
//     console.log(item); //arr[]
// }










//Manipulation Methods

// 4-  indexOf , includes ,slice  


//5- join  , toString
// arr.join('*');

// 6-reverse
// arr.reverse();
// let arr=[100, 500, 900, 5, 6, 9.6, 70, -5, -900, 50, 80, 10, 19, 50, 80, 90];

// Q : create method=> min of arr       
// const getMinOfArr=(op,...paramterArr)=>{
//     // let minVal=arr[0];
//     // for(let item of arr){
//     //     if(item<minVal){
//     //         minVal=item;
//     //     }

//     // }
//     // return minVal;
// // return Math.min(...arr);
// console.log(op,paramterArr);

// }
// 
// function getMinOfArr(){}

// console.log(...arr);
// let arr2=[...arr];
// let arr2=[...arr,5,9,7];
// let res=[...arr,...arr2];

// getMinOfArr('+',10,20,8);




/**
 * ES6  - rest (param) and spread Operator  ...
 */
// Q: rest op,arr 



//spread
// 1- Call Functions takes parameter-- Math.min



//2- Concat
//3- create new Array



let arr=[100, 500, 900, 5, 6, 9.6, 70, -5, -900, 50, 80, 10, 19, 50, 80, 90];


// const compFun=(a,b)=>{
//     // if(a<b) return -1;
//     // else if(a==b) return 0;
//     // else return 1;
//     return a-b;
// }

//  console.log(arr);
// // arr.sort(compFun);
//  arr.sort((a,b)=> a-b);
//  console.log(arr);

// filter
// let filterNum=arr.filter((v)=>v>80);
// // let filterNum=arr.filter((v,i)=>v>80&&i>14);

// console.log(filterNum);
// ask
// let test=arr.some((v)=>v>80);
// let test=arr.every((v)=>v>80);

// console.log(test);

// arr.forEach(element => {
//     console.log(element);
// });

console.log(arr);
let newArr=arr.map(v=>v*2);
console.log(newArr);

let res=arr.reduce((p,c)=>{
    // debugger;
   return p/=c });
console.log(res);