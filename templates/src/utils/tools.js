export const sendAlert = (success=true, text, timeout = 2000) => {

    const color = success ? '#1bb301' : '#ff355e';
    let alert = document.getElementsByClassName("alert-popup")[0];

    alert.innerHTML = text
    alert.style.backgroundColor = color
    alert.style.opacity = 1;

    setTimeout(function () {
        alert.style.opacity = 0;
    }, timeout);
}

export function toTitleCase(str) {
  return str.replace(
    /\w\S*/g,
    function(txt) {
      return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
    }
  );
}

export const getCsrfToken = () => {
  const csrf = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
  return csrf ? csrf.pop() : '';
};