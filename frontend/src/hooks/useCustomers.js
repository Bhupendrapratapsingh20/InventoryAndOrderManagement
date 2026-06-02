import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';

export function useCustomers() {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchCustomers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/customers');
      const data = response.data;
      setCustomers(data.customers || data || []);
    } catch (err) {
      const message =
        err.response?.data?.detail || err.message || 'Failed to fetch customers';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createCustomer = useCallback(async (customerData) => {
    const response = await api.post('/customers', customerData);
    setCustomers((prev) => [...prev, response.data]);
    return response.data;
  }, []);

  const updateCustomer = useCallback(async (id, customerData) => {
    const response = await api.put(`/customers/${id}`, customerData);
    setCustomers((prev) => prev.map((c) => (c.id === id ? response.data : c)));
    return response.data;
  }, []);

  const deleteCustomer = useCallback(async (id) => {
    await api.delete(`/customers/${id}`);
    setCustomers((prev) => prev.filter((c) => c.id !== id));
  }, []);

  useEffect(() => {
    fetchCustomers();
  }, [fetchCustomers]);

  return {
    customers,
    loading,
    error,
    fetchCustomers,
    createCustomer,
    updateCustomer,
    deleteCustomer,
  };
}
