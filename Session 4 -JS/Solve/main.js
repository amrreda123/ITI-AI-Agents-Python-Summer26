// Solve Assignment 1

// userInput.trim() === ""  // => User clicked OK

let message = prompt("Please enter a message:");
// if (message === null || message.trim() === "") {
    for (let i = 1; i <= 6; i++) {
        document.write("<h" + i + ">" + message + "</h" + i + ">");
    }
// }else {
//     document.write("No message was entered.");
// }

// Solve Assignment 2

// isNaN(); // => Is Not A Number
let sum = 0;
let userInput;

do {
    userInput = prompt("Enter a number (Enter 0 to stop):");

    if (userInput === null) { // User clicked cancel
        break;
    }

    if (isNaN(userInput) || userInput.trim() === "") {
        alert("Invalid input! Please enter a numeric value.");
        continue;
    }

    let number = Number(userInput);

    if (number === 0) {
        break;
    }

    sum += number;
} while (sum <= 100);

document.write("<h3>The total sum of the entered values is: " + sum + "</h3>");


// Solve Assignment 3

let Validation = function (input) {
    if (input === null || input.trim() === "" || isNaN(input)) {
        return false;
    }
    return true;
}
let num1 = prompt("Enter the first number:");
let num2 = prompt("Enter the second number:");
let num3 = prompt("Enter the third number:");

if (Validation(num1) && Validation(num2) && Validation(num3)) {
    let sum = Number(num1) + Number(num2) + Number(num3);
    let multiply = Number(num1) * Number(num2) * Number(num3);
    let division = Number(num1) / Number(num2) / Number(num3);
    document.write("<h1>Adding -- Multiplying -- and dividing 3 values</h1>");
    document.write("<hr>");
    document.write("<p><span style='color:red;'>sum of the 3 values </span>" +
            num1 + "+" + num2 + "+" + num3 + " = " + sum + "</p>");
    document.write("<p><span style='color:red;'>multiplication of the 3 values </span>"
            + num1 + "*" + num2 + "*" + num3 + " = " + multiply + "</p>");
    document.write("<p><span style='color:red;'>division of the 3 values </span>" +
            num1 + "/" + num2 + "/" + num3 + " = " + division + "</p>");
} else {
    document.write("<h3>Please enter valid numbers for all three inputs.</h3>");
}