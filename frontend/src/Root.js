import { Fragment, useEffect, useState} from "react";


import { useAuth0 } from "@auth0/auth0-react";

import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';

import Header from "./Header";

function Profile(){
    const { user, isAuthenticated, isLoading, error, getAccessTokenSilently } = useAuth0();
    const [userMetadata, setUserMetadata] = useState(null);

    useEffect(() => {
        const getUserMetadata = async () => {
            const domain = "dev-40laa62kpdtgjqtl.us.auth0.com"
      
            try {
                const accessToken = await getAccessTokenSilently({
                    authorizationParams: {
                        audience: `https://${domain}/api/v2/`, 
                        scope: "openid profile email read:current_user"
                    }
                });
                const userDetailsByIdUrl = `https://${domain}/api/v2/users/${user.sub}`;
        
                const metadataResponse = await fetch(userDetailsByIdUrl, {
                    headers: {
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
        
                const { user_metadata } = await metadataResponse.json();
        
                setUserMetadata(user_metadata);
            } catch (e) {
                console.log(e.message);
            }
        };

        function waitFor(conditionFunction) {

            const poll = resolve => {
              if(conditionFunction()) resolve();
              else setTimeout(_ => poll(resolve), 400);
            }
          
            return new Promise(poll);
        }

        waitFor( () => !isLoading)
        .then(getUserMetadata)

      }, [getAccessTokenSilently, user?.sub]
    );

    if (isLoading) {
        return <div>Loading ...</div>;
    }
    if (error) {
        return <div>Oops... {error.message}</div>;
    }
    return ( isAuthenticated && (
            <div>
                <img src={user.picture} alt={user.name} />
                <h2>{user.given_name}</h2>
                <p>{user.email}</p>
                <h3>User Metadata</h3>
                {userMetadata ? (
                <pre>{JSON.stringify(userMetadata, null, 2)}</pre>
                ) : (
                "No user metadata defined"
                )}
            </div>
        )
    );
};

function Root() {

    return (
        <Fragment>
            <Header></Header>
            <Toolbar />
            <Container>
                <Profile></Profile>
            </Container>
        </Fragment>
    );
}

export default Root;