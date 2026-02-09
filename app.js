const STORAGE_KEY = "todo-items";
const listEl = document.getElementById("list");
const template = document.getElementById("item-template");
const titleInput = document.getElementById("title-input");
const descInput = document.getElementById("desc-input");
const addButton = document.getElementById("add-btn");

let items = loadItems();

function loadItems() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    return [];
  }
}

function saveItems() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function renderItems() {
  listEl.innerHTML = "";
  items.forEach((item) => {
    const node = template.content.firstElementChild.cloneNode(true);
    const checkbox = node.querySelector("input[type='checkbox']");
    const titleEl = node.querySelector(".title");
    const descEl = node.querySelector(".desc");
    const deleteBtn = node.querySelector(".delete");

    titleEl.textContent = item.title;
    if (item.desc) {
      descEl.textContent = item.desc;
    } else {
      descEl.textContent = "";
      descEl.style.display = "none";
    }

    checkbox.checked = item.done;
    node.classList.toggle("done", item.done);

    checkbox.addEventListener("change", () => {
      item.done = checkbox.checked;
      node.classList.toggle("done", item.done);
      saveItems();
    });

    deleteBtn.addEventListener("click", () => {
      items = items.filter((entry) => entry.id !== item.id);
      saveItems();
      renderItems();
    });

    listEl.appendChild(node);
  });
}

function addItem() {
  const title = titleInput.value.trim();
  if (!title) {
    titleInput.focus();
    return;
  }
  const desc = descInput.value.trim();

  items.unshift({
    id: Date.now(),
    title,
    desc,
    done: false,
  });

  saveItems();
  renderItems();
  titleInput.value = "";
  descInput.value = "";
  titleInput.focus();
}

addButton.addEventListener("click", addItem);
titleInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    event.preventDefault();
    addItem();
  }
});

renderItems();
