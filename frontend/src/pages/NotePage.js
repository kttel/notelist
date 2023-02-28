import { useState, useEffect } from "react";
import { useLoaderData, useNavigate, useOutletContext } from "react-router-dom";
import { ReactComponent as ArrowLeft } from "../assets/arrow-left.svg";

const NotePage = () => {
  const [token, setToken] = useOutletContext();

  const navigate = useNavigate();
  const noteId = useLoaderData();

  const [note, setNote] = useState(null);
  const [color, setColor] = useState("#000000");
  const [category, setCategory] = useState("");

  useEffect(() => {
    getNote();
  }, []);

  const getNote = async () => {
    if (noteId === "new") return;

    const response = await fetch(`/api/notes/${noteId}`, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      },
    });
    if (!response.ok) {
      sessionStorage.removeItem("token");
      setToken();
    }
    const data = await response.json();
    setNote(data);
    if (data.category != null) {
      setColor(data.category.color);
      setCategory(data.category.name);
    }
  }

  const updateNote = async () => {
    let noteData = (({ category, ...o }) => o)(note);
    if (category) {
      noteData = {...note, category: {name: category || '', color: color}};
    }
    const response = await fetch(`/api/notes/${noteId}/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      },
      body: JSON.stringify(noteData),
    });
    console.log(response.status)
  };

  const createNote = async () => {
    let noteData = {...note};
    if (category) {
      noteData = {...note, category: {name: category || '', color: color}};
    }
    const response = await fetch(`/api/notes/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      },
      body: JSON.stringify(noteData),
    });
    console.log(response.status);
  };

  const deleteNote = async () => {
    fetch(`/api/notes/${noteId}/`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      },
    });
    navigate("/");
  };

  const handleSubmit = () => {
    if (noteId !== 'new' && note.body === "") {
      deleteNote();
    } else if (noteId !== "new") {
      updateNote();
    } else if (noteId === "new" && note && note.body !== "") {
      createNote();
    }
    navigate("/");
  }

  const handleChange = (value) => {
    setNote(note => ({...note, "body": value}));
  }

  return (
    <div className="note">
      <div className="note-header">
        <h3><ArrowLeft onClick={handleSubmit}/></h3>
        {noteId !== 'new' ? (
          <button onClick={deleteNote}>Delete</button>
        ) : ""}
      </div>
      <textarea value={note?.body} onChange={(e) => {handleChange(e.target.value)}}/>
      <div className="note-enhancement">
        <div className="color-container">
          <input type="color" value={color} onChange={e => setColor(e.target.value)} />
        </div>
        <input type="text" placeholder="category" value={category} onChange={e => setCategory(e.target.value)}/>
      </div>
    </div>
  );
};

export default NotePage;