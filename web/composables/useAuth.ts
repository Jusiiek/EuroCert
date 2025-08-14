import {ref, computed} from "vue";
import {useRouter} from "vue-router";
import type {AuthInterface} from "~/interfaces/auth";
import {AuthServices} from "~/services/auth";

export interface TokenInterface {
    access_token: string;
    token_type: string
}

export const TOKEN_KEY = "euro_cert_token";

const token = ref<TokenInterface | null>(
    localStorage.getItem(TOKEN_KEY)
        ? JSON.parse(localStorage.getItem(TOKEN_KEY) as string)
        : null
);

export function useAuth() {
    const router = useRouter();

    const isLoggedIn = computed(() => !!token.value?.access_token);

    function setToken(newToken: TokenInterface) {
        token.value = newToken;
        localStorage.setItem('authToken', JSON.stringify(newToken));
    }

    function clearToken() {
        token.value = null;
        localStorage.removeItem(TOKEN_KEY);
    }

    async function login(credentials: AuthInterface) {
        const {res, data} = await AuthServices.login(credentials);
        if (res.status === 200 && data.access_token) {
            setToken({
                token_type: data.token_type,
                access_token: data.access_token
            });
        }

        return {res, data};
    }

    function logout() {
        clearToken();
        router.push('/login');
    }

    function getAuthToken() {
        if (!token.value) return "";
        return `${token.value.token_type} ${token.value.access_token}`;
    }

    return {token, isLoggedIn, login, logout, getAuthToken};
}
