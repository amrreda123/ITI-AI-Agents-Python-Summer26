// 1- Bottle Game: return two random names
const getTwoRandomNames = (names) => {
    let first = Math.floor(Math.random() * names.length);
    let second = Math.floor(Math.random() * names.length);
    while (first === second) {
        second = Math.floor(Math.random() * names.length);
    }
    return [names[first], names[second]];
}
document.write(getTwoRandomNames(["Ahmed", "Islam", "Ali", "Sandra"]));


// 2- convert each letter of first word to Capital (Pascal Case)
const toTitleCase = (str) => str.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
document.write("<br>" + toTitleCase("ahmed islam ali sandra"));


// 3- return the longest word within the input
const getLongestWord = (sentence) => sentence.split(' ').sort((a, b) => b.length - a.length)[0];
document.write("<br>" + getLongestWord("ahmed islam ali sandra"));


// 4- returns a passed string with letters in alphabetical order
const sortStringAlphabetically = (str) => str.split('').sort().join('');
document.write("<br>" + sortStringAlphabetically("ahmed"));


// 5- get the month name from a particular date
const getMonthName = (date) => {
    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];
    return monthNames[date.getMonth()];
}
document.write("<br>" + getMonthName(new Date()));


// 6- find the area of Circle and get the radius as function's input
const getCircleArea = (radius) => Math.PI * (radius ** 2);
document.write("<br>" + getCircleArea(5));
