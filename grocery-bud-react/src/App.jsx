import Items from "./components/Items";
// import { groceryItems } from "./data/groceryItems";
import { useEffect, useRef, useState } from "react";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Form from "./components/Form";
import "./App.css";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api/grocery"
).replace(/\/$/, "");

const App = () => {
  const [items, setItems] = useState([]);
  const [editId, setEditId] = useState(null);
  const inputRef = useRef(null);

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/`);
        if (!res.ok) throw new Error("Failed to fetch items");
        const data = await res.json();
        setItems(data);
      } catch (err) {
        toast.error("Could not load grocery list");
      }
    };
    fetchItems();
  }, []);

  const editCompleted = async (itemId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/${itemId}/toggle/`, {
        method: "POST",
      });
      if (!res.ok) throw new Error();
      const updated = await res.json();
      setItems((prev) =>
        prev.map((item) => (item.id === itemId ? updated.data : item)),
      );
    } catch {
      toast.error("Could not update item");
    }
  };

  const removeItem = async (itemId) => {
    try {
      const res = await fetch(`${API_BASE_URL}/${itemId}/`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error();
      setItems((prev) => prev.filter((item) => item.id !== itemId));
      toast.success("Item deleted");
    } catch {
      toast.error("Could not delete item");
    }
  };

  const addItem = async (itemName) => {
    try {
      const res = await fetch(`${API_BASE_URL}/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: itemName, completed: false }),
      });
      if (!res.ok) throw new Error();
      const newItem = await res.json();
      setItems((prev) => [...prev, newItem.data]);
      toast.success("Grocery item added");
    } catch {
      toast.error("Could not add item");
    }
  };

  const updateItemName = async (newName) => {
    try {
      const res = await fetch(`${API_BASE_URL}/${editId}/`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: newName }),
      });
      if (!res.ok) throw new Error();
      const updated = await res.json();
      setItems((prev) =>
        prev.map((item) => (item.id === editId ? updated.data : item)),
      );
      setEditId(null);
      toast.success("Item updated");
    } catch {
      toast.error("Could not update item");
    }
  };

  return (
    <section className="section-center">
      <ToastContainer position="top-center" />
      <Form
        addItem={addItem}
        updateItemName={updateItemName}
        editItemId={editId}
        itemToEdit={items.find((item) => item.id === editId)}
        inputRef={inputRef}
      />
      <Items
        items={items}
        editCompleted={editCompleted}
        removeItem={removeItem}
        setEditId={setEditId}
      />
    </section>
  );
};

export default App;
