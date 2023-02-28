import { useNavigate, useLocation } from "react-router-dom";
import {ReactComponent as ProfileIcon} from "../assets/house-solid.svg";
import {ReactComponent as ArrowLeft} from "../assets/arrow-left.svg";

const Header = ({token, setToken}) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async() => {
    await fetch("/api/logout/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      }
    });
    sessionStorage.removeItem("token");
    setToken();
  }

  const handleRedirect = () => {
    if (location.pathname === "/profile") {
      navigate("/");
    } else {
      navigate("/profile");
    }
  }

  return (
    <div className="app-header">
        <h1>Note List</h1>
        {token && (
          <div className="header-right">
            <button onClick={handleRedirect}>
              {location.pathname === "/profile" ? <ArrowLeft /> : <ProfileIcon />}
            </button>
            <button onClick={handleLogout} className="manage-button">
              Logout
            </button>
          </div>
        )}
    </div>
  );
};

export default Header;