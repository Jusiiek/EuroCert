<template>
  <AuthForm title="Login" buttonText="Sign In" @submit="handleLogin" />
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