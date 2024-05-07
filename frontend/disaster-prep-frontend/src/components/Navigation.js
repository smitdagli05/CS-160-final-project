import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navigation.css';

function Navigation() {
  const location = useLocation();

  return (
    <nav className="bottom-bar">
      <Link to="/" className={location.pathname === '/' ? 'active' : ''}>
        <div className="icon plans-icon"></div>
        <span>Plans</span>
      </Link>
      <Link to="/chat" className={location.pathname === '/chat' ? 'active' : ''}>
        <div className="icon chat-icon"></div>
        <span>Chat</span>
      </Link>
      <Link to="/profile" className={location.pathname === '/profile' ? 'active' : ''}>
        <div className="icon profile-icon"></div>
        <span>Profile</span>
      </Link>
    </nav>
  );
}

export default Navigation;