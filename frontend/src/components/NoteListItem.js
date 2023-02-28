import { Link } from "react-router-dom";
import { useEffect } from "react";


const getTime = (note) => {
  return new Date(note.updated).toLocaleString();
}

const getTitle = (note) => {
  const title = note.body.split("\\")[0]
  if (title.length > 45) {
    return title.slice(0, 45);
  }
  return title;
}

const getContent = (note) => {
  const title = getTitle(note);
  let content = note.body.replaceAll("\n", " ");
  content = content.replaceAll(title, "");

  if (content.length > 45) {
    return content.slice(0, 45) + "..."
  }
  return content
}

const NoteListItem = ({note}) => {
  let categoryColor;
  if (note.category) {
    categoryColor = {
      backgroundColor: note.category.color,
    };
  }


  return (
    <div className="note-list-item-wrapper">
      <div className="color"
      style={note.category && categoryColor}
      title={note.category && note.category.name}></div>
      <div>
        <Link to={`/notes/${note.id}`}>
          <div className="notes-list-item">
            <h3>{getTitle(note)}</h3>
            <p>
              <span>{getTime(note)}</span>
              <span>{getContent(note)}</span>
            </p>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default NoteListItem;