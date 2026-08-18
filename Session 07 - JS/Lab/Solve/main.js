const taskForm = document.getElementById('task-form');
const taskInput = document.getElementById('task-input');
const tasksTable = document.getElementById('tasks-table');
const deleteAllBtn = document.getElementById('delete-all');

taskForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const taskText = taskInput.value.trim();
    if (taskText === '') return;

    
    const tr = document.createElement('tr');

    tr.innerHTML = `
        <td><input type="checkbox" class="done-checkbox"></td>
        <td class="task-text">${taskText}</td>
        <td><button class="delete-btn">🗑️</button></td>
    `;

    const deleteBtn = tr.querySelector('.delete-btn');
    deleteBtn.addEventListener('click', function () {
        if (confirm("R U Sure to delete this task")) {
            tr.remove(); 
        }
    });

    const checkbox = tr.querySelector('.done-checkbox');
    const taskTd = tr.querySelector('.task-text');
    
    checkbox.addEventListener('change', function () {
        if (checkbox.checked) {
            taskTd.style.textDecoration = 'line-through';
            taskTd.style.color = '#888';
        } else {
            taskTd.style.textDecoration = 'none';
            taskTd.style.color = 'inherit';
        }
    });

    tasksTable.appendChild(tr);

    taskInput.value = '';
});

deleteAllBtn.addEventListener('click', function () {
    tasksTable.innerHTML = '';
});
