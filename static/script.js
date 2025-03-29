function addTodo() {
    const todo = document.getElementById("todo-input").value;
    fetch("/add", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `todo=${encodeURIComponent(todo)}`
    })
    .then(() => {
        document.getElementById("todo-input").value = '';
        loadTodos();
    });
}

function deleteTodo(id) {
    fetch(`/delete/${id}`, {
        method: "DELETE"
    }).then(loadTodos);
}

function editTodo(id, currentText) {
    const newTodo = prompt("新しいTodoを入力してください", currentText);
    if ( newTodo && newTodo !== currentText) {
        fetch(`/edit/${id}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `todo=${encodeURIComponent(newTodo)}`
        }).then(loadTodos);
    }
}

function loadTodos() {
    fetch("/list")
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("todo-list");
        list.innerHTML = '';

        data.forEach(item => {
            const li = document.createElement("li");
            const span = document.createElement("span");
            span.textContent = item.todo;

            const editBtn = document.createElement("a");
            editBtn.href = "#";
            editBtn.textContent = " [編集] ";
            editBtn.onclick = () => editTodo(item.id, item.todo);

            const deleteBtn = document.createElement("a");
            deleteBtn.href = "#";
            deleteBtn.textContent = " [削除] ";
            deleteBtn.onclick = () => deleteTodo(item.id);

            li.appendChild(span);
            li.appendChild(editBtn);
            li.appendChild(deleteBtn);
            list.appendChild(li);

        });
    });
}

document.addEventListener("DOMContentLoaded", loadTodos);
