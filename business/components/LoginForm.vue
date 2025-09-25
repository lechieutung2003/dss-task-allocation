<template>
    <div class="lg:py-10 py-6 lg:px-12 px-6 min-w-280 sm:w-full h-full bg-white rounded-lg drop-shadow-md">
        <main class="w-full">
            <div class="w-full md:max-w-[550px] max-w-[450px] mx-auto">
                <slot />
                <span v-if="store.isFirstLogin" class="mb-6">{{ $t('congrate_finishing_account') }}</span>
                <p v-if="error" class="flex self-center justify-center text-red-800 mb-2">{{ error }}</p>
                
                <form class="form" @submit.prevent="login()">
                    <!-- Login Header -->
                    <div class="form-header">
                        <h1 class="form-title">{{ $t('start_using') }}</h1>
                        <p class="form-subtitle">{{ $t('Login_to_start_using') }}</p>
                    </div>
                    <!-- Email Field -->
                    <div class="flex-column">
                        <label>{{ $t('Email') }}</label>
                    </div>
                    <div class="inputForm" :class="{ 'error-border': emailError }">
                        <svg height="20" viewBox="0 0 32 32" width="20" xmlns="http://www.w3.org/2000/svg">
                            <g id="Layer_3" data-name="Layer 3">
                                <path d="m30.853 13.87a15 15 0 0 0 -29.729 4.082 15.1 15.1 0 0 0 12.876 12.918 15.6 15.6 0 0 0 2.016.13 14.85 14.85 0 0 0 7.715-2.145 1 1 0 1 0 -1.031-1.711 13.007 13.007 0 1 1 5.458-6.529 2.149 2.149 0 0 1 -4.158-.759v-10.856a1 1 0 0 0 -2 0v1.726a8 8 0 1 0 .2 10.325 4.135 4.135 0 0 0 7.83.274 15.2 15.2 0 0 0 .823-7.455zm-14.853 8.13a6 6 0 1 1 6-6 6.006 6.006 0 0 1 -6 6z"></path>
                            </g>
                        </svg>
                        <input 
                            v-model="formData.email" 
                            type="email" 
                            class="input" 
                            :placeholder="$t('Email')"
                            @blur="validateEmail"
                        >
                    </div>
                    <span v-if="emailError" class="error-text">{{ emailError }}</span>

                    <!-- Password Field -->
                    <div class="flex-column">
                        <label>{{ t('password_place_holder') }}</label>
                    </div>
                    <div class="inputForm" :class="{ 'error-border': passwordError }">
                        <svg height="20" viewBox="-64 0 512 512" width="20" xmlns="http://www.w3.org/2000/svg">
                            <path d="m336 512h-288c-26.453125 0-48-21.523438-48-48v-224c0-26.476562 21.546875-48 48-48h288c26.453125 0 48 21.523438 48 48v224c0 26.476562-21.546875 48-48 48zm-288-288c-8.8125 0-16 7.167969-16 16v224c0 8.832031 7.1875 16 16 16h288c8.8125 0 16-7.167969 16-16v-224c0-8.832031-7.1875-16-16-16zm0 0"></path>
                            <path d="m304 224c-8.832031 0-16-7.167969-16-16v-80c0-52.929688-43.070312-96-96-96s-96 43.070312-96 96v80c0 8.832031-7.167969 16-16 16s-16-7.167969-16-16v-80c0-70.59375 57.40625-128 128-128s128 57.40625 128 128v80c0 8.832031-7.167969 16-16 16zm0 0"></path>
                        </svg>
                        <input 
                            v-model="formData.password" 
                            :type="showPassword ? 'text' : 'password'" 
                            class="input" 
                            :placeholder="t('password_place_holder')"
                            @blur="validatePassword"
                        >
                        <svg 
                            @click="togglePassword" 
                            class="password-toggle" 
                            viewBox="0 0 576 512" 
                            height="1em" 
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path d="M288 32c-80.8 0-145.5 36.8-192.6 80.6C48.6 156 17.3 208 2.5 243.7c-3.3 7.9-3.3 16.7 0 24.6C17.3 304 48.6 356 95.4 399.4C142.5 443.2 207.2 480 288 480s145.5-36.8 192.6-80.6c46.8-43.5 78.1-95.4 93-131.1c3.3-7.9 3.3-16.7 0-24.6c-14.9-35.7-46.2-87.7-93-131.1C433.5 68.8 368.8 32 288 32zM144 256a144 144 0 1 1 288 0 144 144 0 1 1 -288 0zm144-64c0 35.3-28.7 64-64 64c-7.1 0-13.9-1.2-20.3-3.3c-5.5-1.8-11.9 1.6-11.7 7.4c.3 6.9 1.3 13.8 3.2 20.7c13.7 51.2 66.4 81.6 117.6 67.9s81.6-66.4 67.9-117.6c-11.1-41.5-47.8-69.4-88.6-71.1c-5.8-.2-9.2 6.1-7.4 11.7c2.1 6.4 3.3 13.2 3.3 20.3z"></path>
                        </svg>
                    </div>
                    <span v-if="passwordError" class="error-text">{{ passwordError }}</span>

                    <div class="flex-row">
                        <div>
                            <input v-model="rememberMe" type="checkbox">
                            <label>Remember me</label>
                        </div>
                        <NuxtLink to="/forgot-password" class="span">
                            {{ $t('forgot_password') }}
                        </NuxtLink>
                    </div>

                    <button type="submit" class="button-submit" :disabled="isLoading">
                        <span v-if="isLoading">Signing In...</span>
                        <span v-else>{{ $t('Login') }}</span>
                    </button>

                    <p class="p">Don't have an account? 
                        <span class="span">Sign Up</span>
                    </p>
                </form>
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import OAuthService from '@/services/oauth';
import { useOauthStore } from '~/stores/oauth';
import { getErrorMessage } from '@/utils/error';

const props = defineProps({
    redirectTo: {
        type: String,
        required: false
    },
})

const { t } = useI18n();
const store = useOauthStore()

const formData = ref({
    email: null,
    password: null
})

const error = ref(null);
const isLoading = ref(false);
const showPassword = ref(false);
const rememberMe = ref(false);
const emailError = ref('');
const passwordError = ref('');

const togglePassword = () => {
    showPassword.value = !showPassword.value;
}

const validateEmail = () => {
    if (!formData.value.email) {
        emailError.value = t('validate_error_required');
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.value.email)) {
        emailError.value = t('validate_error_email_format');
    } else {
        emailError.value = '';
    }
}

const validatePassword = () => {
    if (!formData.value.password) {
        passwordError.value = t('validate_error_required');
    } else {
        passwordError.value = '';
    }
}

const validateForm = () => {
    validateEmail();
    validatePassword();
    return !emailError.value && !passwordError.value;
}

const login = async () => {
    if (!validateForm()) {
        return;
    }

    let { email: username, password } = formData.value;
    const { redirectTo } = props
    
    store.setFirstLogin(false);
    error.value = null;
    isLoading.value = true;
    
    let data = { username, password }
    
    try {
        const response = await OAuthService.login(data);
        const { access_token, refresh_token } = response;
        
        if (access_token && refresh_token) {
            store.setTokenInfo({ access_token, refresh_token });
        }
        
        try {
            const user = await OAuthService.userinfo();
            store.setUser(user);
        } catch (e) {
            error.value = getErrorMessage(e, t('an_error_occurred'));
        } finally {
            if (!!redirectTo && redirectTo.length > 0) {
                navigateTo(redirectTo);
            }
        }
    } catch (e) {
        error.value = getErrorMessage(e, t('an_error_occurred'));
    } finally {
        isLoading.value = false;
    }
}
</script>

<style scoped>
.form {
    display: flex;
    flex-direction: column;
    gap: 10px;
    background-color: #ffffff;
    padding: 30px;
    width: 450px;
    border-radius: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

::placeholder {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.form-header {
    text-align: center;
    margin-bottom: 30px;
}

.form-title {
    font-size: 28px;
    font-weight: 700;
    color: #151717;
    margin: 0 0 8px 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.form-subtitle {
    font-size: 16px;
    color: #666;
    margin: 0;
    font-weight: 400;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}

.form button {
    align-self: flex-end;
}

.flex-column {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.flex-column > label {
    color: #151717;
    font-weight: 600;
}

.inputForm {
    border: 1.5px solid #ecedec;
    border-radius: 10px;
    height: 50px;
    display: flex;
    align-items: center;
    padding-left: 10px;
    transition: 0.2s ease-in-out;
    position: relative;
}

.input {
    margin-left: 10px;
    border-radius: 10px;
    border: none;
    width: 85%;
    height: 100%;
    background: transparent;
}

.input:focus {
    outline: none;
}

.inputForm:focus-within {
    border: 1.5px solid #2d79f3;
}

.input:-webkit-autofill,
.input:-webkit-autofill:hover,
.input:-webkit-autofill:focus,
.input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 30px #e7f3ff inset !important;
    -webkit-text-fill-color: #000 !important;
    border-radius: 10px;
    transition: background-color 5000s ease-in-out 0s;
}

.inputForm:has(.input:-webkit-autofill) {
    background-color: #e7f3ff;
    border-color: #2d79f3;
}

.inputForm.autofill {
    background-color: #e7f3ff;
    border-color: #2d79f3;
}

.inputForm:focus-within {
    border: 1.5px solid #2d79f3;
}

.error-border {
    border: 1.5px solid #ef4444 !important;
}

.error-text {
    color: #ef4444;
    font-size: 12px;
    margin-top: -5px;
}

.password-toggle {
    cursor: pointer;
    width: 20px;
    height: 20px;
    margin-right: 10px;
}

.flex-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    justify-content: space-between;
}

.flex-row > div > label {
    font-size: 14px;
    color: black;
    font-weight: 400;
}

.span {
    font-size: 14px;
    margin-left: 5px;
    color: #2d79f3;
    font-weight: 500;
    cursor: pointer;
    text-decoration: none;
}

.button-submit {
    margin: 20px 0 10px 0;
    background-color: #151717;
    border: none;
    color: white;
    font-size: 15px;
    font-weight: 500;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    cursor: pointer;
}

.button-submit:hover {
    background-color: #252727;
}

.button-submit:disabled {
    background-color: #666;
    cursor: not-allowed;
}

.p {
    text-align: center;
    color: black;
    font-size: 14px;
    margin: 5px 0;
}

.btn {
    margin-top: 10px;
    width: 100%;
    height: 50px;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: 500;
    gap: 10px;
    border: 1px solid #ededef;
    background-color: white;
    cursor: pointer;
    transition: 0.2s ease-in-out;
}

.btn:hover {
    border: 1px solid #2d79f3;
}

a {
    text-decoration: none;
}
</style>