import {useAuth} from '~/composables/useAuth';

export default defineNuxtRouteMiddleware((to, from) => {
    const {isLoggedIn} = useAuth();
    if (!isLoggedIn.value && to.meta.auth !== false) {
        return navigateTo('/login');
    }
});
