import { useState, useEffect } from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const BASE_URL = import.meta.env.VITE_API_URL;

function App() {
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState("");

  // Load items from backend
  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await fetch(`${BASE_URL}/`);
        if (!res.ok) throw new Error("Failed to fetch items");
        const data = await res.json();
        setItems(data);
      } catch {
        toast.error("Could not load grocery list");
      }
    };
    fetchItems();
  }, []);

  // Add item
  const addItem = async () => {
    try {
      const res = await fetch(`${BASE_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newItem, completed: false }),
      });
      if (!res.ok) throw new Error();
      const newData = await res.json();
      setItems((prev) => [...prev, newData.data]);
      setNewItem("");
      toast.success("Item added");
    } catch {
      toast.error("Could not add item");
    }
  };

  // Toggle item
  const toggleItem = async (id) => {
    try {
      const res = await fetch(`${BASE_URL}/${id}/toggle/`, { method: "POST" });
      if (!res.ok) throw new Error();
      const updated = await res.json();
      setItems((prev) =>
        prev.map((item) => (item.id === id ? updated.data : item)),
      );
      toast.success("Item toggled");
    } catch {
      toast.error("Could not toggle item");
    }
  };

  // Delete item
  const deleteItem = async (id) => {
    try {
      const res = await fetch(`${BASE_URL}/${id}/`, { method: "DELETE" });
      if (!res.ok) throw new Error();
      setItems((prev) => prev.filter((item) => item.id !== id));
      toast.success("Item deleted");
    } catch {
      toast.error("Could not delete item");
    }
  };

  return (
    <div>
      <h1>Grocery Bud (React + Django)</h1>
      <input
        value={newItem}
        onChange={(e) => setNewItem(e.target.value)}
        placeholder="Add grocery item"
      />
      <button onClick={addItem}>Add</button>

      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <span
              style={{
                textDecoration: item.completed ? "line-through" : "none",
              }}
            >
              {item.name}
            </span>
            <button onClick={() => toggleItem(item.id)}>
              {item.completed ? "Undo" : "Complete"}
            </button>
            <button onClick={() => deleteItem(item.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
