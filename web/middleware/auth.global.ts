import {ActiveUser} from "~/services/active_user";

export default defineNuxtRouteMiddleware((to, from) => {
    const publicPages = ['/login', '/register'];
    const token = ActiveUser.getToken();

    if (publicPages.includes(to.path) && token) {
        if (to.path !== '/') return navigateTo('/');
    }

    if (!token && !publicPages.includes(to.path)) {
        return navigateTo('/login');
    }
});
