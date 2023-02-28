import { useState, useEffect } from "react";
import { useOutletContext } from "react-router-dom";

const Profile = () => {
  const [token, setToken, handleThemeChange] = useOutletContext();
  const [profile, setProfile] = useState([]);

  useEffect(() => {
    getProfile();
  }, []);

  let getProfile = async () => {
    let response = await fetch(`/api/me/`, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      }
    });
    if (!response.ok) {
      sessionStorage.removeItem("token");
      setToken();
    }
    const data = await response.json();
    setProfile(data);
  };
  console.log(profile)

  return (
    <div className="profile-container">
      <div className="profile-header">
        Hello, {profile.username}!
      </div>
      <div className="theme-choose">
        <button className="theme-button" id="theme1" onClick={e => handleThemeChange("")}></button>
        <button className="theme-button" id="theme2" onClick={e => handleThemeChange("dark")}></button>
        <button className="theme-button" id="theme3" onClick={e => handleThemeChange("pink")}></button>
      </div>
      <div className="profile-information">
        You have {profile.total_notes} notes at the moment!
      </div>
    </div>
  );
};

export default Profile;