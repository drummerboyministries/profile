import './App.css';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Root from './Root';
import Login from './Login';


function App() {
  const router = createBrowserRouter([
    {path:"/", element:<Root />},
    {path:"/login", element:<Login />},
  ]);
  return (
    <div className="App">
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
