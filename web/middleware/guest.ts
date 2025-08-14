import {useAuth} from "~/composables/useAuth";

export default defineNuxtRouteMiddleware((to, from) => {
    const {isAuthenticated} = useAuth();

    const openPaths = ["/login", "/register"];
    if (!isAuthenticated.value && !openPaths.includes(to.path)) {
        return navigateTo("/login");
    }
})
