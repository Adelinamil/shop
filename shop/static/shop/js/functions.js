let delayTimer;
const checkUser = async (columnName, columnValue) => {
    let form = new FormData();
    form.append('column_name', columnName);
    form.append('column_value', columnValue);
    const response = await fetch('/users/check_user/', {
        method: 'POST',
        body: form,
        credentials: 'same-origin',
        headers: {"X-CSRFToken": Cookies.get('csrftoken')},
    });
    return (await response.json())['is_taken'];
};

const addError = (id, message) => {
    const alertsContainer = document.getElementById("alerts");
    if (document.getElementById("error_" + id)) return;
    const newAlert = document.createElement("div");
    newAlert.id = "error_" + id;
    newAlert.className = "alert alert-danger w-75 m-auto mt-1";
    newAlert.textContent = message;
    alertsContainer.appendChild(newAlert);
};

const removeError = (id) => {
    const alertToRemove = document.getElementById("error_" + id);
    if (!alertToRemove) return;
    try {
        document.getElementById("alerts").removeChild(alertToRemove);
    } catch (TypeError) {

    }
};

const validateInputWithRequest = async (elementId, columnName, errorMessage) => {
    let element = document.getElementById(elementId);
    if (element.value !== "") {
        delayTimer = setTimeout(async () => {
            const isUsernameExists = await checkUser(columnName, element.value);
            if (isUsernameExists) {
                element.classList.remove("is-valid");
                element.classList.add("is-invalid");
                element.setCustomValidity(errorMessage);
                addError(elementId, errorMessage);
            } else {
                element.classList.remove("is-invalid");
                element.setCustomValidity("");
                removeError(elementId);
            }
        }, 500);
    } else {
        element.classList.remove("is-invalid");
        element.setCustomValidity("");
        removeError(elementId);
    }
};

const validatePassword = () => {
    const passwordInput = document.getElementById('id_password1');

    if (passwordInput.value !== "") {
        const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
        if (!passwordRegex.test(passwordInput.value)) {
            passwordInput.classList.remove("is-valid");
            passwordInput.classList.add("is-invalid");
            passwordInput.setCustomValidity("Неверный формат");
            addError("id_password1", "Пароль не соответствует формату");
        } else {
            passwordInput.classList.remove("is-invalid");
            passwordInput.setCustomValidity("");
            removeError("id_password1");
        }
    } else {
        passwordInput.classList.remove("is-invalid");
        passwordInput.setCustomValidity("");
        removeError("id_password1");
    }

    const confirmPasswordInput = document.getElementById('id_password2');
    if (confirmPasswordInput.value !== "" && passwordInput.value !== passwordInput && passwordInput.value !== confirmPasswordInput.value) {
        confirmPasswordInput.classList.remove("is-valid");
        confirmPasswordInput.classList.add("is-invalid");
        confirmPasswordInput.setCustomValidity("Пароли не соответствуют");
        addError("id_password2", "Пароли не соответствуют");
    } else {
        confirmPasswordInput.classList.remove("is-invalid");
        confirmPasswordInput.setCustomValidity("");
        removeError("id_password2");
    }
}

const onInputUser = async () => {
    if (delayTimer) clearTimeout(delayTimer);
    await validateInputWithRequest("id_username", "username", "Имя пользователя должно быть уникальным.");
    await validateInputWithRequest("id_email", "email", "Почта должна быть уникальной.");
    delayTimer = setTimeout(() => validatePassword(), 750);
};

const sendRequest = async (url, form) => {
    return await fetch(url, {
        method: 'POST',
        body: form,
        credentials: 'same-origin',
        headers: {"X-CSRFToken": Cookies.get('csrftoken')},
    });
};

const onAddToCart = async (productId) => {
    const form = new FormData();
    const p_data_response = await sendRequest(`/cart/add/${productId}/`, form);
    if (!p_data_response.ok) {
        addError('cart_item_add', 'Недостаточно единиц на складе')
    } else {
        window.location.href = p_data_response.url;
    }
};

const removeFromCart = async (productId) => {
    const form = new FormData();
    const p_data_response = await sendRequest(`/cart/remove/${productId}/`, form);
    if (!p_data_response.ok) {
        addError('cart_item_remove', 'Произошла ошибка при удалении из корзины')
    } else {
        window.location.href = p_data_response.url;
    }
};


const onConfirmPasswordOrder = async () => {
    if (delayTimer) clearTimeout(delayTimer);
    const passwordInput = document.getElementById('id_password');
    if (passwordInput.value !== "") {
        delayTimer = setTimeout(async () => {
            let form = new FormData();
            form.append('password', passwordInput.value);
            const response = await fetch('/users/confirm_password/', {
                method: 'POST',
                body: form,
                credentials: 'same-origin',
                headers: {"X-CSRFToken": Cookies.get('csrftoken')},
            });
            let isCorrect = (await response.json())['is_correct'];
            if (!isCorrect) {
                passwordInput.classList.remove("is-valid");
                passwordInput.classList.add("is-invalid");
                passwordInput.setCustomValidity("Неверный пароль");
                addError("id_password", "Неверный пароль");
            } else {
                passwordInput.classList.remove("is-invalid");
                passwordInput.setCustomValidity("");
                removeError('id_password');
            }
        }, 750);
    } else {
        passwordInput.classList.remove("is-invalid");
        passwordInput.setCustomValidity("");
        removeError('id_password');
    }
};
