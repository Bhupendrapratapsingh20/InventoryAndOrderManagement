import { useState } from 'react';
import { useProducts } from '../hooks/useProducts';
import { useForm } from '../hooks/useForm';
import { useToast } from '../context/ToastContext';
import '../styles/pages.css';

export default function Products() {
  const { products, loading, error, fetchProducts, createProduct, deleteProduct } = useProducts();
  const { addToast } = useToast();
  const [showForm, setShowForm] = useState(false);
  const { form, updateForm, resetForm } = useForm({
    sku: '',
    name: '',
    description: '',
    price: '',
    quantity_in_stock: '',
    category: '',
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        ...form,
        price: parseFloat(form.price),
        quantity_in_stock: parseInt(form.quantity_in_stock),
      };
      await createProduct(data);
      addToast('Product created successfully', 'success');
      resetForm();
      setShowForm(false);
      fetchProducts();
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to create product';
      addToast(message, 'error');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this product?')) return;
    try {
      await deleteProduct(id);
      addToast('Product deleted successfully', 'success');
    } catch (err) {
      const message = err.response?.data?.detail || 'Failed to delete product';
      addToast(message, 'error');
    }
  };

  if (loading && products.length === 0) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading products...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📦 Products</h1>
        <button
          className="btn btn-primary"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : '➕ Add Product'}
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}

      {showForm && (
        <form className="form-card" onSubmit={handleSubmit}>
          <div className="form-grid">
            <div className="form-group">
              <label>SKU *</label>
              <input
                type="text"
                name="sku"
                value={form.sku}
                onChange={updateForm}
                required
                placeholder="e.g., PROD-001"
              />
            </div>
            <div className="form-group">
              <label>Name *</label>
              <input
                type="text"
                name="name"
                value={form.name}
                onChange={updateForm}
                required
                placeholder="Product name"
              />
            </div>
            <div className="form-group">
              <label>Price *</label>
              <input
                type="number"
                name="price"
                value={form.price}
                onChange={updateForm}
                required
                min="0"
                step="0.01"
                placeholder="0.00"
              />
            </div>
            <div className="form-group">
              <label>Quantity *</label>
              <input
                type="number"
                name="quantity_in_stock"
                value={form.quantity_in_stock}
                onChange={updateForm}
                required
                min="0"
                placeholder="0"
              />
            </div>
            <div className="form-group">
              <label>Category</label>
              <input
                type="text"
                name="category"
                value={form.category}
                onChange={updateForm}
                placeholder="Product category"
              />
            </div>
            <div className="form-group">
              <label>Description</label>
              <textarea
                name="description"
                value={form.description}
                onChange={updateForm}
                placeholder="Product description"
                rows="3"
              />
            </div>
          </div>
          <button type="submit" className="btn btn-success">
            Create Product
          </button>
        </form>
      )}

      <div className="table-container">
        {products.length === 0 ? (
          <p className="no-data">No products found. Create your first product!</p>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>SKU</th>
                <th>Name</th>
                <th>Category</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td className="code">{product.sku}</td>
                  <td>{product.name}</td>
                  <td>{product.category || '-'}</td>
                  <td>${product.price.toFixed(2)}</td>
                  <td>
                    <span
                      className={
                        product.quantity_in_stock < 10 ? 'badge-warning' : 'badge-success'
                      }
                    >
                      {product.quantity_in_stock}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-sm btn-danger"
                      onClick={() => handleDelete(product.id)}
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

