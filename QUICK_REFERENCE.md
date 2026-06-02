# 🚀 Quick Reference - InvenTrack

## 🎯 Start Here (Choose One)

### Docker (Recommended)
```bash
docker-compose up --build
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Local Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

### Local Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:5173
```

---

## 📍 What's Where

| What | Where |
|------|-------|
| Frontend Pages | `frontend/src/pages/` |
| Backend Routes | `backend/app/routers/` |
| Database Models | `backend/app/models/` |
| API Schemas | `backend/app/schemas/` |
| Styles | `frontend/src/styles/` |
| Components | `frontend/src/components/` |
| Custom Hooks | `frontend/src/hooks/` |

---

## 🔗 Key URLs

| Purpose | URL |
|---------|-----|
| Web App | http://localhost:3000 |
| API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |
| DB Check | http://localhost:8000/health/db |

---

## 📦 Technologies

- **Backend**: Python 3.11, FastAPI, SQLAlchemy
- **Frontend**: React 18, Vite, React Router
- **Database**: PostgreSQL 15
- **Docker**: Multi-stage builds, Nginx

---

## 🎨 Design

- **Theme**: Dark with glassmorphism
- **Colors**: Indigo, Emerald, Amber, Red
- **Font**: Inter
- **Responsive**: Mobile, Tablet, Desktop

---

## 📊 Features

| Feature | Status |
|---------|--------|
| Dashboard | ✅ Complete |
| Products | ✅ Complete |
| Customers | ✅ Complete |
| Orders | ✅ Complete |
| Stock Management | ✅ Complete |
| API Docs | ✅ Complete |

---

## 🔑 Environment Variables

```bash
# Root .env
POSTGRES_PASSWORD=postgres_secure_password_123
DEBUG=true
VITE_API_BASE_URL=http://localhost:8000
```

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild without cache
docker-compose up --build --no-cache
```

---

## 🧪 API Testing

```bash
# Get products
curl http://localhost:8000/api/v1/products

# Create product
curl -X POST http://localhost:8000/api/v1/products \
  -H "Content-Type: application/json" \
  -d '{"sku":"TEST001","name":"Test","price":9.99,"quantity_in_stock":10}'

# Dashboard stats
curl http://localhost:8000/api/v1/dashboard/stats

# Or use Swagger: http://localhost:8000/docs
```

---

## 📁 Project Structure

```
inventoryAndOrderManagement/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/       # ORM models
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Validation
│   │   └── crud/         # Database ops
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── pages/        # Page components
│   │   ├── components/   # Reusable components
│   │   └── hooks/        # Custom hooks
│   └── package.json
├── docker-compose.yml    # Infrastructure
└── README.md            # Documentation
```

---

## 🚨 Troubleshooting

### Port in use?
```bash
# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :3000
kill -9 <PID>
```

### Database connection error?
```bash
# Check if database is healthy
docker-compose logs db

# Restart database
docker-compose restart db
```

### Frontend blank page?
- Check browser console (F12)
- Verify VITE_API_BASE_URL in .env
- Clear cache and reload

### API returning 500?
```bash
# Check backend logs
docker-compose logs api

# Verify migrations ran
docker-compose exec api alembic upgrade head
```

---

## 📱 Page Breakdown

### Dashboard
- Statistics cards (products, customers, orders, revenue)
- Low-stock alerts
- Recent orders list

### Products
- Add new product form
- Products table with SKU, name, price, stock
- Delete button
- Stock level badge

### Customers
- Add customer form
- Customers table with name, email, phone, city
- Delete button

### Orders
- Create multi-item order form
- Customer selection
- Product & quantity selection
- Order history table

---

## 🔌 API Endpoints Quick List

```
GET    /health
GET    /health/db
GET    /api/v1/products
POST   /api/v1/products
GET    /api/v1/products/{id}
PUT    /api/v1/products/{id}
DELETE /api/v1/products/{id}
GET    /api/v1/products/low-stock/
GET    /api/v1/customers
POST   /api/v1/customers
GET    /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
GET    /api/v1/orders
POST   /api/v1/orders
GET    /api/v1/orders/{id}
DELETE /api/v1/orders/{id}
GET    /api/v1/dashboard/stats
```

---

## 💡 Tips

1. **Use Swagger UI** at `/docs` for interactive API testing
2. **Check logs** when debugging: `docker-compose logs -f [service]`
3. **Use .env.example** as template, don't commit actual .env
4. **Database migrations** run automatically on startup
5. **Hot reload** works in dev mode (both frontend and backend)
6. **CORS errors?** Check ALLOWED_ORIGINS in .env
7. **Stock validation** happens on order creation
8. **Stock restoration** happens on order deletion

---

## 🎯 First Test

1. Start: `docker-compose up --build`
2. Open: http://localhost:3000
3. Create a product
4. Create a customer
5. Create an order with that product
6. View dashboard statistics
7. Check API docs at http://localhost:8000/docs

---

## 📚 Full Docs

- **Setup**: See `IMPLEMENTATION_GUIDE.md`
- **Status**: See `COMPLETION_SUMMARY.md`
- **Details**: See `README.md`

---

*Quick Reference v1.0 - June 2026*

