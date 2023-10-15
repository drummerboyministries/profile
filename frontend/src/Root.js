import { Fragment, useEffect, useState} from "react";


import { useAuth0 } from "@auth0/auth0-react";

import Container from '@mui/material/Container';
import Toolbar from '@mui/material/Toolbar';

import Header from "./Header";

function Profile(){
    const { user, isAuthenticated, isLoading, error } = useAuth0();

    if (isLoading) {
        return <div>Loading ...</div>;
    }
    if (error) {
        return <div>Oops... {error.message}</div>;
    }
    return ( isAuthenticated && (
            <div>
                asdfasdf {Object.keys(user)}
                
                <img src={user.picture} alt={user.name} />
                <h2>{user.given_name}</h2>
                <p>{user.email}</p>
                <h3>User Metadata</h3>
                {/* {userMetadata ? (
                <pre>{JSON.stringify(userMetadata, null, 2)}</pre>
                ) : (
                "No user metadata defined"
                )} */}
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