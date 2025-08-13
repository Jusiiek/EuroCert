<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <AuthForm
        title="Register"
        buttonText="Sign Up"
        @submit="handleRegister"
        class="max-w-[600px] w-full"
    />
  </div>
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