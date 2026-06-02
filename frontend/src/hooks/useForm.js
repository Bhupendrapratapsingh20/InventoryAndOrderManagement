import { useState, useCallback } from 'react';

export function useForm(initialValues = {}, validate = null) {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback((e) => {
    const { name, value, type } = e.target;
    const parsed = type === 'number' ? (value === '' ? '' : Number(value)) : value;

    setValues((prev) => ({ ...prev, [name]: parsed }));
    setErrors((prev) => {
      if (prev[name]) {
        const next = { ...prev };
        delete next[name];
        return next;
      }
      return prev;
    });
  }, []);

  const setFieldValue = useCallback((name, value) => {
    setValues((prev) => ({ ...prev, [name]: value }));
    setErrors((prev) => {
      if (prev[name]) {
        const next = { ...prev };
        delete next[name];
        return next;
      }
      return prev;
    });
  }, []);

  const handleSubmit = useCallback(
    (callback) => async (e) => {
      e.preventDefault();

      if (validate) {
        const validationErrors = validate(values);
        if (Object.keys(validationErrors).length > 0) {
          setErrors(validationErrors);
          return;
        }
      }

      setErrors({});
      setIsSubmitting(true);

      try {
        await callback(values);
      } catch (err) {
        throw err;
      } finally {
        setIsSubmitting(false);
      }
    },
    [values, validate]
  );

  const resetForm = useCallback(
    (newValues) => {
      setValues(newValues || initialValues);
      setErrors({});
      setIsSubmitting(false);
    },
    [initialValues]
  );

  // Alias for handleChange for convenience
  const updateForm = handleChange;

  return {
    form: values,
    values,
    errors,
    isSubmitting,
    handleChange,
    updateForm,
    handleSubmit,
    resetForm,
    setFieldValue,
    setErrors,
  };
}
