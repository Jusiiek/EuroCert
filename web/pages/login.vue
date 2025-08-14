<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <AuthForm
        title="Login"
        buttonText="Sign In"
        linkLabel="Dont have an account? Create now!"
        linkTarget="/register"
        @submit="handleLogin"
        class="max-w-[600px] w-full"
    />
  </div>
</template>

<script setup>
import { useAuth } from "~/composables/useAuth";

definePageMeta({
  layout: 'auth',
  middleware: 'auth'
})

const { login } = useAuth();

async function handleLogin(loginData) {
  const { res, data } = await login(loginData);
  if (res.status !== 200) {
    alert(`Login failed: ${data.detail}`)
  }

}

</script>

<style scoped>

</style>