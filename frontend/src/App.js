import './App.css';

import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import { Auth0Provider } from '@auth0/auth0-react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Root from './Root';
import Login from './Login';
import Logout from './Logout';


function App() {
  const router = createBrowserRouter([
    {path:"/", element:<Root />},
    {path:"/login", element:<Login />},
    {path:"/logout", element:<Logout />},
  ]);
  return (
    <Auth0Provider
      domain="dev-40laa62kpdtgjqtl.us.auth0.com"
      clientId="3xZlJE0SQaxTufjRC8ZMFrWZszpSQnkx"
      authorizationParams={{
        redirect_uri: window.location.origin,
        audience: "https://dev-40laa62kpdtgjqtl.us.auth0.com/api/v2/"
      }}
    >

      <RouterProvider router={router} />
    </Auth0Provider>
  );
}

export default App;
