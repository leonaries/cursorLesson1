// 获取所有待办事项
function fetchTodos() {
    fetch('/api/todos')
        .then(response => response.json())
        .then(todos => {
            const todoList = document.getElementById('todoList');
            todoList.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.innerHTML = `
                    ${todo.content}
                    <button class="delete-btn" onclick="deleteTodo(${todo.id})">删除</button>
                `;
                todoList.appendChild(li);
            });
        });
}

// 添加新的待办事项
function addTodo() {
    const input = document.getElementById('todoInput');
    const content = input.value.trim();
    
    if (content) {
        fetch('/api/todos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ content: content })
        })
        .then(response => response.json())
        .then(() => {
            input.value = '';
            fetchTodos();
        });
    }
}

// 删除待办事项
function deleteTodo(id) {
    fetch(`/api/todos/${id}`, {
        method: 'DELETE'
    })
    .then(() => {
        fetchTodos();
    });
}

// 页面加载时获取所有待办事项
document.addEventListener('DOMContentLoaded', fetchTodos); 