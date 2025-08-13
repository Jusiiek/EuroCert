<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <AuthForm
        title="Login"
        buttonText="Sign In"
        @submit="handleLogin"
        class="max-w-[600px] w-full"
    />
  </div>
</template>

<script setup>
definePageMeta({
  layout: 'auth'
})

function handleLogin(data) {
  console.log("Login data:", data)
  // TODO: handle login
}
</script>

<style scoped>

</style>