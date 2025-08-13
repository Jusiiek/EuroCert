<template>
  <AuthForm title="Register" buttonText="Sign Up" @submit="handleRegister" />
</template>

<script setup>
definePageMeta({
  layout: 'auth'
})

function handleRegister(data) {
  console.log("Register data:", data)
  // TODO: Handle register
}
</script>


<style scoped>

</style>