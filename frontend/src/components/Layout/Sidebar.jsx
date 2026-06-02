import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const navItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/products', label: 'Products', icon: '📦' },
  { path: '/customers', label: 'Customers', icon: '👥' },
  { path: '/orders', label: 'Orders', icon: '🛒' },
];

export default function Sidebar({ isOpen, onClose }) {
  return (
    <aside className={`sidebar ${isOpen ? 'sidebar-open' : ''}`}>
      <div className="sidebar-brand">
        <span className="sidebar-logo">◆</span>
        <h1 className="sidebar-title">InvenTrack</h1>
      </div>

      <nav className="sidebar-nav">
        <span className="sidebar-section-title">Main Menu</span>
        <ul className="sidebar-nav-list">
          {navItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                end={item.path === '/'}
                className={({ isActive }) =>
                  `sidebar-nav-item ${isActive ? 'active' : ''}`
                }
                onClick={onClose}
              >
                <span className="sidebar-nav-icon">{item.icon}</span>
                <span className="sidebar-nav-label">{item.label}</span>
                <span className="sidebar-nav-active-bar" />
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="sidebar-footer">
        <div className="sidebar-footer-badge">v1.0.0</div>
      </div>
    </aside>
  );
}
