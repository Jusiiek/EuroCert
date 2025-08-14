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
import { AuthServices } from "~/services/auth.js";
import { useRouter } from 'vue-router';

definePageMeta({
  layout: 'auth'
})

const router = useRouter();

async function handleLogin(loginData) {
  const { res, data } = await AuthServices.login(loginData);
  if (res.status === 200) {
    router.push('/')
    return
  }
  alert(`Login failed: ${data.detail}`)
}

</script>

<style scoped>

</style>