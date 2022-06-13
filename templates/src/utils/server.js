import axios from 'axios';
import {getCsrfToken} from "./tools";

export const ajax = (url, method, data) => {
    let csrf = getCsrfToken()

    const headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": csrf,
        }

    return axios({
        url: url,
        method: 'post',
        data: data,
        headers: headers
    })
}


// function to execute commands
export const execute = (command) => {
    return ajax('/ajax/execute/', 'POST', {command: command}).then(res => (res.data))
}

export const copyToClipboard = (content) => {
    return ajax('/ajax/copy/', 'POST', {content: content}).then(res => (res.data))
}

export function login(username, password) {
    return ajax('/ajax/login/', 'POST', {username: username, password: password}).then(res => (res.data))
}

export function initialData() {
    return ajax('/ajax/initial/', 'POST').then(res => (res.data))
}
