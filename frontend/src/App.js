import './App.css';
import Header from './components/Header';
import { Outlet, useNavigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login';


function App() {
  const getToken = () => {
    const tokenString = sessionStorage.getItem('token');
    return tokenString;
  };

  const [token, setToken] = useState(getToken());

  const handleThemeChange = (newTheme) => {
    console.log(newTheme);
    sessionStorage.setItem("theme", newTheme);
    setTheme(newTheme);
  }

  const getTheme = () => {
    const savedTheme = sessionStorage.getItem("theme") || "dark";
    return savedTheme;
  }

  const context = [token, setToken, handleThemeChange];
  const [theme, setTheme] = useState(getTheme());

  return (
    <div className={`container ${theme}`}>
      <div className="app">
        <Header token={token} setToken={setToken} />
        {token ?
          <Outlet context={context} /> :
          <Login setToken={setToken} />}
      </div>
    </div>
  );
}

export default App;
