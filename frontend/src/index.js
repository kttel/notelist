import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import NotesList from './pages/NotesList';
import NotePage from './pages/NotePage';
import {
  createBrowserRouter,
  RouterProvider,
} from 'react-router-dom';
import Login from './pages/Login';
import Profile from './pages/Profile';

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "",
        element: <NotesList />,
      },
      {
        path: "login",
        element: <Login />
      },
      {
        path: "profile",
        element: <Profile />
      },
      {
        path: "notes/:id",
        element: <NotePage />,
        loader: ({ params }) => {
          return params.id;
        },
      },
    ]
  },
]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
