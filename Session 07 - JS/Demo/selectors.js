

//Using Tree for image Object  DOM


//Using document Methods for image Object document.images

 //---------------1- document.getElementById  naming  example


 //---------------2- document.getElementsByTagName li , ol -->li 



 //---------------3- document.getElementsByName   name attribute
 //chekboxes  -->  hoppy



 //---------------4- document.getElementByClassName
//case-senstive   -> class or more??

  
    
//ClassList new property => add, remove , toggle



//------------- 5 chaining methods to get your element

//second table rows
// document.querySelectorAll('table')[1].querySelectorAll('tr')[1]
// document.querySelectorAll('table.bPink tr ')[1]


/***********************************************
      document.querySelector() and document.querySelectorAll()
      //input for these methods is css2 selectors
*/
//tag name
//parent and direct parent
//classes with parents
//.class1.class2




/***********************************************
  Do Something           Attributes as property and as method
 */
// image src , anchor href , and checkbox(here better to use methods not property)
//.src // setAttribute()

// innerText   , innerHTML,   value , textContent


//--------------------------- Change style for all images
// Steps: 1-select:images  2- do => style
// let targetImages=document.images;
// console.log(targetImages); 
// // loop
// // for(let i=0;i<targetImages.length;i++){

// //       targetImages[i].style.border="2px solid red";
// // }
// for(let img of targetImages){

      
//        img.style.border="2px solid red";
// }


/**********************************************
 *    Section 2: 
 *   /*  create ,insert ,delete  HTML Elements */

 //------------ create Elemnts  document.createElement(TagName) returns HTML Object


 
//------------- insert the HTML from memory into the page   appendChild Method

//------------- delete Elements
//removeChild or remove-> on the same tag 

