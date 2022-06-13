import React, {useState, useEffect, useRef} from 'react';
import ReactDOM from 'react-dom/client';
import './static/bootstrap/bootstrap.min.css';
import './static/styles/styles.css';
import {Container, FlexColumn} from "./utils/components";
import {MainPage, Profile} from "./utils/pages";
import {sendAlert} from "./utils/tools";
import {initialData} from "./utils/server";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faSpinner} from "@fortawesome/free-solid-svg-icons";


const root = ReactDOM.createRoot(document.getElementById('root'));

function App(props) {

    const [isInHomePage, setIsInHomePage] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [user, setUser] = useState();
    const [links, setLinks] = useState();
    const [customButtons, setCustomButtons] = useState();
    let loginRequired = useRef(true);

    useEffect(() => {
        initialData().then(response => {
            setLinks(response["data"]["links"]);

            if (response["data"]["settings"]["login-required"] === false) {
                loginRequired.current = false;
                setCustomButtons(response["data"]["custom_buttons"]);
                setIsInHomePage(true);
            }

            if (response["data"]["user"]["is_admin"] === true) {
                setUser(response["data"]['user']);
                setCustomButtons(response["data"]["custom_buttons"]);
                setIsInHomePage(true);
                setIsLoggedIn(true);
            } else if (loginRequired.current === true) {
                sendAlert(false, 'Login to continue', 2000);
                setIsInHomePage(false);
            }
        })
    }, []);

    const onProfileButtonClick = (e) => {
        if (!e.currentTarget.disabled)
            setIsInHomePage(false)
    }

    const onHomePageButtonClick = (e) => {
        if (!e.currentTarget.disabled)
            if (!isLoggedIn && loginRequired.current) {
                sendAlert(false, 'Login to use this section', 2000);
            } else {
                setIsInHomePage(true);
            }
    }

    const Render = () => {
        if (isInHomePage === null) {
            return <FlexColumn><FontAwesomeIcon icon={faSpinner} fontSize={'8rem'} spin /></FlexColumn>
        } else if (isInHomePage === true) {
            return <MainPage customButtons={customButtons} links={links} />
        } else if (isInHomePage === false) {
            return <Profile
                user={user} setUser={setUser}
                links={links} setLinks={setLinks}
                loginRequired={loginRequired} isLoggedIn={isLoggedIn} setIsLoggedIn={setIsLoggedIn}
                setIsinHomePage={setIsInHomePage}
            />
        }
    }
    return (
        <div className={'center'}>
            <Container
                isInHomePage={isInHomePage}
                homePageButtonClick={onHomePageButtonClick}
                profileButtonClick={onProfileButtonClick}
            >

            {Render()}
            </Container>
        </div>

    )
}

root.render(<App />);

