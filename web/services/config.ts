export const getApiUrl = (): string => {
    const config = useRuntimeConfig()
    return config.public.apiUrl
}
