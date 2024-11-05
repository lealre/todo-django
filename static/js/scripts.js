//  ------- TRASH TODO TABLE ------------

// trash table
document.addEventListener("DOMContentLoaded", function () {
  const deleteTodos = document.querySelectorAll(".delete-todo");
  for (const todo of deleteTodos) {
    todo.addEventListener("submit", function (e) {
      e.preventDefault();
      const confirmed = confirm("Are you sure you want to delete this to-do?");
      if (confirmed) {
        e.currentTarget.submit();
      }
    });
  }
});

// -------- TODO TABLE -----------

// Send post to update todo state
function submitForm(todoId, todoState, todoPage) {
  document.getElementById("todo-id").value = todoId;
  document.getElementById("todo-state").value = todoState;
  document.getElementById("todo-page").value = todoPage;
  document.getElementById("todo-form").submit();
}

// Open the modal to update todo
const modal = document.getElementById("myModal");
const closeBtn = document.getElementsByClassName("close")[0];
const openModalButtons = document.getElementsByClassName("open-modal");
const modalTodoIdField = document.getElementById("modal-todo-id");
const modalTodoTitleField = document.getElementById("modal-todo-title");

Array.from(openModalButtons).forEach((button) => {
  button.onclick = function (event) {
    event.stopPropagation();
    modal.style.display = "block";

    const todoId = button.getAttribute("data-id");
    const todoTitle = button.getAttribute("data-title");

    modalTodoIdField.value = todoId;
    modalTodoTitleField.value = todoTitle;
  };
});

closeBtn.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target === modal) {
    modal.style.display = "none";
  }
};


