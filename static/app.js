const form = document.getElementById("todo-form");
const input = document.getElementById("todo-input");
const list = document.getElementById("todo-list");


async function loadTodos() {

    const response = await fetch("/api/todos");
    const todos = await response.json();

    list.innerHTML = "";

    todos.forEach(todo => {

        const li = document.createElement("li");

        li.innerHTML = `
            <span class="${todo.completed ? "completed" : ""}">
                ${todo.title}
            </span>

            <div>
                <button onclick="toggleTodo(${todo.id}, ${!todo.completed})">
                    ${todo.completed ? "Undo" : "Done"}
                </button>

                <button onclick="deleteTodo(${todo.id})">
                    Delete
                </button>
            </div>
        `;

        list.appendChild(li);
    });
}


form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const title = input.value.trim();

    if (!title) {
        return;
    }

    await fetch("/api/todos", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            title: title
        })
    });

    input.value = "";

    loadTodos();
});


async function toggleTodo(id, completed) {

    await fetch(`/api/todos/${id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            completed: completed
        })
    });

    loadTodos();
}


async function deleteTodo(id) {

    await fetch(`/api/todos/${id}`, {
        method: "DELETE"
    });

    loadTodos();
}


loadTodos();
