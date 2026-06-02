import { useState, useEffect } from 'react';
import { useOrders } from '../hooks/useOrders';
import { useProducts } from '../hooks/useProducts';
import { useCustomers } from '../hooks/useCustomers';
import { useForm } from '../hooks/useForm';
import { useToast } from '../context/ToastContext';
import '../styles/pages.css';

export default function Orders() {
  const { orders, loading, error, fetchOrders, createOrder, deleteOrder } = useOrders();
  const { products } = useProducts();
  const { customers } = useCustomers();
  const { addToast } = useToast();
  const [showForm, setShowForm] = useState(false);
  const [orderItems, setOrderItems] = useState([]);
  const { form, updateForm, resetForm } = useForm({
    customer_id: '',
  });

  const handleAddItem = () => {
    setOrderItems([
      ...orderItems,
      { product_id: '', quantity: 1, id: Date.now() },
    ]);
  };

  const handleUpdateItem = (itemId, field, value) => {
    setOrderItems(
      orderItems.map((item) =>
        item.id === itemId ? { ...item, [field]: value } : item
      )
    );
  };

  const handleRemoveItem = (itemId) => {
    setOrderItems(orderItems.filter((item) => item.id !== itemId));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.customer_id) {
      addToast('Please select a customer', 'error');
      return;
    }
    if (orderItems.length === 0) {
      addToast('Please add at least one item to the order', 'error');
      return;
    }

    try {
      const items = orderItems.map(({ id, ...item }) => ({
        ...item,
        quantity: parseInt(item.quantity),
      }));
      await createOrder({
        customer_id: form.customer_id,
        items,
      });
      addToast('Order created successfully', 'success');
      resetForm();
      setOrderItems([]);
      setShowForm(false);
      fetchOrders();
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to create order';
      addToast(message, 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this order?')) return;
    try {
      await deleteOrder(id);
      addToast('Order deleted successfully', 'success');
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete order';
      addToast(message, 'error');
    }
  };

  const calculateOrderTotal = () => {
    return orderItems.reduce((total, item) => {
      const product = products.find((p) => p.id === item.product_id);
      return total + (product ? product.price * item.quantity : 0);
    }, 0);
  };

  if (loading && orders.length === 0) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading orders...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📋 Orders</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '➕ Create Order'}
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Customer *</label>
            <select
              name="customer_id"
              value={form.customer_id}
              onChange={updateForm}
              required
            >
              <option value="">Select a customer</option>
              {customers.map((customer) => (
                <option key={customer.id} value={customer.id}>
                  {customer.first_name} {customer.last_name} ({customer.email})
                </option>
              ))}
            </select>
          </div>

          <div className="order-items-section">
            <h3>Order Items</h3>
            {orderItems.map((item, index) => (
              <div key={item.id} className="order-item-row">
                <select
                  value={item.product_id}
                  onChange={(e) => handleUpdateItem(item.id, 'product_id', e.target.value)}
                  required
                >
                  <option value="">Select product</option>
                  {products.map((product) => (
                    <option key={product.id} value={product.id}>
                      {product.name} (${product.price.toFixed(2)}) - Stock: {product.quantity_in_stock}
                    </option>
                  ))}
                </select>
                <input
                  type="number"
                  min="1"
                  value={item.quantity}
                  onChange={(e) => handleUpdateItem(item.id, 'quantity', e.target.value)}
                  placeholder="Qty"
                />
                <button
                  type="button"
                  className="btn btn-sm btn-danger"
                  onClick={() => handleRemoveItem(item.id)}
                >
                  Remove
                </button>
              </div>
            ))}
            <button
              type="button"
              className="btn btn-sm btn-secondary"
              onClick={handleAddItem}
            >
              ➕ Add Item
            </button>
          </div>

          <div className="order-summary">
            <p>Order Total: <strong>${calculateOrderTotal().toFixed(2)}</strong></p>
          </div>

          <button type="submit" className="btn btn-success">
            Create Order
          </button>
        </form>
      )}

      <div className="table-container">
        {orders.length === 0 ? (
          <p className="no-data">No orders found. Create your first order!</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Customer</th>
                <th>Total Amount</th>
                <th>Items</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id}>
                  <td className="code">{order.id.slice(0, 8)}...</td>
                  <td>{order.customer_name}</td>
                  <td>${order.total_amount.toFixed(2)}</td>
                  <td>{order.items?.length || 0}</td>
                  <td>{new Date(order.created_at).toLocaleDateString()}</td>
                  <td>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(order.id)}
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

