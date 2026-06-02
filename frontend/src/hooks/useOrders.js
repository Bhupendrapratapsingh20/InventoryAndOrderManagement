import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';

export function useOrders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchOrders = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/orders');
      const data = response.data;
      setOrders(data.orders || data || []);
    } catch (err) {
      const message =
        err.response?.data?.detail || err.message || 'Failed to fetch orders';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createOrder = useCallback(async (orderData) => {
    const response = await api.post('/orders', orderData);
    setOrders((prev) => [...prev, response.data]);
    return response.data;
  }, []);

  const deleteOrder = useCallback(async (id) => {
    await api.delete(`/orders/${id}`);
    setOrders((prev) => prev.filter((o) => o.id !== id));
  }, []);

  useEffect(() => {
    fetchOrders();
  }, [fetchOrders]);

  return {
    orders,
    loading,
    error,
    fetchOrders,
    createOrder,
    deleteOrder,
  };
}
