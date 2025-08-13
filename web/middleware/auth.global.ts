export default defineNuxtRouteMiddleware((to, from) => {

    const publicPages = ['/login', '/register']

    if (publicPages.includes(to.path)) {
        return
    }

    const token = process.client ? localStorage.getItem('token') : null
    if (!token) {
        return navigateTo('/login')
    }
})
