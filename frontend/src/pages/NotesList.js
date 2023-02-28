import { useState, useEffect } from "react";
import NoteListItem from "../components/NoteListItem";
import AddButton from "../components/AddButton";
import { useOutletContext } from "react-router-dom";
import FilterForm from "../components/FilterForm";

const NotesList = () => {
  const [token, setToken] = useOutletContext();
  let [notes, setNotes] = useState([]);
  let [query, setQuery] = useState("");

  useEffect(() => {
    getNotes();
  }, []);

  let getNotes = async () => {
    let response = await fetch(`/api/notes/?query=${query}`, {
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${token}`,
      }
    });
    if (!response.ok) {
      sessionStorage.removeItem("token");
      setToken();
    }
    let data = await response.json();
    setNotes(data);
  };

  const handleFiltering = (query) => {
    setQuery(query);
  }

  return (
    <div className="notes">
      <div className="notes-header">
        <h2 className="notes-title">&#9782; Notes</h2>
        <p className="notes-count">{notes.length}</p>
      </div>
      <div className="filtering">
        <FilterForm getNotes={getNotes} query={query} handleFiltering={handleFiltering} />
      </div>
      <div className="notes-list">
        {notes.map((note, index) => (
          <NoteListItem note={note} key={index} />
        ))}
      </div>
      <AddButton />
    </div>
  );
};

export default NotesList;