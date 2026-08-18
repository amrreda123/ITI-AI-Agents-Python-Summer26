function main() {
    let sizeInput = prompt("Enter the size of the array:");
    if (sizeInput === null) return;
    
    let size = parseInt(sizeInput);
    if (isNaN(size) || size <= 0) {
        alert("Invalid size. Please enter a valid number greater than 0.");
        return;
    }

    let arr = [];
    for (let i = 0; i < size; i++) {
        let valInput = prompt(`Enter value for element ${i + 1}:`);
        if (valInput === null) return;
        let val = Number(valInput);
        
        while (isNaN(val) || valInput.trim() === "") {
            valInput = prompt(`Invalid input! Please enter a valid NUMBER for element ${i + 1}:`);
            if (valInput === null) return;
            val = Number(valInput);
        }
        arr.push(val);
    }

    let repeat = true;
    while (repeat) {
        let choice = prompt(`Choose an option:
a: Display array with the same receiving order
b: Display array with ascending order
c: Display array with descending order
d: Display reversed version of original array
e: Display even numbers only from array
f: Receive number and display all numbers from array divisible by it
g: Display new array with 30% discount for all numbers in original array
h: Display string which represent all numbers of array concated with ***`);
        
        if (choice === null) break;

        choice = choice.toLowerCase().trim();
        
        switch (choice) {
            case 'a':
                alert(`Array in receiving order: ${arr.join(", ")}`);
                break;
            case 'b':
                let ascArr = [...arr].sort((x, y) => x - y);
                alert(`Array in ascending order: ${ascArr.join(", ")}`);
                break;
            case 'c':
                let descArr = [...arr].sort((x, y) => y - x);
                alert(`Array in descending order: ${descArr.join(", ")}`);
                break;
            case 'd':
                let revArr = [...arr].reverse();
                alert(`Reversed array: ${revArr.join(", ")}`);
                break;
            case 'e':
                let evenArr = arr.filter(x => x % 2 === 0);
                if (evenArr.length === 0) {
                    alert("There are no even numbers in the array.");
                } else {
                    alert(`Even numbers: ${evenArr.join(", ")}`);
                }
                break;
            case 'f':
                let numInput = prompt("Enter a number to check divisibility:");
                if (numInput !== null) {
                    let num = Number(numInput);
                    if (isNaN(num)) {
                        alert("Invalid number.");
                    } else {
                        let divArr = arr.filter(x => x % num === 0);
                        if (divArr.length === 0) {
                            alert(`There are no numbers divisible by ${num}.`);
                        } else {
                            alert(`Numbers divisible by ${num}: ${divArr.join(", ")}`);
                        }
                    }
                }
                break;
            case 'g':
                let discArr = arr.map(x => (x * 0.7).toFixed(2));
                alert(`Array with 30% discount: ${discArr.join(", ")}`);
                break;
            case 'h':
                let strArr = arr.join("***");
                alert(`Array concatenated with ***: ${strArr}`);
                break;
            default:
                alert("Invalid choice. Please enter a letter from a to h.");
                break;
        }

        let repeatInput = prompt("Do you want to repeat running? (yes/y to repeat, anything else to stop)");
        if (repeatInput === null || (repeatInput.toLowerCase() !== 'yes' && repeatInput.toLowerCase() !== 'y')) {
            repeat = false;
        }
    }
}

main();
