import React, {useRef, useState} from "react";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import {
    faCaretDown,
    faCircle,
    faHome,
    faSpinner,
    faUser
} from "@fortawesome/free-solid-svg-icons";
import {execute} from "./server";
import {sendAlert} from "./tools";

export function Vector(props) {

    let {src, alt, className, refrence, ...rest} = props;

    className = className ? 'svg ' + className : 'svg';

    return (
        <img src={require(`../static/vectors/${src}`)} alt={alt} className={className} ref={refrence} {...rest} />
    );
}

export function Container(props) {

    const {homePageButtonClick, profileButtonClick, isInHomePage, ...rest } = props;

    return (
            <div className={'container'} {...rest}>
                <div className="alert-popup">Alert</div>

                <div className={'logo'}>
                    <Vector src={'logo.svg'} alt={'logo'} width={'50%'}/>
                </div>

                {props.children}

                <Footer>
                    <FooterItem icon={faHome}
                                active={isInHomePage}
                                onClick={homePageButtonClick}
                    />
                    <FooterItem icon={faUser}
                                active={!isInHomePage}
                                onClick={profileButtonClick}
                    />
                </Footer>
            </div>
    );
}

export function FlexRow(props) {
    return (
        <div className={'flex-row'} {...props}>
            {props.children}
        </div>
    );
}

export function FlexColumn(props) {
    return (
        <div className={'flex-column'} {...props}>
            {props.children}
        </div>
    );
}

export function Row(prop) {
    return (
        <div className={'row'}>
            {prop.children}
        </div>
    );
}

export const Button = React.forwardRef((props, ref) => {

    let {reference, ...rest} = props;

    return (
        <button ref={ref} {...rest} />
    );

})

export function IconButton(props) {

    let { icon, iconSize, loading, children, reference, clickHandler, ...rest } = props;

    return (
        <>
            <Button onClick={clickHandler} ref={reference} {...rest} >
                {
                    !loading ?
                        <FontAwesomeIcon icon={icon} />
                        : <FontAwesomeIcon icon={faSpinner} spin />
                }
                {children}
            </Button>
        </>
    )
}

export function SlideDown(props) {
    const {
        children,
        open, setOpen,
        clickHandler,
        reference,
        ...rest } = props;


    const onSlideDownClick = () => {
        setOpen(!open);
    }

    return (
        <div className={`slide-down ${open ? 'open' : 'close'}`} ref={reference} onClick={clickHandler || onSlideDownClick}>
            <div className={'slide-down-wrapper'}>

                <div className={'slide-down-content'}>
                    {children}
                </div>

                <div className={'slide-down-icon'} >
                    <FontAwesomeIcon icon={faCaretDown} />
                </div>
            </div>



        </div>
    );
}

export function HomeButton(props) {

    let { className, clickHandler, ...rest } = props;

    className = className ? 'home-button ' + className : 'home-button';

    const button = useRef();
    const [loading, setLoading] = useState(false);

    const onClick = e => {
        clickHandler(true);
        setLoading(true);
        execute(button.current.value).then(response => {
            if (response["meta"].status === 'ok') {
                sendAlert(true, 'Success')
            } else {
                let message = response["meta"].message ? response["meta"].message : 'Error: ' + response["meta"].code
                sendAlert(false, message)
            }

            setLoading(false);
            clickHandler(false)
        })
    }

    return (
        <IconButton loading={loading} reference={button} className={className} clickHandler={onClick} {...rest} />
    )
}

export function IconInput(props) {

    let {
        icon, iconColor, iconClickHandler,
        btnIcon, btnClickHandler,
        reference, inputClickHandler,
        ...rest
    } = props;

    if (icon) {
        icon = <FontAwesomeIcon icon={icon} color={iconColor || 'gray'} onClick={iconClickHandler} />
    }

    return (
        <div className={'icon-input'}>
            <TextInput onClick={inputClickHandler} reference={reference} {...rest} />
            {icon}
            {btnIcon &&
                <Button onClick={btnClickHandler} >
                    <FontAwesomeIcon icon={btnIcon} />
                </Button>
            }

        </div>
    );
}

export function TextInput(props) {

    const { reference, ...rest } = props;

    return (
        <input type={'text'} ref={reference} {...rest} />
    );
}


export function Footer(props) {
    return (
        <div className={'footer'}>
            {props.children}
        </div>
    );
}

export function FooterItem(props) {

    const {icon, active, onClick, color, ...rest} = props;

    return (
        <div className={'footer-item'}>
            <button onClick={onClick}>
                <FontAwesomeIcon
                    className={'footer-icon'}
                    icon={icon}
                    color={active ? color || 'black' : 'gray'}
                    {...rest}
                />
                {props.active &&
                    <FontAwesomeIcon icon={faCircle} style={{width: '7px', height: '7px'} }/>
                }
            </button>
        </div>
    );
}
