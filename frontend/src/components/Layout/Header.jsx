import { useLocation } from 'react-router-dom';
import './Header.css';

const pageTitles = {
  '/': 'Dashboard',
  '/products': 'Products',
  '/customers': 'Customers',
  '/orders': 'Orders',
};

export default function Header({ onMenuToggle }) {
  const location = useLocation();
  const title = pageTitles[location.pathname] || 'Page';

  return (
    <header className="header">
      <div className="header-left">
        <button
          className="header-menu-btn"
          onClick={onMenuToggle}
          aria-label="Toggle navigation"
        >
          <span className="header-menu-icon">
            <span />
            <span />
            <span />
          </span>
        </button>
        <h2 className="header-title">{title}</h2>
      </div>

      <div className="header-right">
        <button className="header-icon-btn" aria-label="Notifications">
          <span className="header-bell">🔔</span>
          <span className="header-notification-dot" />
        </button>
        <div className="header-avatar">
          <span>A</span>
        </div>
      </div>
    </header>
  );
}
