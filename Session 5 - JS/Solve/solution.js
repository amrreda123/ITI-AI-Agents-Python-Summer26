// 1. Create the student object
const student = {
  name: "Ahmed",
  age: 21,
  subjects: [
    { subject: "Math", score: 85 },
    { subject: "English", score: 90 },
    { subject: "Science", score: 95 }
  ]
};

// 2. Create getTotalGrade function
function getTotalGrade(studentObj) {
  let total = 0;
  for (let i = 0; i < studentObj.subjects.length; i++) {
    total += studentObj.subjects[i].score;
  }
  return total;
}

// 3. Create getAverageGrade function
function getAverageGrade(studentObj) {
  const average = getTotalGrade(studentObj) / studentObj.subjects.length;
  return average;
}


document.write("Original Student:<pre>" + JSON.stringify(student,null,2) + "</pre>");
document.write("<br>");
document.write("Total Grade: " + getTotalGrade(student)); 
document.write("<br>");
document.write("Average Grade: " + getAverageGrade(student)); 
document.write("<br>");

