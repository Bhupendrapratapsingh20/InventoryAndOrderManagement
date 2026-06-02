import { useState } from 'react';
import { useCustomers } from '../hooks/useCustomers';
import { useForm } from '../hooks/useForm';
import { useToast } from '../context/ToastContext';
import '../styles/pages.css';

export default function Customers() {
  const { customers, loading, error, fetchCustomers, createCustomer, updateCustomer, deleteCustomer } = useCustomers();
  const { addToast } = useToast();
  const [showForm, setShowForm] = useState(false);
  const [editingCustomer, setEditingCustomer] = useState(null);
  const { form, updateForm, resetForm } = useForm({
    email: '',
    first_name: '',
    last_name: '',
    phone: '',
    address: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingCustomer) {
        await updateCustomer(editingCustomer.id, form);
        addToast('Customer updated successfully', 'success');
        setEditingCustomer(null);
      } else {
        await createCustomer(form);
        addToast('Customer created successfully', 'success');
      }
      resetForm();
      setShowForm(false);
      fetchCustomers();
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to save customer';
      addToast(message, 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this customer?')) return;
    try {
      await deleteCustomer(id);
      addToast('Customer deleted successfully', 'success');
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete customer';
      addToast(message, 'error');
    }
  };

  const handleEdit = (customer) => {
    setEditingCustomer(customer);
    resetForm({
      email: customer.email,
      first_name: customer.first_name,
      last_name: customer.last_name,
      phone: customer.phone || '',
      address: customer.address || '',
      city: customer.city || '',
      state: customer.state || '',
      postal_code: customer.postal_code || '',
      country: customer.country || '',
    });
    setShowForm(true);
  };

  if (loading && customers.length === 0) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading customers...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>👥 Customers</h1>
        <button
          className="btn btn-primary"
          onClick={() => { setShowForm(!showForm); setEditingCustomer(null); if (showForm) resetForm(); }}
        >
          {showForm ? 'Cancel' : '➕ Add Customer'}
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>Email *</label>
              <input
                type="email"
                name="email"
                value={form.email}
                onChange={updateForm}
                required
                placeholder="customer@example.com"
              />
            </div>
            <div className="form-group">
              <label>First Name *</label>
              <input
                type="text"
                name="first_name"
                value={form.first_name}
                onChange={updateForm}
                required
                placeholder="John"
              />
            </div>
            <div className="form-group">
              <label>Last Name *</label>
              <input
                type="text"
                name="last_name"
                value={form.last_name}
                onChange={updateForm}
                required
                placeholder="Doe"
              />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={form.phone}
                onChange={updateForm}
                placeholder="+1 (555) 123-4567"
              />
            </div>
            <div className="form-group full-width">
              <label>Address</label>
              <input
                type="text"
                name="address"
                value={form.address}
                onChange={updateForm}
                placeholder="123 Main St"
              />
            </div>
            <div className="form-group">
              <label>City</label>
              <input
                type="text"
                name="city"
                value={form.city}
                onChange={updateForm}
                placeholder="New York"
              />
            </div>
            <div className="form-group">
              <label>State</label>
              <input
                type="text"
                name="state"
                value={form.state}
                onChange={updateForm}
                placeholder="NY"
              />
            </div>
            <div className="form-group">
              <label>Postal Code</label>
              <input
                type="text"
                name="postal_code"
                value={form.postal_code}
                onChange={updateForm}
                placeholder="10001"
              />
            </div>
            <div className="form-group">
              <label>Country</label>
              <input
                type="text"
                name="country"
                value={form.country}
                onChange={updateForm}
                placeholder="United States"
              />
            </div>
          </div>
          <button type="submit" className="btn btn-success">
            {editingCustomer ? 'Update Customer' : 'Create Customer'}
          </button>
        </form>
      )}

      <div className="table-container">
        {customers.length === 0 ? (
          <p className="no-data">No customers found. Add your first customer!</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Phone</th>
                <th>City</th>
                <th>Country</th>
                <th>Joined</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {customers.map((customer) => (
                <tr key={customer.id}>
                  <td className="bold">
                    {customer.first_name} {customer.last_name}
                  </td>
                  <td className="code">{customer.email}</td>
                  <td>{customer.phone || '-'}</td>
                  <td>{customer.city || '-'}</td>
                  <td>{customer.country || '-'}</td>
                  <td>{new Date(customer.created_at).toLocaleDateString()}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-primary"
                      onClick={() => handleEdit(customer)}
                      style={{ marginRight: '8px' }}
                    >
                      Edit
                    </button>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(customer.id)}
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

