import {ref, computed} from "vue";
import {useRouter} from "vue-router";
import type {AuthInterface, TokenInterface} from "~/interfaces/auth";
import {AuthServices} from "~/services/auth";


export const TOKEN_KEY = "euro_cert_token";

const token = ref<TokenInterface | null>(null)

export function useAuth() {
    const router = process.client ? useRouter() : null;

    if (process.client) {
        const stored = localStorage.getItem(TOKEN_KEY);
        token.value = stored ? JSON.parse(stored) as TokenInterface : null;
    }

    const isAuthenticated = computed(() => !!token.value?.access_token);

    function setToken(newToken: TokenInterface) {
        if (process.client) {
            token.value = newToken;
            localStorage.setItem(TOKEN_KEY, JSON.stringify(newToken));
        }
    }

    function clearToken() {
        if (process.client) {
            token.value = null;
            localStorage.removeItem(TOKEN_KEY);
        }
    }

    async function login(credentials: AuthInterface) {
        const {res, data} = await AuthServices.login(credentials);
        if (res.status === 200 && data.access_token) {
            setToken({
                token_type: data.token_type,
                access_token: data.access_token
            });
            if (router) {
                router.push('/');
            }
        }

        return {res, data};
    }

    function logout() {
        clearToken();
        if (router) {
            router.push('/login');
        }
    }

    function forbidden() {
        if (router) {
            router.push('/');
        }
    }

    function getAuthToken() {
        if (!token.value) return "";
        return `${token.value.token_type} ${token.value.access_token}`;
    }

    return {token, isAuthenticated, login, logout, forbidden, getAuthToken};
}
