import { useState, useEffect, useCallback } from 'react';
import api from '../api/axios';

export function useProducts() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await api.get('/products');
      const data = response.data;
      setProducts(data.products || data || []);
    } catch (err) {
      const message =
        err.response?.data?.detail || err.message || 'Failed to fetch products';
      setError(message);
    } finally {
      setLoading(false);
    }
  }, []);

  const createProduct = useCallback(async (productData) => {
    const response = await api.post('/products', productData);
    setProducts((prev) => [...prev, response.data]);
    return response.data;
  }, []);

  const updateProduct = useCallback(async (id, productData) => {
    const response = await api.put(`/products/${id}`, productData);
    setProducts((prev) =>
      prev.map((p) => (p.id === id ? response.data : p))
    );
    return response.data;
  }, []);

  const deleteProduct = useCallback(async (id) => {
    await api.delete(`/products/${id}`);
    setProducts((prev) => prev.filter((p) => p.id !== id));
  }, []);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  return {
    products,
    loading,
    error,
    fetchProducts,
    createProduct,
    updateProduct,
    deleteProduct,
  };
}
