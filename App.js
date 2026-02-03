import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [details, setDetails] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);

  const [formData, setFormData] = useState({
    name: "",
    email: "",
    mobile: ""
  });

  const API = "http://127.0.0.1:8000";

  // ---------------- FETCH DATA ----------------
  const fetchDetails = async () => {
    const res = await axios.get(`${API}/get_details`);
    setDetails(res.data);
  };

  useEffect(() => {
    fetchDetails();
  }, []);

  // ---------------- FORM CHANGE ----------------
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // ---------------- ADD / UPDATE ----------------
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (editId) {
      // UPDATE
      await axios.put(`${API}/update_detail/${editId}`, formData);
    } else {
      // ADD
      await axios.post(`${API}/add_detail`, formData);
    }

    setFormData({ name: "", email: "", mobile: "" });
    setEditId(null);
    setShowForm(false);
    fetchDetails();
  };

  // ---------------- EDIT ----------------
  const handleEdit = (detail) => {
    setFormData({
      name: detail.name,
      email: detail.email,
      mobile: detail.mobile
    });
    setEditId(detail.id);
    setShowForm(true);
  };

  // ---------------- DELETE ----------------
  const handleDelete = async (id) => {
    if (window.confirm("Are you sure you want to delete?")) {
      await axios.delete(`${API}/delete_detail/${id}`);
      fetchDetails();
    }
  };

  return (
    <div className="App">
      <h2>Customer Details</h2>

      <button onClick={() => setShowForm(!showForm)}>
        {showForm ? "Cancel" : "Add Details"}
      </button>

      {showForm && (
        <form onSubmit={handleSubmit}>
          <input
            name="name"
            placeholder="Name"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            name="mobile"
            placeholder="Mobile"
            value={formData.mobile}
            onChange={handleChange}
            required
          />
          <button type="submit">
            {editId ? "Update" : "Submit"}
          </button>
        </form>
      )}

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Mobile</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {details.map((d) => (
            <tr key={d.id}>
              <td>{d.id}</td>
              <td>{d.name}</td>
              <td>{d.email}</td>
              <td>{d.mobile}</td>
              <td>
                <button onClick={() => handleEdit(d)}>Edit</button>
                <button onClick={() => handleDelete(d.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
