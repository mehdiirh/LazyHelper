import React from "react";
import {useRef, useState} from "react";
import {copyToClipboard, execute, initialData, login} from "./server";
import {sendAlert, toTitleCase} from "./tools";
import {
    IconButton, HomeButton,
    FlexColumn, FlexRow,
    IconInput, Button, SlideDown,
} from "./components";
import {
    faArrowRight,
    faArrowRightToFile, faCaretDown,
    faCog,
    faCopy,
    faMoon,
    faPowerOff,
    faRotateBack,
    faStarOfLife,
    faUser, faUserCheck,
    faUserLock,
} from "@fortawesome/free-solid-svg-icons";


export function MainPage(props) {

    const {customButtons, links, ...rest} = props;

    const copyToClipboardInput = useRef();
    const [isSlideDownOpen, setIsSlideDownOpen] = useState(false);

    const handleButtonClick = (disableButtons) => {
        const buttons = document.querySelectorAll('button, input');
        for (let i=0; i < buttons.length; i++) {
            buttons[i].disabled = disableButtons;
        }
    }

    const handleCustomButtonClick = (e) => {
        handleButtonClick(true);
        execute(e.currentTarget.value).then(response => {
            if (response["meta"].status === 'ok') {
                sendAlert(true, 'Success')
            } else {
                let message = response["meta"].message ? response["meta"].message : 'Error: ' + response["meta"].code
                sendAlert(false, message)
            }
            handleButtonClick(false)
        })
    }

    const copyToClipboardClickHandler = (e) => {
        handleButtonClick(true);
        const content = copyToClipboardInput.current.value;

        copyToClipboard(content).then((res) => {

            if (res['meta']['status'] === 'ok') {
                sendAlert(true, 'Copied to clipboard');
            } else {
                let message = res["meta"].message ? res["meta"].message : 'Error: ' + res["meta"].code
                sendAlert(false, message)
            }
            handleButtonClick(false);
        });
    }

    return (
        <>
            <SlideDown open={isSlideDownOpen} setOpen={setIsSlideDownOpen} >
                {customButtons && customButtons.map((button) => {
                    return (
                        <Button key={button.id} onClick={handleCustomButtonClick}
                                value={button.short_code} className={'btn'}
                                style={{backgroundColor: button.color}}
                        >
                            {button.title}
                        </Button>
                    )
                })}

                <a href={links && links["add_buttons"]}>
                    <Button className={'btn btn-light'}>
                    + Add custom button
                    </Button>
                </a>
            </SlideDown>

            <FlexColumn>
                <FlexRow>
                    <HomeButton icon={faPowerOff} value={'shutdown'} clickHandler={handleButtonClick}>
                        Shutdown
                    </HomeButton>

                    <HomeButton icon={faRotateBack} value={'reboot'} clickHandler={handleButtonClick}>
                        Reboot
                    </HomeButton>
                </FlexRow>

                <FlexRow>
                    <HomeButton icon={faMoon} value={'sleep'} clickHandler={handleButtonClick}>
                        Sleep
                    </HomeButton>

                    <HomeButton icon={faUserLock} value={'lock'} clickHandler={handleButtonClick}>
                        Lock
                    </HomeButton>
                </FlexRow>
            </FlexColumn>

            <div className={'vertical-center'}>
                <IconInput placeholder={"copy to clipboard"}
                           reference={copyToClipboardInput}
                           icon={faCopy}
                           btnIcon={faArrowRightToFile}
                           btnClickHandler={copyToClipboardClickHandler}
                />
            </div>
        </>
    )
}

export function Profile(props) {

    const usernameInput = useRef();
    const passwordInput = useRef();
    const {
        loginRequired, isLoggedIn, setIsLoggedIn,
        user, setUser,
        links, setLinks,
        setIsinHomePage,
        ...rest} = props;

    const [loadingOnLogin, setLoadingOnLogin] = useState(false);

    const loginClickHandler = (e) => {
        if (!e.currentTarget.disabled) {
            setLoadingOnLogin(true)
            document.querySelectorAll('button, input').forEach((e) => e.disabled = true);

            login(usernameInput.current.value, passwordInput.current.value).then((res) => {
                if (res["meta"]["status"] === "ok") {

                    initialData().then((res) => {
                        setUser(res["data"]["user"]);
                        setLinks(res["data"]["links"]);
                    })

                    setIsinHomePage(true);
                    setIsLoggedIn(true);
                    sendAlert(true, 'You are logged in');
                } else {
                    sendAlert(false, 'Invalid username or password', 2000);
                }
            }).catch((err) => {
                sendAlert(false, 'Error: ' + err, 2000);
            })

            setLoadingOnLogin(false)
            document.querySelectorAll('button, input').forEach((e) => e.disabled = false);
        }

    }

    const profileButtonClickHandler = (e) => {
        window.location = e.currentTarget.value;
    }

    if (!isLoggedIn) {
        return (
            <>
                <FlexColumn>
                    <FlexRow>
                        <IconInput icon={faUser} reference={usernameInput} placeholder={"username"} />
                    </FlexRow>
                    <FlexRow>
                        <IconInput type={'password'} icon={faStarOfLife} reference={passwordInput} placeholder={"username"}/>
                    </FlexRow>

                    <div className={"flex-row justify-content-end me-3"}>
                        <IconButton className={'btn btn-lazy w-50'} loading={loadingOnLogin} icon={faArrowRight} clickHandler={loginClickHandler} >
                            <span> Login</span>
                        </IconButton>
                    </div>
                </FlexColumn>
            </>
        );
    } else {
        return (
            <>
                <FlexColumn>
                    <FlexRow>
                        <h3>Hello, <strong>{toTitleCase(
                            user['user']
                            // 'admin'
                        )}</strong> ! </h3>
                    </FlexRow>
                </FlexColumn>

                <FlexColumn>
                    <FlexRow>
                        <IconButton icon={faUserCheck} className={'home-button'}
                                    value={links['panel']} clickHandler={profileButtonClickHandler}>
                            Panel
                        </IconButton>
                        <IconButton icon={faCog} className={'home-button'}
                                    value={links['settings']} clickHandler={profileButtonClickHandler} >
                            Settings
                        </IconButton>
                    </FlexRow>
                </FlexColumn>

                <FlexRow>
                    <Button className={'btn'} value={'/logout/'} onClick={profileButtonClickHandler}>
                        <span> Logout</span>
                    </Button>
                </FlexRow>
            </>
        )
    }
}
