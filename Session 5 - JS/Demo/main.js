// literal object

//  let id=88,stdName="testttttttttt ali",age=66;
// let track=55;
let person1={
    //k:v,k:v
    id:10,
    stdName:"jana ali",
    age:22,
    address:{
        city:"zag",
        street:10,
        toString(){
            console.log(this);
            return `address: ${this.street} , ${this.city}`;
        }
    },
    // print:function print(){
    //     // console.log(`hello from print std id= ${id} stdname=${stdName} ,age =${age} `);
    //     // console.log(`hello from print std id= ${person.id} stdname=${person.stdName} ,age =${person.age} `);
    //     console.log(this.stdName);// caller
    //     console.log(`hello from print std id= ${this.id} stdname=${this.stdName} ,age =${this.age} `);
    
    // }
    //  print:function(){
    //     console.log(`hello from print std id= ${this.id} stdname=${this.stdName} ,age =${this.age} `);
    
    // }
     print(){
        console.log(`hello from print std id= ${this.id} stdname=${this.stdName} ,age =${this.age} `);
    
    },
   toString(){
        return `name: ${this.stdName} age: ${this.age} address: ${this.address} `;
   }
}
//id,name ,age
// console.log(person);

// use:

// get, set
// console.log(person.age);
// console.log(person['age']);
// console.log(person.trackName);
// person.trackName="AI_agent";
// console.log(person);




// adding



// delete
// delete person.brach


// identity and state
// let person2={...person};
// console.log(person);
// console.log(person2);
// person2.id=50;
// console.log(person);
// console.log(person2);


// for(let key in person){
//     console.log(key,person[key]); //person.key
// }


// Method=>print
// person1.print();
// // person['print']();

// // this
// console.log(person1.address.city);

// console.log(10+"test");
// // console.log((person1).toString());
// console.log(person1 + " ");


// obj => obj 


// object object
// +''




//json
// let jsonObj=JSON.stringify(person1);
// // console.log(jsonObj);

// let jsObj=JSON.parse(jsonObj); // bk
// console.log(jsObj);


// MAth , Date
// let d=new Date(2005,4,5);
// console.log(d);


