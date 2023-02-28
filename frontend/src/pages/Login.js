import { useState } from "react";

async function loginUser(data) {
  let response = await fetch("/api/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  let result = await response.json();
  if ("token" in result) {
    return result
  }
  return null;
}

const Login = ({ setToken }) => {
  const [username, setUsername] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();

    const token = await loginUser({
      username,
      password,
    });

    if (token !== null && token !== undefined) {
      setToken(token["token"]);
      sessionStorage.setItem('token', token["token"]);
    }
  };

  return (
    <div className="form-wrapper">
        <form className="form login-form" onSubmit={handleSubmit}>
            <div className="form-element">
                <label htmlFor="username">Username</label>
                <input placeholder="Your username" onChange={e => setUsername(e.target.value)} />
            </div>
            <div className="form-element">
                <label htmlFor="password">Password</label>
                <input type="password" placeholder="●●●●●●●●" onChange={e => setPassword(e.target.value)} />
            </div>
            <div className="form-element">
                <button>Login</button>
            </div>
        </form>
    </div>
  );
};

export default Login;