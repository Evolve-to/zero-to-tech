const btn = document.getElementById('btn');
const numText = document.getElementById('num');
let count = 0;

btn.addEventListener('click', function () {
    count+=2;
    numText.innerText = count;
});
