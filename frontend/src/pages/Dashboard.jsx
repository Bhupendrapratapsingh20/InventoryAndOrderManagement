import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useToast } from '../context/ToastContext';
import '../styles/pages.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const { addToast } = useToast();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await api.get('/dashboard/stats');
        setStats(response.data);
      } catch (error) {
        const message =
          error.response?.data?.detail || 'Failed to fetch dashboard stats';
        addToast(message, 'error');
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [addToast]);

  if (loading) {
    return (
      <div className="page-container">
        <div className="loading-spinner">Loading dashboard...</div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>📊 Dashboard</h1>
        <p>Overview of your inventory & orders</p>
      </div>

      {stats && (
        <>
          {/* Stats Grid */}
          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-icon">📦</div>
              <div className="stat-content">
                <p className="stat-label">Total Products</p>
                <p className="stat-value">{stats.total_products || 0}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">👥</div>
              <div className="stat-content">
                <p className="stat-label">Total Customers</p>
                <p className="stat-value">{stats.total_customers || 0}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">📋</div>
              <div className="stat-content">
                <p className="stat-label">Total Orders</p>
                <p className="stat-value">{stats.total_orders || 0}</p>
              </div>
            </div>

            <div className="stat-card">
              <div className="stat-icon">💰</div>
              <div className="stat-content">
                <p className="stat-label">Total Revenue</p>
                <p className="stat-value">${(stats.revenue || 0).toFixed(2)}</p>
              </div>
            </div>
          </div>

          {/* Low Stock Alerts */}
          {stats.low_stock_products && stats.low_stock_products.length > 0 && (
            <div className="alert-section">
              <h2>⚠️ Low Stock Products</h2>
              <div className="alert-list">
                {stats.low_stock_products.map((product) => (
                  <div key={product.id} className="alert-item">
                    <div className="alert-info">
                      <p className="alert-title">{product.name}</p>
                      <p className="alert-sku">SKU: {product.sku}</p>
                    </div>
                    <p className="alert-stock">{product.quantity_in_stock} units</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Recent Orders */}
          {stats.recent_orders && stats.recent_orders.length > 0 && (
            <div className="recent-section">
              <h2>📈 Recent Orders</h2>
              <div className="table-container">
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Order ID</th>
                      <th>Customer</th>
                      <th>Total</th>
                      <th>Items</th>
                      <th>Created</th>
                    </tr>
                  </thead>
                  <tbody>
                    {stats.recent_orders.map((order) => (
                      <tr key={order.id}>
                        <td className="order-id">{order.id.slice(0, 8)}...</td>
                        <td>{order.customer_name || 'Unknown'}</td>
                        <td>${order.total_amount.toFixed(2)}</td>
                        <td>{order.items_count || 0}</td>
                        <td>{new Date(order.created_at).toLocaleDateString()}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

